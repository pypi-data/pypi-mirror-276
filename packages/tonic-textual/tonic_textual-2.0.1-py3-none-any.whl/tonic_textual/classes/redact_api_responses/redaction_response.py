from typing import List

from tonic_textual.classes.common_api_responses.single_detection_result import (
    SingleDetectionResult,
)


class RedactionResponse(dict):
    def __init__(
        self,
        original_text: str,
        redacted_text: str,
        usage: int,
        de_identify_results: List[SingleDetectionResult],
    ):
        self.original_text = original_text
        self.redacted_text = redacted_text
        self.usage = usage
        self.de_identify_results = de_identify_results
        dict.__init__(
            self,
            original_text=original_text,
            redacted_text=redacted_text,
            usage=usage,
            de_identify_results=de_identify_results,
        )

    def describe(self):
        result = f"{self.redacted_text}\n"
        for x in self.de_identify_results:
            result += f"{x.describe()}\n"
        return result

    def get_usage(self):
        return self.usage
