# SPDX-FileCopyrightText: 2023 German Aerospace Center (DLR)
# SPDX-FileContributor: Stephan Druskat <stephan.druskat@dlr.de>
#
# SPDX-License-Identifier: MIT
import re
from copy import deepcopy
from typing import Optional
from urllib.parse import urlparse
from pathlib import Path
from collections import namedtuple

from pydantic import Field
from pydantic.dataclasses import dataclass

from opendors.abc import WorkflowRule
from opendors.model import (
    Platform,
    VCS,
    VersionType,
    MentionedVersion,
    SourceCodeRepository,
    DeterminationSource,
)

_Parse = namedtuple("Parse", "scheme, subdomain, domain, tld, path1, path2")
_NetlocParse = namedtuple("NetlocParse", "subdomain, domain, tld")


_ALPHA_NUM_DASH = r"[a-zA-Z0-9_-]+"
_ALPHA_NUM_DASH_PERIOD = r"[a-zA-Z0-9\._-]+"
_NO_GIT_SUFFIX = r"(?<!\.git)"

_DOMAIN_GITHUB = "github"
_DOMAIN_GITHUBUSERCONTENT = "githubusercontent"
_DOMAIN_GITLAB = "gitlab"
_DOMAIN_BITBUCKET = "bitbucket"
_DOMAIN_SOURCEFORGE = "sourceforge"


@dataclass
class ProjectData:
    canonical_url: str
    invalid_subdomains: list[str] = Field(default=[])
    alias_domains: list[str] = Field(default=[])
    canonical_domain: str = None
    tld: str = None
    valid_regex: str = None
    platform: Platform = None
    vcs: Optional[VCS] = None


@dataclass
class GithubProjectData(ProjectData):
    invalid_subdomains: list[str] = Field(
        default=[
            "gist",
            "cloud",
            "octoverse",
            "archiveprogram",
            "guides",
            "pages",
            "docs",
        ]
    )
    alias_domains: list[str] = Field(
        default=[_DOMAIN_GITHUB, _DOMAIN_GITHUBUSERCONTENT]
    )
    canonical_domain: str = _DOMAIN_GITHUB
    tld: str = "com"
    valid_regex: str = (
        r"^https://github.com/"
        + _ALPHA_NUM_DASH
        + r"/"
        + _ALPHA_NUM_DASH_PERIOD
        + _NO_GIT_SUFFIX
        + r"$"
    )
    platform: Platform = Platform.GITHUB_COM
    vcs: Optional[VCS] = VCS.git


@dataclass
class SourceforgeProjectData(ProjectData):
    invalid_subdomains: list[str] = Field(
        default=[
            "lists",
            "users",
        ]
    )
    canonical_domain: str = _DOMAIN_SOURCEFORGE
    tld: str = "net"
    valid_regex: str = (
        r"https://sourceforge.net/projects/"
        + _ALPHA_NUM_DASH_PERIOD
        + _NO_GIT_SUFFIX
        + r"$"
    )
    platform: Platform = Platform.SOURCEFORGE_NET


@dataclass
class GitlabProjectData(ProjectData):
    canonical_domain: str = _DOMAIN_GITLAB
    tld: str = "com"
    valid_regex: str = (
        r"^https://gitlab.com/"
        + _ALPHA_NUM_DASH
        + r"/"
        + _ALPHA_NUM_DASH_PERIOD
        + _NO_GIT_SUFFIX
        + r"$"
    )
    platform: Platform = Platform.GITLAB_COM
    vcs: Optional[VCS] = VCS.git


@dataclass
class BitbucketProjectData(ProjectData):
    canonical_domain: str = _DOMAIN_BITBUCKET
    tld: str = "org"
    valid_regex: str = (
        r"^https://bitbucket.org/"
        + _ALPHA_NUM_DASH
        + r"/"
        + _ALPHA_NUM_DASH_PERIOD
        + _NO_GIT_SUFFIX
        + r"$"
    )
    platform: Platform = Platform.BITBUCKET_ORG
    vcs: Optional[VCS] = VCS.git


_VALID_DOMAINS = [
    _DOMAIN_GITHUB,
    _DOMAIN_GITHUBUSERCONTENT,
    _DOMAIN_GITLAB,
    _DOMAIN_BITBUCKET,
    _DOMAIN_SOURCEFORGE,
]


def _parse_netloc(netloc: str) -> _NetlocParse | None:
    """
    Parses the netloc part of a urlparse'd URL into a three-item named tuple
    with parts subdomain, domain and tld, where only subdomain can be empty,
    and only specific single-element TLDs are allowed.

    :param netloc: The netloc string to parse
    :return: A namedtuple with the parse result including subdomain, domain and top-level domain
    """
    parts = netloc.split(".")
    length = len(parts)
    if length in [2, 3] and parts[-1] in ["com", "org", "io", "net"]:
        return _NetlocParse(parts[-3] if length == 3 else "", parts[-2], parts[-1])


def _get_path_parts(path: str) -> tuple[str, ...] | None:
    """
    Gets the first two path elements for a given path string.
    Returns only the first path element if there is only one,
    and returns None if the path cannot be parsed.

    :param path: The path string to parse
    :return: A tuple containing the first path element and the second path element
    """
    two_paths = Path(path).parts[1:3]
    if two_paths:
        return (
            two_paths[0],
            two_paths[1] if len(two_paths) == 2 else "",
        )


def _handle_sourceforge_url(url: str) -> str:
    """
    Handles some specific cases for Sourceforge URLs.

    :param url: The Sourceforge URL to handle
    :return: The adapted Sourceforge URL
    """
    if "/p/" in url:
        return url.replace("/p/", "/projects/")
    elif "/apps/mediawiki/" in url:
        return url.replace("/apps/mediawiki/", "/projects/")
    else:
        return url


def _paths_end_insensibly(paths):
    """
    Returns whether paths end in characters that may not be sensible but may be legal.

    :param paths: The paths to check
    :return: Whether any of the paths end in something insensible
    """
    if paths:
        insensible_characters = {","}
        for path in paths:
            if path and path[-1] in insensible_characters:
                return True
    return False


def parse_url(url: str) -> _Parse | None:
    """
    Parses a URL into parts and returns a namedtuple with the following parts.

    Note that this only works in the context of URLs with single-element effective TLDs!

    Parts:
    - 0: scheme (always returns "https")
    - 1: subdomain (subdomain or empty string)
    - 2: domain
    - 3: tld (only single element TLDs)
    - 4: first two path elements (e.g., '/path1/path2/'; returns empty string when path is "/",
    and only ever returns the first two path elements without any leading or trailing slashes)

    :param url: The URLs to parse
    :return: A namedtuple with the parse results, or None if the parse failed
    """

    if "sourceforge.net" in url:
        url = _handle_sourceforge_url(url)
    try:
        url_parts = urlparse(url, scheme="https")
    except ValueError:
        return None
    netloc_parts = _parse_netloc(url_parts.netloc)
    if netloc_parts:
        if url_parts.path and url_parts.path != "/":
            paths = _get_path_parts(url_parts.path)
            if _paths_end_insensibly(paths):
                return None
            if not paths:
                paths = ("", "")
        else:
            paths = ("", "")
        return _Parse(
            "https",
            netloc_parts.subdomain,
            netloc_parts.domain,
            netloc_parts.tld,
            paths[0],
            paths[1],
        )


def _ignore_url(parse: _Parse) -> bool:
    """
    Returns True for URLs that 1) are not validly patterned repository URLs,
    and 2) not URLs with a known pattern that can be converted to a valid repository URL,
    and 3) known subdomain URLs that are not user subdomains.

    # Known subdomain URLs to ignore

    - gist.github.com
    - cloud.github.com
    - octoverse.github.com
    - archiveprogram.github.com
    - guides.github.com
    - pages.github.com
    - docs.github.com
    - lists.sourceforge.net
    - users.sourceforge.net

    # Known paths to ignore
    - sourceforge.net/tracker

    :param parse: The parse object for the URL to check
    :return: Whether the URL should be ignored
    """
    # All interesting URLs apart from SourceForge need at least one path to not be ignored
    if parse.domain != _DOMAIN_SOURCEFORGE and not parse.path1:
        return True
    # Ignore user URLs
    if not parse.subdomain and not parse.path2:
        return True
    # Ignore platform-specific stuff
    if parse.domain == _DOMAIN_GITHUB:
        # Invalid subdomains
        if parse.subdomain in GithubProjectData.invalid_subdomains:
            return True
    elif parse.domain == _DOMAIN_GITLAB:
        return False
    elif parse.domain == _DOMAIN_SOURCEFORGE:
        # Invalid subdomains
        if parse.subdomain in SourceforgeProjectData.invalid_subdomains:
            return True
        if not parse.subdomain and not parse.path1:
            return True
        if parse.path1 == "tracker":
            return True
    # GitHub raw pages need two path segments
    elif parse.domain == _DOMAIN_GITHUBUSERCONTENT:
        if not parse.path2:
            return True
    elif parse.domain == _DOMAIN_BITBUCKET:
        return False
    else:
        # When this is called, domain validity should already have been checked.
        raise ValueError("Parse domain is not valid.")


def _get_paths(parse: _Parse) -> tuple[str, str]:
    """
    Known URL patterns that can be transformed into valid repository URLs

    - https://(user).github.io/(repo) -> https://github.com/(user)/(repo)
    - https://(user).github.com/(repo) -> https://github.com/(user)/(repo)
    - https://raw.githubusercontent.com/(user)/(repo)
    - https://(user).gitlab.io/(repo) -> https://gitlab.com/(user)/(repo)
    - https://(group).gitlab.io/(subgroup/)+ -> https://gitlab.com/(group)/(subgroup)+
    - https://(repo).sourceforge.io/ -> https://sourceforge.net/projects/(repo)

    :param parse: The parse result for the URL for which to retrieve the paths
    :return: The transformed paths for the given URL
    """
    if parse.subdomain:
        if parse.domain == SourceforgeProjectData.canonical_domain:
            path1 = "projects"
            path2 = parse.subdomain
        elif parse.domain == _DOMAIN_GITHUBUSERCONTENT:
            path1 = parse.path1
            path2 = parse.path2
        else:
            path1 = parse.subdomain
            path2 = parse.path1
    else:
        path1 = parse.path1
        path2 = parse.path2

    return path1, path2


def _project_data_from(parse: _Parse) -> ProjectData | None:
    """
    Transform a given parse result into a repository URL string
    with the pattern https://<domain>.<tld>/<path1>/<path2> and
    return it if it is canonical, else return None.

    :param parse: The parse result for the URL to transform
    :return: The canonical transformed URL or None
    """
    project_data = DOMAIN_DATA[parse.domain]
    path1, path2 = _get_paths(parse)
    path2 = path2.removesuffix(".git")

    transformed_url = (
        f"https://{project_data.canonical_domain}.{project_data.tld}/{path1}/{path2}"
    )

    if re.match(project_data.valid_regex, transformed_url):
        return project_data(canonical_url=transformed_url)
    else:
        return None


DOMAIN_DATA = {
    _DOMAIN_GITHUB: GithubProjectData,
    _DOMAIN_GITHUBUSERCONTENT: GithubProjectData,
    _DOMAIN_GITLAB: GitlabProjectData,
    _DOMAIN_BITBUCKET: BitbucketProjectData,
    _DOMAIN_SOURCEFORGE: SourceforgeProjectData,
}


def _canonical_data_from(url: str, domain: str):
    """
    TODO
    :param url:
    :param domain:
    :return:
    """
    klass = DOMAIN_DATA[domain]
    return klass(canonical_url=url)


def canonical_project_data(url: str) -> ProjectData | None:
    """
    If possible, returns canonical project data including a canonical URL for a given URL, else returns None.

    Valid repository URL patterns for all platforms that are in the scope of this package are

    - https://github.com/(user)/(repo)
    - https://gitlab.com/(user)/(repo)
    - https://sourceforge.net/projects/(repo)
    - https://bitbucket.org/(user)/(repo)

    Note that currently, GitLab subgroup URLs cannot be canonicalized.

    Note also that this function may return data with canonical URLs that don't resolve.

    :param url: The URL string to attempt to make canonical
    :return: The canonical project data for the given URL string, or None
    """
    parse = parse_url(url)
    if parse:
        if parse.domain not in _VALID_DOMAINS:
            return None
        # Return early if URL is already canonical
        if re.match(DOMAIN_DATA[parse.domain].valid_regex, url):
            return _canonical_data_from(url, parse.domain)
        else:
            if _ignore_url(parse):
                return None
            return _project_data_from(parse)


def get_sourceforge_api_url(url: str) -> str:
    """
    Transforms a valid canonical Sourceforge project URL (of schema https://sourceforge.net/projects/<project>)
    into a Sourceforge REST URL (of schema https://sourceforge.net/rest/p/<project>).

    :raise ValueError if the input URL is not a valid Sourceforge project URL:
    :param url: A canonical Sourceforge project URL
    :return: A Sourceforge REST URL
    """
    url = str(url)
    if re.match(SourceforgeProjectData.valid_regex, url):
        return f"https://sourceforge.net/rest/p/{url.split('/')[-1]}"
    else:
        raise ValueError(f"URL {url} is not a valid Sourceforge project URL.")


class URLVersionRetriever(WorkflowRule):
    """
    Attempts to identify the mentioned version for all mentions of a list of software based on the given original
    mentioned URLs.

    Requirements to run this rule:
        - All software in input_json must have values for 'platform' and 'vcs' for all repositories in 'repositories'.
    """

    def __init__(
        self,
        input_json: str,
        output_json: str,
        log_file: str,
        log_level: str = "DEBUG",
        indent: int = 0,
    ):
        super().__init__(__name__, log_file, log_level, indent)
        self.input_json = input_json
        self.output_json = output_json

    ##################################################
    ########## Methods
    ##################################################

    # ########
    # # Main method
    # ########
    def run(self) -> None:
        corpus = self.read_corpus(self.input_json)
        for software in corpus.research_software:
            for mention in software.mentions:
                mention.version = get_version_from_repository_urls(
                    software.platform,
                    mention.version,
                    software.repositories,
                    mention.mentioning_urls,
                )
        self.write_corpus(corpus, self.output_json)


def get_version_from_repository_urls(
    platform: Platform,
    orig_version: MentionedVersion,
    repositories: list[SourceCodeRepository],
    orig_urls: set[str],
) -> MentionedVersion:
    """
    Attempts to extract version information from a mention's originally mentioned URLs.

    This method is opinionated in that for Sourceforge projects which can have more than one repository,
    it returns the first encountered git repository. It also returns the "best" encountered version information,
    where tags > commit > branch > path. (See opendors.model.VersionType for more information about types).

    :param platform: The platform the software source code is hosted on
    :param orig_version: The existing version instance of the mention
    :param repositories: The list of repositories of that software
    :param orig_urls: The originally mentioned URLs of a mention
    :return: An instance of MentionedVersion, optionally enriched with version information
    """
    if not orig_version:
        orig_version = MentionedVersion()

    # Return early if we already have a best version
    if orig_version.type == VersionType.TAG:
        return orig_version

    type_weights = {
        VersionType.TAG: 4,
        VersionType.REVISION: 3,
        VersionType.BRANCH: 2,
        VersionType.PATH: 1,
        None: 0,
    }
    WeightedVer = namedtuple("WeightedVersion", ["version", "weight"])
    best_weighted_ver = WeightedVer(orig_version, type_weights[orig_version.type])
    git_repo = None
    svn_repo = None

    # Get repo to work on, where git repos are better than svn repos
    for repo in repositories:
        if repo.vcs == VCS.git:
            # Use the first encountered git repository
            git_repo = repo
            break
        elif repo.vcs == VCS.svn:
            svn_repo = repo
    preferred_repo = git_repo if git_repo else svn_repo
    if not preferred_repo:
        return orig_version

    # Go through all original URLs and determine best for versioning, then return that
    for orig_url in orig_urls:
        version_copy = deepcopy(orig_version)
        temp_ver = _get_version_from_url(
            version_copy, orig_url, platform, preferred_repo.vcs
        )
        temp_weight = type_weights[temp_ver.type]
        best_weighted_ver = (
            WeightedVer(temp_ver, temp_weight)
            if not best_weighted_ver.weight >= temp_weight
            else best_weighted_ver
        )
    return best_weighted_ver.version


def _handle_sourceforge(
    version: MentionedVersion, path: str, repo_url: str, vcs: VCS
) -> MentionedVersion:
    """
    TODO

    :param version:
    :param path: URL path that has been stripped of any final '/'
    :param repo_url:
    :param vcs:
    :return:
    """
    if vcs == VCS.svn:
        if m := re.search(r"/(svn|code)/(\d+)(/tree/?)?$", path):
            version.identification_url = repo_url
            version.type = VersionType.REVISION
            last_segment = m.group(2).lstrip("/").rstrip("/")
            version.version = last_segment
            version.determined_from = DeterminationSource.URL
        elif m := re.search(r"/code/.+", path):
            version.identification_url = repo_url
            version.type = VersionType.PATH
            # Strip "/code/" prefix
            last_segment = m.group(0)[6:].lstrip("/").rstrip("/")
            version.version = last_segment
            version.determined_from = DeterminationSource.URL

    elif vcs == VCS.git:
        version.identification_url = repo_url
        version.type = VersionType.PATH

        if "/ci/" in path:
            relevant_path = path.split("/ci/")[-1]
            if re.search("/tree($|/)", relevant_path):
                version.type = VersionType.PATH
                version.version = relevant_path
                version.determined_from = DeterminationSource.URL
            elif "/" not in relevant_path:
                if re.match(r"[0-9a-f]{40}", relevant_path):
                    version.type = VersionType.REVISION
                    version.version = relevant_path
                    version.determined_from = DeterminationSource.URL

    return version


def _handle_git_platforms(
    version: MentionedVersion, path: str, repo_url: str
) -> MentionedVersion:
    """
    TODO

    :param version:
    :param path: URL path that has been stripped of any final '/'
    :param repo_url:
    :return:
    """
    path_type_map = {
        r"/(tree|blob)/": VersionType.PATH,
        r"bitbucket.org/.+/.+/src/": VersionType.PATH,
        r"/(tags?|releases|commits/tag)/": VersionType.TAG,
        r"/commits?/(?!tag/)": VersionType.REVISION,
        r"bitbucket.org/.+/.+/branch/.+": VersionType.BRANCH,
    }
    for key, value in path_type_map.items():
        if re.search(key, repo_url):
            version.identification_url = repo_url
            version.type = value
            if not value == VersionType.PATH:
                last_segment = path.split("/")[-1]
            else:
                # key may include domain + tld, path never does: strip key, retain last segment for regex matching
                key = r"/" + key.rstrip("/").split("/")[-1] + r"/"
                last_segment = (
                    re.search(key + r".*$", path).group(0).lstrip("/").rstrip("/")
                )
            version.version = last_segment
            version.determined_from = DeterminationSource.URL
    return version


def _get_version_from_url(
    version: MentionedVersion, repo_url: str, platform: Platform, vcs: VCS
) -> MentionedVersion:
    parse = urlparse(repo_url)
    path = parse.path.rstrip("/")

    if not version:
        version = MentionedVersion()

    if platform in (Platform.GITHUB_COM, Platform.GITLAB_COM, Platform.BITBUCKET_ORG):
        return _handle_git_platforms(version, path, repo_url)
    elif platform == Platform.SOURCEFORGE_NET:
        return _handle_sourceforge(version, path, repo_url, vcs)
    return version
