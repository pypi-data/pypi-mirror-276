from typing import List
from tonic_textual.classes.file_content.base_document import BaseDocument
from tonic_textual.classes.file_content.content import Content


class CsvDocument(BaseDocument):

    def __init__(self, client, json_def):
        super().__init__(client, json_def)
        self.content: List[List[Content]] = [
            [Content(client, f) for f in row] for row in json_def["content"]
        ]
        # self.header = json_def['header']  -gotta start sending from backend

    def get_cell_content(self, i: int, j: int) -> Content:
        return self.content[i][j]
