from datetime import datetime

from tonic_textual.classes.file_parse_result_diff_enumerator import (
    FileParseResultsDiffEnumerator,
)
from tonic_textual.classes.httpclient import HttpClient


class PipelineRun(object):
    def __init__(self, id: str, status: str, end_time: datetime, client: HttpClient):
        self.id = id
        self.status = status
        self.end_time = end_time
        self.client = client

    def get_delta(self, other: "PipelineRun") -> FileParseResultsDiffEnumerator:
        if isinstance(other, PipelineRun):
            if self.status != "Completed" or other.status != "Completed":
                raise Exception("Both runs must be successful to compare files")
            return FileParseResultsDiffEnumerator(self.id, other.id, self.client)
        else:
            raise TypeError("Expected `other` to be a PipelineRun object")
