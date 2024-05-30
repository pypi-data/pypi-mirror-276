from typing import List

import requests

from tonic_textual.classes.file_parse_result_diff_enumerator import (
    FileParseResultsDiffEnumerator,
)
from tonic_textual.classes.httpclient import HttpClient
from tonic_textual.classes.pipeline_file_enumerator import PipelineFileEnumerator
from tonic_textual.classes.pipeline_run import PipelineRun


class Pipeline:
    """Class to represent and provide access to a Tonic Textual pipeline.

    Parameters
    ----------
    name: str
        Pipeline name.

    id: str
        Pipeline identifier.

    client: HttpClient
        The HTTP client to use.
    """

    def __init__(self, name: str, id: str, client: HttpClient):
        self.id = id
        self.name = name
        self.client = client

    def describe(self) -> str:
        """Print the name and id of the pipeline."""
        description = "--------------------------------------------------------\n"
        description += f"Name: {self.name}\n"
        description += f"ID: {self.id}\n"
        description += "--------------------------------------------------------\n"
        return description

    def get_runs(self) -> List[PipelineRun]:
        """Get the runs for the pipeline.

        Returns
        -------
        List[PipelineRun]
            A list of PipelineRun objects.
        """
        with requests.Session() as session:
            response = self.client.http_get(
                f"/api/parsejob/{self.id}/jobs", session=session
            )
            runs: List[PipelineRun] = []
            for run in response:
                runs.append(
                    PipelineRun(run["id"], run["status"], run["endTime"], self.client)
                )
            return runs

    def enumerate_files(self, lazy_load_content=True) -> PipelineFileEnumerator:
        """Enumerate the files in the pipeline.

        Parameters
        ----------
        lazy_load_content: bool
            Whether to lazily load the content of the files. Default is True.

        Returns
        -------
        PipelineFileEnumerator
            An enumerator for the files in the pipeline.
        """
        runs = self.get_runs()
        successful_runs = filter(lambda r: r.status == "Completed", runs)
        sorted_finished_runs = sorted(
            successful_runs, key=lambda r: r.end_time, reverse=True
        )

        if len(sorted_finished_runs) == 0:
            return PipelineFileEnumerator(
                "", self.client, lazy_load_content=lazy_load_content
            )

        job_id = sorted_finished_runs[0].id
        return PipelineFileEnumerator(
            job_id, self.client, lazy_load_content=lazy_load_content
        )

    def get_delta(
        self, pipeline_run1: PipelineRun, pipeline_run2: PipelineRun
    ) -> FileParseResultsDiffEnumerator:
        return FileParseResultsDiffEnumerator(
            pipeline_run1.id, pipeline_run2.id, self.client
        )
