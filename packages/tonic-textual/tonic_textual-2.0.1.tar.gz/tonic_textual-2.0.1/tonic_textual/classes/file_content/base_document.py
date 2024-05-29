from typing import Dict, List
from tonic_textual.classes.common_api_responses.single_detection_result import (
    SingleDetectionResult,
)
from tonic_textual.classes.httpclient import HttpClient


class BaseDocument:
    def __init__(self, client: HttpClient, json_def: Dict):
        self.client = client
        self._json_def = json_def
        self.markdown = json_def["markdown"]
        self.entities: List[SingleDetectionResult] = [
            SingleDetectionResult(
                s["pythonStart"], s["pythonEnd"], s["label"], s["text"], s["score"]
            )
            for s in json_def["entities"]
        ]

    def get_markdown(self):
        return self.markdown

    def get_all_entities(self):
        return self.entities

    def to_dict(self):
        return self._json_def
