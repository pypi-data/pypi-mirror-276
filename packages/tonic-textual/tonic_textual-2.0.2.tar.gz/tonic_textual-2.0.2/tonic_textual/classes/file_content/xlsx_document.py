from typing import Dict, List

from tonic_textual.classes.file_content.base_document import BaseDocument
from tonic_textual.classes.file_content.content import Content
from tonic_textual.classes.httpclient import HttpClient


class XlsxDocument(BaseDocument):

    def __init__(self, client: HttpClient, json_def):
        super().__init__(client, json_def)
        d = {}
        for sheet_name in json_def["content"]:
            d[sheet_name]: List[List[Content]] = [  # type: ignore
                [Content(client, f) for f in row]
                for row in json_def["content"][sheet_name]
            ]
        self.content: Dict[str, List[List[Content]]] = d

    def get_cell_content(self, sheet_name: str, i: int, j: int) -> Content:
        return self.content[sheet_name][i][j]
