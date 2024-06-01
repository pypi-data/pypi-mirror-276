import glob
import os
import subprocess
import toml
import asyncio
import hashlib
import shutil
import urllib
from collections import defaultdict

from subpop.util import AttrDict

from metatools.cmd import run_shell

# TODO: although this is currently working, it's not recommended.
#       we should look into using non-dyne references to these classes more.
# from funtoo.pkgtools.ebuild import Artifact, Archive
import dyne.org.funtoo.metatools.pkgtools as pkgtools


async def add_crates_bundle(
	hub,
	pkginfo,
	cargo_lock_data=None,
	cargo_lock_path=None,
	src_artifact=None,
	src_dir_glob="*",
):
	"""
	This is the new, preferred way to handle the dependencies of Rust packages in Funtoo.

	This function generates a bundle containing all necessary crates for the given Rust package,
	which can be used by your ebuild and Funtoo's ``cargo.eclass`` transparently.

	This solves the problem of having to download hundreds of individual crates when you emerge
	something -- instead, you just download the bundle from our CDN, in one HTTP request.

	To use this function, you will want to call it from your autogen. There are a variety of ways
	to call it, due to the variety of ways to grab a "Cargo.lock".

	If you want to simply have this method use the "Cargo.lock" from an Artifact, the easiest way
	to do this is to set ``pkginfo['artifacts'] = { 'main': <your artifact> }``. The Artifact does
	not need to be downloaded yet. This function will fetch it and look inside for a "Cargo.lock".

	Alternatively, you can use the ``src_artifact=`` keyword argument if your source Artifact is
	not in pkginfo, or if your ``artifacts`` are not in a dictionary (e.g. if you are using this
	function in conjunction with GitHub helpers like ``release_gen`` or ``tag_gen``).

	You can also pass ``cargo_lock_data`` or ``cargo_lock_path`` if your "Cargo.lock" is located
	elsewhere, or if you happen to have read its contents already.

			Upon completion, metatools will create its own archive from scratch and store it in the local
			binary object store, and copy it to $DISTDIR for you for convenience.

	To use the generated bundle in a template, simply set ``SRC_URI`` to the new ``{{src_uri}}``
	template variable, which will include all Artifacts in the BreezyBuild. The ``cargo.eclass``
	in Funtoo will use this bundle automatically if this function was used and will identify it by
	its special name. It will then source all crates from it instead of fetching them one by one.
	"""
	# For convenience/convention, if there is a pkginfp['artifacts']['main'], use it automatically.
	if (
		"artifacts" in pkginfo
		and isinstance(pkginfo["artifacts"], dict)
		and "main" in pkginfo["artifacts"]
	):
		src_artifact = pkginfo["artifacts"]["main"]

	pkginfo["crates_bundle"] = AttrDict()

	if src_artifact:
		await src_artifact.ensure_fetched()
		src_artifact.extract()

		src_dir = glob.glob(os.path.join(src_artifact.extract_path, src_dir_glob))[0]

		cargo_lock_path = os.path.join(src_dir, "Cargo.lock")
		if not os.path.exists(cargo_lock_path):
			cargo_cmd = subprocess.Popen(["cargo", "update"], cwd=src_dir).wait()

		crates, pkginfo["crates_bundle"].crates_artifacts = await generate_crates_metadata(
			lock_path=cargo_lock_path
		)

		src_artifact.cleanup()
	elif cargo_lock_data:
		crates, pkginfo["crates_bundle"].crates_artifacts = await generate_crates_metadata(
			lock_data=cargo_lock_data
		)
	elif cargo_lock_path:
		crates, pkginfo["crates_bundle"].crates_artifacts = await generate_crates_metadata(
			lock_path=cargo_lock_path
		)
	else:
		raise ValueError("No source of `Cargo.lock` provided.")

	crates_hash = hashlib.sha512(crates.encode("utf-8")).hexdigest()

	pkginfo["crates_bundle"].key = AttrDict(
		{
			"catpkg": f"{pkginfo['cat']}/{pkginfo['name']}",
			"version": pkginfo["version"],
			"crates_hash": crates_hash,
		}
	)
	pkginfo[
		"crates_bundle"
	].final_name = f"{pkginfo['name']}-{pkginfo['version']}-funtoo-crates-bundle-{pkginfo['crates_bundle'].key.crates_hash}.tar.gz"

	crates_archive = await create_crates_archive(hub, pkginfo)

	if "artifacts" not in pkginfo:
		pkginfo["artifacts"] = {}

	if isinstance(pkginfo["artifacts"], list):
		pkginfo["artifacts"].append(crates_archive)
	elif isinstance(pkginfo["artifacts"], dict):
		pkginfo["artifacts"]["crates_bundle"] = crates_archive
	else:
		raise ValueError(
			f"Unrecognized type for pkginfo['artifacts']: {type(pkginfo['artifacts'])}"
		)


async def create_crates_archive(hub, pkginfo):
	"""
	This is a helper function which interfaces with metatools' dynamic archive functionality and
	grabs a reference to an existing crates bundle if it exists locally, and if it doesn't, it gets
	it created. It does this by ensuring that all crates are downloaded using our spider and then
	creates an archive that contains all the crates inside.

	Note: autogen writers typically don't need to call this. Use ``add_crates_archive`` instead.

			:param hub: your hub (local variable)
			:param pkginfo: your pkginfo
			:return: an ``Archive``, suitable to be added as an Artifact.
	"""
	crates_bundle = pkginfo["crates_bundle"]

	(crates_archive, *_) = hub.Archive.find(
		key=crates_bundle.key, final_name=crates_bundle.final_name
	)

	if crates_archive:
		return crates_archive

	crates_archive = hub.Archive(crates_bundle.final_name)
	await crates_archive.initialize(f"funtoo-crates-bundle-{pkginfo['name']}")

	crates_artifacts = crates_bundle.crates_artifacts

	# Fetch crates in parallel
	await asyncio.gather(*[artifact.ensure_completed() for artifact in crates_artifacts])

	for artifact in crates_artifacts:
		shutil.copy(
			artifact.blos_object.blob.path,
			os.path.join(crates_archive.top_path, artifact.final_name),
		)

	await crates_archive.store(key=crates_bundle["key"])

	return crates_archive


async def fetch_git_dependency(url, crates):
	parsed_url = urllib.parse.urlparse(url)

	ref = parsed_url.fragment
	repo_url = parsed_url._replace(fragment="", query="").geturl()

	repo_name = urllib.parse.quote(repo_url, safe="")

	archive_name = f"{repo_name}-{ref}.tar.xz"
	archive_key = AttrDict({"git_url": repo_url, "ref": ref})

	# archive, _ = Archive.find(key=archive_key, final_name=archive_name)
	archive, _ = pkgtools.ebuild.Archive.find(key=archive_key, final_name=archive_name)
	if archive is None:
		# archive = Archive(final_name=archive_name)
		archive = pkgtools.ebuild.Archive(final_name=archive_name)

		dir_name = f"{repo_name}-{ref}"
		await archive.initialize(dir_name)

		await run_shell(f"git clone --depth=1 {repo_url} {archive.top_path}")
		await run_shell(
			f"(cd {archive.top_path} && git fetch origin {ref} && git reset --hard {ref})"
		)
		await run_shell(
			f"(cd {archive.top_path} && git submodule update --init --recursive)"
		)

		crate_locations = {}
		for cargo_path in glob.glob(
				os.path.join(archive.top_path, "**/Cargo.toml"), recursive=True
		):
			with open(cargo_path, "r") as cargo_file:
				cargo_data = cargo_file.read()

			cargo_data = toml.loads(cargo_data)

			cargo_package_data = cargo_data.get("package", None)
			if cargo_package_data is None:
				continue

			cargo_package_name = cargo_package_data.get("name", None)
			if cargo_package_name is None:
				continue

			crate_locations[cargo_package_name] = os.path.relpath(
				os.path.dirname(cargo_path), os.path.dirname(archive.top_path)
			)

		cargo_config_content = f"[patch.'{repo_url}']\n"
		for crate in crates:
			crate_location = crate_locations[crate]

			cargo_config_content += f"{crate} = {{ path = \"{os.path.join('%CRATES_DIR%', crate_location)}\" }}\n"

		with open(
				os.path.join(archive.top_path, "funtoo_config.toml"), "w"
		) as config_file:
			config_file.write(cargo_config_content)

		await archive.store(key=archive_key)

	return archive


async def generate_crates_metadata(lock_path=None, lock_data=None):
	"""
	This function generates crates data for the CRATES variable used in ebuilds, and also returns a
	list of attributes to use to create new Artifacts for all crates that need to be downloaded to
	build the project.
	:param lock_path: If provided, open this Cargo.lock file and read its contents (string)
	:param lock_data: If provided, this is a string containing the contents of Cargo.lock
	:return: a tuple containing a string to use in CRATES, plus a list of attributes to use to
					 to create Artifacts.
	"""
	if lock_path:
		with open(lock_path, "r") as f:
			lock_data = f.read()

	if lock_data is None:
		raise ValueError(
			"No source of lock data provided. Please provide either `lock_path` or `lock_data`."
		)

	crates_dict = toml.loads(lock_data)

	crates = ""
	crates_artifacts = []

	git_crates = defaultdict(list)

	for package in crates_dict["package"]:
		if "source" not in package:
			continue

		name = package["name"]
		version = package["version"]
		source = package["source"]

		source_origin = "crates"

		if source.startswith("git+"):
			source_origin = "git"

			url = source.lstrip("git+")

			# Append ref to version so that ref changes reflect in the hash.
			#
			# Note that this breaks the legacy CRATES approach, which should
			# be fine, as it doesn't support git crates either way. We do this
			# instead of altering the hash computation to avoid recreating all
			# existing cached archives.
			ref = url.rsplit("#", 2)[-1]
			version += f"-{ref}"

			git_crates[url].append(name)

		crates = crates + name + "-" + version + "\n"

		if source_origin == "crates":
			final_name = f"{name}-{version}.crate"

			crates_artifacts.append(
				# Artifact(
				pkgtools.ebuild.Artifact(
					url=(
							"https://crates.io/api/v1/crates/"
							+ name
							+ "/"
							+ version
							+ "/download"
					),
					final_name=final_name,
				)
			)

	for url, contained_crates in git_crates.items():
		git_archive = await fetch_git_dependency(url, contained_crates)

		crates_artifacts.append(git_archive)

	return crates, crates_artifacts


async def generate_crates_from_artifact(src_artifact, src_dir_glob="*"):
	"""
	IMPORTANT: It's now preferred to use ``add_crates_bundle`` instead, which uses dynamic archives
	and avoids having hundreds of files in SRC_URI.

	This method, when passed an Artifact, will fetch the artifact, extract it, look in the directory
	``src_dir_glob`` (a glob specifying the name of the source directory within the extracted files
	which contains ``Cargo.lock`` -- you can also specify sub-directories as part of this glob), and
	will then parse ``Cargo.lock`` for package names, and then generate a list of artifacts for each
	crate discovered. This list of new artifacts will be returned as a list. In the case there is no
	``Cargo.lock`` present in the artifact, ``cargo update`` will be run to generate one.
	"""
	await src_artifact.fetch()
	src_artifact.extract()

	src_dir = glob.glob(os.path.join(src_artifact.extract_path, src_dir_glob))[0]

	cargo_lock_path = os.path.join(src_dir, "Cargo.lock")
	if not os.path.exists(cargo_lock_path):
		await run_shell(["cargo", "update"], chdir=src_dir)

	crates, crates_artifacts = await generate_crates_metadata(lock_path=cargo_lock_path)

	src_artifact.cleanup()

	return dict(crates=crates, crates_artifacts=crates_artifacts)
