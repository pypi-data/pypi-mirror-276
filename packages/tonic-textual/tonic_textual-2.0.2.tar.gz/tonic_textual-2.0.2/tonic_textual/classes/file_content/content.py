from typing import List, Dict
from tonic_textual.enums.pii_state import PiiState
from tonic_textual.classes.httpclient import HttpClient
from tonic_textual.classes.common_api_responses.single_detection_result import (
    SingleDetectionResult,
)
from tonic_textual.generator_utils import (
    filter_entities_by_config,
    make_utf_compatible_entities,
)


class Content:
    def __init__(self, client: HttpClient, json_def: Dict):
        self.ner_results: List[SingleDetectionResult] = [
            SingleDetectionResult(
                s["pythonStart"], s["pythonEnd"], s["label"], s["text"], s["score"]
            )
            for s in json_def["nerResults"]
        ]
        self.content_hash = json_def["contentHash"]
        self.content = json_def["contentAsMarkdown"]
        self.client = client

    def get_markdown(self) -> str:
        return self.content

    def get_all_entities(self) -> List[SingleDetectionResult]:
        return self.ner_results

    def get_entities(self, entity_type_list: List[str]) -> List[SingleDetectionResult]:
        return [ent for ent in self.ner_results if ent["label"] in entity_type_list]

    def to_dict(self) -> Dict:
        return {
            "entity_spans": [x.to_dict() for x in self.ner_results],
            "content_as_markdown": self.content,
            "content_hash": self.content_hash,
        }

    def redact(
        self,
        generator_config: Dict[str, PiiState] = dict(),
        generator_default: PiiState = PiiState.Off,
    ) -> str:
        markdown = self.get_markdown()
        all_entities = self.get_all_entities()
        entities = filter_entities_by_config(
            all_entities, generator_config, generator_default
        )
        utf_compatible_entities = make_utf_compatible_entities(markdown, entities)
        response = self.client.http_post(
            "/api/redact/known_entities",
            data={"knownEntities": utf_compatible_entities, "text": markdown, "generatorConfig": generator_config, "generatorDefault": generator_default},
        )
        return response["redactedText"]

    def is_sensitive(self, sensitive_entity_types: List[str]):
        return len(self.get_entities(sensitive_entity_types)) > 0
