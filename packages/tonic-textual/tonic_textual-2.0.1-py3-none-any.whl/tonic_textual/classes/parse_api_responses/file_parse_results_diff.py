from enum import Enum

from tonic_textual.classes.parse_api_responses.file_parse_result import FileParseResult


class FileParseDiffAction(Enum):
    Added = 1
    Deleted = 2
    Modified = 3


class FileParseResultsDiff(object):
    def __init__(self, status: FileParseDiffAction, file: FileParseResult):
        self.status = status
        self.file = file

    def describe(self):
        return f"{self.status}: {self.file.parsed_file_path}"

    def deconstruct(self):
        return self.status, self.file
