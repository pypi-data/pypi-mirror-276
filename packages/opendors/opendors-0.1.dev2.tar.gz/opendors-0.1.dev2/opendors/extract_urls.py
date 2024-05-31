# SPDX-FileCopyrightText: 2023 German Aerospace Center (DLR)
# SPDX-FileContributor: Stephan Druskat <stephan.druskat@dlr.de>
#
# SPDX-License-Identifier: MIT

import json
import re

from jsonpath_ng import parse

from opendors.abc import WorkflowRule
from opendors.model import (
    IdType,
    MetadataSource,
    Corpus,
    Mention,
    Platform,
    RepoValidatedResearchSoftware,
)
from opendors.urls import canonical_project_data


# ######################################################################################################################
# ############################ Class
# ######################################################################################################################


class ExtractURLsRetriever(WorkflowRule):
    def __init__(
        self,
        data_source: MetadataSource,
        input_json: str,
        output_jsons: list[str],
        log_file: str,
        log_level: str,
        indent: int = 0,
    ):
        """
        A retriever for publication metadata from the PMC and ArXiv subsets of the Extract URLs dataset.

        :param input_json: The input data JSON file
        :param FIXME platform_file: A dict mapping platform names to output file names
        :param log_file: The path string to the log file that logging output should be written to
        """
        super().__init__(f"{__name__}.{data_source.value}", log_file, log_level, indent)
        self.data_source = data_source
        self.input_json = input_json
        self.output_jsons = output_jsons

    def _extract_id(self, pdf_file: str) -> str:
        """
        Extracts the data source ID from a PDF file path in the Extract-URLs data.

        :param pdf_file: The pdf file path string to extract the ID from
        :return: the data source ID
        """
        pdf_file = pdf_file.strip("'").strip('"')
        pattern = id_candidate = None
        if self.data_source == MetadataSource.EXTRACT_URLS_ARXIV:
            id_candidate = pdf_file.replace(".pdf", "")
            pattern = r"^\d+\.\d+v\d+$"
        elif self.data_source == MetadataSource.EXTRACT_URLS_PMC:
            split_name = pdf_file.split(".")
            id_candidate = split_name[-2].replace("PMC", "")
            pattern = r"^\d+$"
        try:
            assert re.match(pattern, id_candidate)
        except AssertionError as ae:
            message = (
                f"Could not find data source id in {pdf_file}'s id candidate {id_candidate} "
                f"with pattern {pattern}."
            )
            ae.args += (message,)
            self.log.error(message)
            raise ae
        return id_candidate

    def run(self) -> None:
        """
        Extracts repository URLs from Extract-URLs parsed data JSON files,
        checks whether URLs can be transformed into canonical repository URLs,
        and if so, adds them to a corpus of repositories of canonical URLs
        and their mentions in the subset of the dataset.
        The corpus is then written into a JSON file.
        """
        platform_corpus = {
            Platform.GITHUB_COM: Corpus(),
            Platform.GITLAB_COM: Corpus(),
            Platform.BITBUCKET_ORG: Corpus(),
            Platform.SOURCEFORGE_NET: Corpus(),
        }
        with open(self.input_json, "r") as json_in:
            data = json.load(json_in)
        expr = "$.*.files.*.url_count"
        jsonpath_expression = parse(expr)
        id_type = (
            IdType.ARXIV
            if self.data_source == MetadataSource.EXTRACT_URLS_ARXIV
            else IdType.PMC
        )

        for datum in jsonpath_expression.find(data):
            if int(datum.value) > 0:
                all_urls = datum.context.value["all_urls"]
                for url in all_urls:
                    if canon_project_data := canonical_project_data(url):
                        # Get data source ID for the paper and map it.
                        # The match can only have exactly one context, and that is the parent field,
                        # i.e., the PDF name, which contains the data source ID.
                        pdf_file = str(datum.context.path)
                        data_source_id = self._extract_id(pdf_file)
                        canon_url = canon_project_data.canonical_url
                        self.log.debug(
                            f"Mapping data source ID {data_source_id} to URL {canon_url}."
                        )
                        m = Mention(
                            metadata_source=self.data_source,
                            id=data_source_id,
                            id_type=id_type,
                            mentioning_urls={url},
                        )
                        platform = canon_project_data.platform
                        s = RepoValidatedResearchSoftware(
                            canonical_url=canon_url, mentions=[m], platform=platform
                        )
                        platform_corpus[platform].add_software(s)
                    else:
                        self.log.info(f"Could not get canonical project data for {url}")

        for platform, corpus in platform_corpus.items():
            out_file = self._get_out_file_for_platform(platform)
            if out_file:
                self.write_corpus(corpus, out_file)
            else:
                self.log.error(
                    f"Output file for platform {platform} is not in {self.output_jsons}."
                )

    def _get_out_file_for_platform(self, platform: str) -> str:
        """
        TODO

        :param platform:
        :return:
        """
        for out_file in self.output_jsons:
            if platform.split(".")[0] in out_file:
                return out_file
