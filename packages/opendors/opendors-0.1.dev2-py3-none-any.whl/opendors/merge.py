# SPDX-FileCopyrightText: 2023 German Aerospace Center (DLR)
# SPDX-FileContributor: Stephan Druskat <stephan.druskat@dlr.de>
#
# SPDX-License-Identifier: MIT

from opendors.abc import WorkflowRule
from opendors.model import Corpus


########################################################################################################################
############################## Class
########################################################################################################################


class CorpusMerger(WorkflowRule):
    """
    TODO
    """

    def __init__(
        self,
        input_jsons: list[str],
        output_json: str,
        log_file: str,
        log_level: str = "DEBUG",
        indent: int = 0,
    ):
        super().__init__(__name__, log_file, log_level, indent)
        self.input_jsons = input_jsons
        self.output_json = output_json

    ##################################################
    ########## Methods
    ##################################################

    ##########
    ### Main method
    ##########
    def run(self) -> None:
        c = Corpus()
        total_inputs = len(self.input_jsons)
        for i_input, input_json in enumerate(self.input_jsons):
            self.log.debug(f"Merging input files {i_input + 1}/{total_inputs}.")
            c_in = self.read_corpus(input_json)
            for r_in in c_in.research_software:
                c.add_software(r_in)

        self.write_corpus(c, self.output_json)
