#!/usr/bin/env python3

from __future__ import annotations
import asyncio
import logging
import os
import shutil
import threading
from asyncio import Task
from collections import OrderedDict, defaultdict
from collections.abc import Mapping
from datetime import datetime
from subprocess import getstatusoutput
from typing import Optional, Tuple

import jinja2

from metatools.cmd import capture_bg
from metatools.store import StoreObject
from metatools.fastpull.spider import FetchError, FetchRequest

log = logging.getLogger('metatools.autogen')

import dyne.org.funtoo.metatools.pkgtools as pkgtools


class BreezyError(Exception):
	def __init__(self, msg):
		self.msg = msg


class Archive:

	_final_name: str = None
	_top_directory: str = None

	def __init__(self, final_name):
		"""
		:param final_name: This is the on-disk name for the artifact, which may be different from
			what is in the URL.
		"""
		self._final_name = final_name
		self.breezybuilds = []
		self.blos_object: Optional[StoreObject] = None

	@property
	def final_data(self):
		if self.blos_object:
			return self.blos_object.data["hashes"]
		return None

	@property
	def url(self):
		sha = self.final_data["sha512"]
		return f"https://direct.funtoo.org/{sha[0:2]}/{sha[2:4]}/{sha[4:6]}/{sha}"

	@property
	def src_uri(self):
		if self._final_name is None:
			return self.url
		else:
			return self.url + " -> " + self._final_name

	@property
	def catpkgs(self):
		outstr = ""
		for bzb in self.breezybuilds:
			outstr = f"{outstr} {bzb.catpkg}"
		return outstr.strip()

	@property
	def extract_path(self):
		return os.path.join(pkgtools.model.temp_path, "artifact_extract", self.final_name)

	@property
	def temp_archive_path(self):
		return os.path.join(pkgtools.model.temp_path, "archive_create", self.final_name)

	@property
	def work_path(self):
		return os.path.join(pkgtools.model.temp_path, "archive_work", self.final_name)

	async def create_work_path(self):
		if os.path.exists(self.work_path):
			await capture_bg(f"rm -rf {self.work_path}")
		os.makedirs(self.work_path, exist_ok=True)

	@property
	def final_path(self):
		return self.blos_object.blob.path

	@property
	def final_name(self):
		return self._final_name

	@property
	def top_path(self):
		if self._top_directory:
			return os.path.join(self.extract_path, self._top_directory)
		else:
			return os.path.join(self.extract_path)

	async def initialize(self, top_directory=None):
		"""
		This method is supposed to create an empty extract_path so we can fill the archive with
		things we want. top_directory is optional and specifies the directory to create which will
		contain the files.
		:return:
		"""
		self._top_directory = top_directory
		if os.path.exists(self.extract_path):
			await capture_bg(f"rm -rf {self.extract_path}")
		os.makedirs(self.top_path, exist_ok=False)

	async def store(self, key: dict = None, metadata: dict = None, existing=None):
		"""
		This method will store an archive as a dynamic archive, indexed by ``key``. By default, it
		will use the contents of ```self.temp_archive_path``` to grab the contents; if instead you
		already have a created archive you want to store, you can simply pass the path in the
		``existing`` argument, and this exact file will be used instead.

		If you want to store a dynamic archive for later retrieval *by name*, then use the
		``Archive.store_by_name`` method instead.

		An optional ``metadata`` dictionary can be provided, which will also be stored with the
		dynamic archive. A datestamp will automatically be stored in ``metadata['created_on']`` for
		you. All other metadata can be provided by you. This metadata, unlike the key, is not used
		to *find*/*match* the object when retrieval is attempted; instead, the metadata is just made
		available to you upon retrieval. So you can use it to store extra things that are of
		interest to you.
		"""
		if key is None:
			key = {}

		if metadata is None:
			metadata = {}
		metadata["created_on"] = datetime.utcnow()

		if not existing:

			temp_archive = self.temp_archive_path

			# Ensure we have a clean location for creating a new temporary archive:

			if not os.path.exists(os.path.dirname(temp_archive)):
				os.makedirs(os.path.dirname(temp_archive), exist_ok=True)

			if os.path.exists(temp_archive):
				os.unlink(temp_archive)

			# Create the archive:

			if self.final_name.endswith(".tar.xz"):
				cmd = f"tar -C {self.extract_path} -cJf {temp_archive} ."
			elif self.final_name.endswith(".tar.gz"):
				cmd = f"tar -C {self.extract_path} -czf {temp_archive} ."
			elif self.final_name.endswith(".tar.zst"):
				cmd = f"tar -C {self.extract_path} -c --zstd -f {temp_archive} ."
			else:
				raise ValueError(f"Unrecognized archive format: {self.final_name}. Supported formats: tar.gz, tar.xz, tar.zst")
			log.debug(f"store: command: {cmd}")

			proc, out = await capture_bg(cmd)
			if proc.returncode != 0:
				raise pkgtools.ebuild.BreezyError(f"Couldn't execute {cmd}. Output: {out}")

			# Store in BLOS and create integrity database reference:
			existing = temp_archive

		self.blos_object = pkgtools.model.blos.insert_blob(existing)
		pkgtools.model.fastpull_session.store_file_dynamic(key, existing, metadata=metadata)

		# If we are running in non-production mode, then attempt to copy the generated distfile into
		# /var/cache/portage/distfiles so it is "already fetched" as it will not exist on the CDN yet.
		# This allows local testing of the autogenerated ebuild:

		if not pkgtools.model.prod:
			dist_path = f"/var/cache/portage/distfiles/{self.final_name}"
			# try to link file into /var/cache/portage/distfiles:
			try:
				if os.path.exists(dist_path):
					os.unlink(dist_path)
				shutil.copy(self.blos_object.blob.path, dist_path)
			except PermissionError:
				log.warning(f"Unable to copy dynamic archive to {dist_path}. Make sure you are in the portage group.")

	async def store_by_name(self, key: dict = None, metadata: dict = None, existing=None):
		"""
		This method will store the contents of ``self.temp_archive_path`` as a dynamic archive, and will be indexed by
		name, and with an optional provided key, so that it can be retrieved by name using the ``Archive.find_by_name``
		classmethod.

		This method now has an optional ``existing=`` keyword argument if you already have an archive that exists.
		If you provide a path to this archive, its exact contents will be used instead of tarring up whatever is in
		``self.temp_archive_path``.
		"""
		if key is None:
			key = {}
		# We must make final_name part of the key used to find the archive:
		key["final_name"] = self.final_name
		return await self.store(key, metadata, existing=existing)

	@classmethod
	def find(cls, key: dict = None, final_name: str = None) -> Tuple[Archive, dict] | Tuple[None, None]:
		"""
		This classmethod is the big brother of ``Archive.find_by_name()`` and is more flexible. It allows
		dynamic archives to be found by an arbitrary key. This allows archives to be found where you may not
		exactly know the final_name (aka filename) of the archive.

		This classmethod is used to implement ``Archive.find_by_name()`` as well. It accepts a key, which
		is assumed to be "final" -- i.e. "ready to go", unless a ``final_name`` is specified, in which case
		it will be added to the key to look for that specific named file.
		"""
		if pkgtools.model.force_dynamic:
			# force auto-generation of dynamic archive by purposely returning "not found".
			return None, None
		if key is None:
			key = {}
		if final_name:
			key["final_name"] = final_name
		blos_object, metadata = pkgtools.model.fastpull_session.get_file_dynamic(key)
		log.debug(f"In find, blos object found: {blos_object} using key {key}")
		if blos_object is None:
			return None, None
		else:
			if not final_name:
				final_name = metadata["final_name"]
			found_archive = Archive(final_name)
			found_archive.blos_object = blos_object
			return found_archive, metadata

	@classmethod
	def find_by_name(cls, final_name: str, key: dict = None) -> Tuple[Archive, dict] | Tuple[None, None]:
		"""
		This classmethod is used to attempt to find a dynamic archive (see docs/features/dynamic_archives.rst) by
		*name*. This means you are looking for a file with a specific, known filename.

		Specify the filename as an argument, along with an optional dictionary key containing data that *must*
		match for the archive to be considered acceptable for your purposes.

		A tuple containing the Archive and a dictionary containing metadata stored with the Archive is returned,
		or a (None, None) tuple if nothing was found that met the criteria.
		"""
		return cls.find(key=key, final_name=final_name)

	def extract(self):
		ep = self.extract_path
		os.makedirs(ep, exist_ok=True)
		if self.final_name.endswith(".zip"):
			cmd = f"unzip -o {self.final_path} -d {ep}"
		else:
			cmd = f"tar -C {ep} -xf {self.final_path}"
		s, o = getstatusoutput(cmd)
		if s != 0:
			raise pkgtools.ebuild.BreezyError("Command failure: %s" % cmd)

	def cleanup(self):
		# TODO: check for path stuff like ../.. in final_name to avoid security issues.
		getstatusoutput("rm -rf " + os.path.join(pkgtools.model.temp_path, "artifact_extract", self.final_name))

	@property
	def hashes(self):
		return self.blos_object.data["hashes"]

	@property
	def size(self):
		return self.blos_object.data["hashes"]["size"]

	def hash(self, h):
		return self.blos_object.data["hashes"][h]

	async def ensure_completed(self) -> bool:
		return True


class Artifact(Archive):
	"""
	An artifact is a tarball or other archive that is used by a BreezyBuild, and ultimately referenced in an ebuild.
	It's also possible that an artifact could be fetched by an autogen directly, but not included in an ebuild.
	All Artifacts have a ``url`` which represents the official download location of the artifact.

	If an artifact is going to be incorporated into an ebuild, it's passed to the ``artifacts=`` keyword argument
	of the ``BreezyBuild`` constructor. When it is passed in this way, we perform extra processing. We will store the
	resultant download BLOS (base layer object store) and create a reference to this binary blob in the distfile
	integrity database, so the URL is associated with the hashes.sha512 index in the BLOS.

	So, say that "sys-apps/foo-1.0.ebuild" references "foo-1.0.tar.gz". The distfile integrity database entry
	will associate the download URL for "foo-1.0.tar.gz" with its hashes.sha512 digest, which also happens to be
	the index for the binary data in the BLOS.
	"""

	def __init__(self, url=None, key=None, final_name=None, extra_http_headers=None, **kwargs):
		"""
		:param url: A required URL for fetching the resource.
		:param key: Appears unused.
		:param final_name: This is the on-disk name for the artifact, which may be different from
			what is in the URL.
		:param extra_http_headers: An optional dictionary of additional HTTP headers to be used
			when fetching the file.
		:param kwargs: Not used, but allows extra keyword arguments to be passed to constructor
			which will be ignored.
		"""

		# Initialization of final_name. This has to happen in this order to work.

		self._url = url
		if final_name:
			self._final_name = final_name

		super().__init__(self.final_name)

		assert self._url is not None
		try:
			assert self._url.split(':')[0] in ['http', 'https', 'ftp']
		except (IndexError, AssertionError):
			raise ValueError(f"url= argument of Artifact is '{self._url}', which appears malformed or an unsupported protocol.")
		self.key = key
		self.extra_http_headers = extra_http_headers

	@property
	def url(self):
		return self._url

	@property
	def final_name(self):
		if self._final_name is None:
			return self.url.split("/")[-1]
		else:
			return self._final_name

	async def fetch(self):
		await self.ensure_fetched()

	def is_fetched(self):
		return os.path.exists(self.final_path)

	def extract(self):
		if not self.exists:
			self.fetch()
		super().extract()

	def exists(self):
		return self.is_fetched()

	async def ensure_fetched(self, throw=True) -> bool:
		"""
		This function ensures that the artifact is 'fetched' -- in other words, it exists locally. This means we can
		calculate its hashes or extract it.

		Returns a boolean with True indicating success and False failure when ``throw=False``. By default, the
		original fetch exception will be raised on error.
		"""

		if self.blos_object is not None:
			return True
		try:
			# TODO: add extra headers, retry,
			req = FetchRequest(self.url,
				extra_headers=self.extra_http_headers,
				# TODO: we currently don't support authenticating to retrieve an Artifact (just HTTP requests for API)
				username=None,
				password=None,
				final_name=self.final_name
			)
			log.debug(f'Artifact.ensure_fetched:{threading.get_ident()} now fetching {self.url} using FetchRequest {req}')
			# TODO: this used to be indexed by catpkg, and by final_name. So we are now indexing by source URL.
			# TODO: what exceptions are we interested in here?
			self.blos_object = await pkgtools.model.fastpull_session.get_file_by_url(req)
			# This above call takes some IO, so if we are being hammered with ensure_fetched() calls, this allows
			# downloads to stay responsive, hopefully.
			await asyncio.sleep(0)
		except FetchError as fe:
			# We encountered some error retrieving the resource.
			if throw:
				raise fe
			log.error(f"Fetch error: {fe}")
			return False
		return True

	async def ensure_completed(self) -> bool:
		return await self.ensure_fetched()

	async def try_fetch(self):
		"""
		This is like ensure_fetched, but will return an exception if the download fails.
		"""
		await self.ensure_fetched(throw=True)


def aggregate(meta_list):
	out_list = []
	for item in meta_list:
		if isinstance(item, list):
			out_list += item
		else:
			out_list.append(item)
	return out_list


class BreezyBuild:

	autogen_id = None
	cat = None
	name = None
	path = None
	template = None
	version = None
	_revision = None
	source_tree = None
	output_tree = None
	template_args = None

	@property
	def revision(self):
		if self._revision is None:
			self._revision = 0
		else:
			self.fixup_revision()
		return self._revision

	def __init__(
		self,
		artifacts=None,
		template: str = None,
		template_text: str = None,
		template_path: str = None,
		autogen_id=None,
		**kwargs,
	):
		self.autogen_id = autogen_id
		self.source_tree = self.output_tree = pkgtools.model.locator.root
		self._pkgdir = None
		self.template_args = kwargs
		for kwarg in ["cat", "name", "version", "path"]:
			if kwarg in kwargs:
				setattr(self, kwarg, str(kwargs[kwarg]))
		if "revision" in kwargs:
			self._revision = kwargs["revision"]

		self.template = template
		self.template_text = template_text
		if template_path is None:
			if "path" in self.template_args:
				# If we have a pkginfo['path'], this gives us our current processing path.
				# Use this as a base for our default template path.
				self._template_path = os.path.join(self.template_args["path"] + "/templates")
			else:
				# This is a no-op, but wit this set to None, we will use the template_path()
				# property to get the value, which will be relative to the repo root and based
				# on the setting of name and category.
				self._template_path = None
		else:
			# A manual template path was specified.
			self._template_path = template_path
		if self.template_text is None and self.template is None:
			self.template = self.name + ".tmpl"
		if artifacts is None:
			self.artifacts = []
		else:
			self.artifacts = artifacts
		self.template_args["artifacts"] = artifacts
		self.template_args["autogen_id"] = autogen_id

	def fixup_revision(self):
		"""
		Expand revision based on YAML structure which may have version-specific revision information, like this:

		revision:
		  2.0.0: 1

		We only want to apply this revision info if the version happens to match.
		"""
		if self._revision:
			if isinstance(self._revision, int):
				pass
			elif isinstance(self._revision, dict):
				if self.version in self._revision:
					self._revision = self._revision[self.version]
				else:
					self._revision = 0
			elif isinstance(self._revision, str):
				self._revision = int(self._revision)
			else:
				raise TypeError(f"Unrecognized type for revision= argument for {self.catpkg}: {repr(type(self._revision))}")
			pkgtools.model.log.debug(f"Fixup-revision: {self.catpkg}: {type(self._revision)} {self._revision}")

	def iter_artifacts(self):
		if type(self.artifacts) == list:
			for artifact in self.artifacts:
				yield artifact
		elif type(self.artifacts) in (dict, OrderedDict, defaultdict):
			for key, artifact in self.artifacts.items():
				if isinstance(artifact, list):
					for lil_art in artifact:
						yield lil_art
				else:
					yield artifact
		else:
			raise TypeError("Invalid type for artifacts passed to BreezyBuild -- should be list or dict.")

	@property
	def src_uri(self):
		out = ""
		for artifact in self.iter_artifacts():
			out += f"{artifact.src_uri}\n"
		return out.rstrip()

	@property
	def src_uri_with_use(self):
		if not isinstance(self.artifacts, dict):
			return self.src_uri
		out = ""
		for key, artifact_list in self.artifacts.items():
			if key == "global":
				if isinstance(artifact_list, list):
					for artifact in artifact_list:
						out += f"{artifact.src_uri}\n"
				elif isinstance(artifact_list, Archive) or isinstance(artifact_list, Artifact):
					out += f"{artifact_list.src_uri}\n"
				else:
					ValueError(f"Found {artifact_list} of type {type(artifact_list)} inside artifacts.")
			else:
				if isinstance(artifact_list, list):
					out += f"{key}? (\n"
					for artifact in artifact_list:
						out += f"  {artifact.src_uri}\n"
					out += ")\n"
				elif isinstance(artifact_list, Archive) or isinstance(artifact_list, Artifact):
					out += f"{key}? ( {artifact_list.src_uri} )\n"
				else:
					ValueError(f"Found {artifact_list} of type {type(artifact_list)} inside artifacts.")
		return out

	async def setup(self):
		"""
		This method performs some special setup steps. We tend to treat Artifacts as stand-alone objects -- and they
		can be -- such as if you instantiate an Artifact in `generate()` and fetch it because you need to extract it
		and look inside it.

		But when associated with a BreezyBuild, as is commonly the case, this means that there is a relationship between
		the Artifact and the BreezyBuild.

		In this scenario, we know that the Artifact is associated with a catpkg, and will be written out to a Manifest.
		So this means we want to create some associations. We want to record that the Artifact is associated with the
		catpkg of this BreezyBuild. We use this for writing new entries to the Distfile Integrity database for
		to-be-fetched artifacts.
		"""

		fetch_tasks_dict = {}

		for artifact in self.iter_artifacts():
			if isinstance(artifact, Mapping):
				artifact = Artifact(**artifact)

			# This records that the artifact is used by this catpkg, because an Artifact can be shared among multiple
			# catpkgs. This is used for the integrity database writes:

			if self not in artifact.breezybuilds:
				artifact.breezybuilds.append(self)

			if artifact.__class__.__name__ == "Artifact":
				async def lil_coroutine(a):
					try:
						status = await a.ensure_completed()
						return a, status
					except FetchError as fe:
						pkgtools.model.log.error(fe, exc_info=False)
					except Exception as e:
						pkgtools.model.log.error(e, exc_info=True)

				fetch_task = asyncio.Task(lil_coroutine(artifact))
				fetch_tasks_dict[artifact] = fetch_task

		# Wait for any artifacts that are still fetching:
		results, failures = await pkgtools.autogen.gather_pending_tasks("fetch", fetch_tasks_dict.values())
		completion_list = aggregate(results)
		if failures:
			for fail_task in failures:
				logging.exception("Fetch exception", exc_info=fail_task.exception())
			raise BreezyError("Fetch exceptions encountered.")
		fetch_fail = False
		for artifact, status in completion_list:
			if status is False:
				log.error(f"Artifact for url {artifact.url} referenced in {artifact.catpkgs} could not be fetched.")
				fetch_fail = True
		if fetch_fail:
			raise BreezyError("Unable to fetch at least one artifact.")

	def push(self):
		#
		# https://stackoverflow.com/questions/1408171/thread-local-storage-in-python

		with pkgtools.autogen.GENNED_BREEZYBUILDS_LOCK:
			if self.output_pkgdir in pkgtools.autogen.GENNED_BREEZYBUILDS and pkgtools.autogen.GENNED_BREEZYBUILDS[self.output_pkgdir] != self.autogen_id:
				raise BreezyError(f"{self.output_pkgdir} has already been generated by another autogen: {pkgtools.autogen.GENNED_BREEZYBUILDS[self.output_pkgdir]}.")
			else:
				pkgtools.autogen.GENNED_BREEZYBUILDS[self.output_pkgdir] = self.autogen_id

		async def wrapper(self):
			try:
				await self.generate()
				return True
			except FetchError as fe:
				pkgtools.model.log.error(fe, exc_info=False)
				raise fe
			except Exception as e:
				pkgtools.model.log.error(e, exc_info=True)
				raise e

		# This will cause the BreezyBuild to start autogeneration immediately, appending the task to the thread-
		# local context so we can grab the result later. The return value will be the BreezyBuild object itself,
		# thanks to the wrapper.
		bzb_task = Task(wrapper(self))
		bzb_task.bzb = self
		bzb_task.info = self.catpkg_version_rev
		hub.THREAD_CTX.running_breezybuilds.append(bzb_task)

	@property
	def pkgdir(self):
		if self._pkgdir is None:
			self._pkgdir = os.path.join(self.source_tree, self.cat, self.name)
			os.makedirs(self._pkgdir, exist_ok=True)
		return self._pkgdir

	@property
	def output_pkgdir(self):
		if self._pkgdir is None:
			self._pkgdir = os.path.join(self.output_tree, self.cat, self.name)
			os.makedirs(self._pkgdir, exist_ok=True)
		return self._pkgdir

	@property
	def ebuild_name(self):
		if self.revision == 0:
			return "%s-%s.ebuild" % (self.name, self.version)
		else:
			return "%s-%s-r%s.ebuild" % (self.name, self.version, self.revision)

	@property
	def ebuild_path(self):
		return os.path.join(self.pkgdir, self.ebuild_name)

	@property
	def output_ebuild_path(self):
		return os.path.join(self.output_pkgdir, self.ebuild_name)

	@property
	def catpkg(self):
		return self.cat + "/" + self.name

	def __getitem__(self, key):
		return self.template_args[key]

	@property
	def catpkg_version_rev(self):
		if self.revision == 0:
			return self.cat + "/" + self.name + "-" + self.version
		else:
			return self.cat + "/" + self.name + "-" + self.version + "-r%s" % self.revision

	@property
	def template_path(self):
		if self._template_path:
			return self._template_path
		tpath = os.path.join(self.source_tree, self.cat, self.name, "templates")
		return tpath

	async def record_manifest_lines(self):
		"""
		This method records literal Manifest output lines which will get written out later, because we may
		not have *all* the Manifest lines we need to write out until autogen is fully complete.
		"""
		if not len(self.artifacts):
			return

		key = self.output_pkgdir + "/Manifest"

		for artifact in self.iter_artifacts():
			success = await artifact.ensure_completed()
			if not success:
				raise BreezyError(f"Something prevented us from storing Manifest data for {key}.")
			pkgtools.model.manifest_lines[key].add(
				"DIST %s %s BLAKE2B %s SHA512 %s\n"
				% (artifact.final_name, artifact.size, artifact.hash("blake2b"), artifact.hash("sha512"))
			)

	def create_ebuild(self):
		if not self.template_text:
			template_file = os.path.join(self.template_path, self.template)
			try:
				with open(template_file, "r") as tempf:
					try:
						template = jinja2.Template(tempf.read())
					except jinja2.exceptions.TemplateError as te:
						raise BreezyError(f"Template error in {template_file}: {repr(te)}")
					except Exception as te:
						raise BreezyError(f"Unknown error processing {template_file}: {repr(te)}")
			except FileNotFoundError as e:
				log.error(f"Could not find template: {template_file}")
				raise BreezyError(f"Template file not found: {template_file}")
		else:
			template = jinja2.Template(self.template_text)
		# allow "src_uri" to be used inside all templates to print out official src_uri of all artifacts.
		template.globals.update({"src_uri": self.src_uri_with_use})
		template.globals.update({"src_uri_with_use": self.src_uri_with_use})
		with open(self.output_ebuild_path, "wb") as myf:
			try:
				myf.write(template.render(**self.template_args).encode("utf-8"))
			except Exception as te:
				raise BreezyError(f"Error rendering template: {repr(te)}")
		log.info("Created: " + os.path.relpath(self.output_ebuild_path))

	async def generate(self):
		"""
		This is an async method that does the actual creation of the ebuilds from templates. It also handles
		initialization of Artifacts (indirectly) and could result in some HTTP fetching. If you call
		``myebuild.push()``, this is the task that gets pushed onto the task queue to run in parallel.
		If you don't call push() on your BreezyBuild, then you could choose to call the generate() method
		directly instead. In that case it will run right away.
		"""
		if self.cat is None:
			raise BreezyError("Please set 'cat' to the category name of this ebuild.")
		if self.name is None:
			raise BreezyError("Please set 'name' to the package name of this ebuild.")
		await self.setup()
		try:
			self.create_ebuild()
		except Exception as e:
			raise BreezyError(f"Error creating ebuild {self.catpkg}: {str(e)}")
		await self.record_manifest_lines()
		return self


# vim: ts=4 sw=4 noet
