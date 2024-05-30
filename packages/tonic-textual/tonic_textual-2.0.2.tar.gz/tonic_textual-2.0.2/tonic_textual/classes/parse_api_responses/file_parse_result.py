from datetime import datetime
from typing import Dict, List, Union

import requests

from tonic_textual.classes.common_api_responses.base_file import BaseFile
from tonic_textual.classes.common_api_responses.single_detection_result import (
    SingleDetectionResult,
)
from tonic_textual.classes.enums.file_type import FileTypeEnum
from tonic_textual.classes.file_content.csv_document import CsvDocument
from tonic_textual.classes.file_content.docx_document import DocxDocument
from tonic_textual.classes.file_content.pdf_document import PdfDocument
from tonic_textual.classes.file_content.raw_document import RawDocument
from tonic_textual.classes.file_content.xlsx_document import XlsxDocument
from tonic_textual.classes.httpclient import HttpClient
from tonic_textual.enums.pii_state import PiiState
from tonic_textual.markdown_utils import split_markdown
from tonic_textual.generator_utils import (
    filter_entities_by_config,
    make_utf_compatible_entities,
)


class FileParseResult(object):
    """A class representing the result of a parsed file.

    Parameters
    ----------
    response: Dict
        The response from the API.

    client: HttpClient
        The HTTP client to use.

    lazy_load_content: bool
        Whether to lazy load the content of the file. Default is False.
    """

    def __init__(self, response: Dict, client: HttpClient, lazy_load_content=False):
        self.id: str = response["id"]
        self.file: BaseFile = BaseFile(response["file"])
        self.file_parse_job_id: str = response["fileParseJobId"]
        self.parsed_file_path: str = response["parsedFilePath"]
        self.created_date: datetime = response["createdDate"]
        self.last_modified_date: datetime = response["lastModifiedDate"]
        self.__is_content_retrieved = False
        self.content: Union[
            RawDocument, CsvDocument, DocxDocument, XlsxDocument, PdfDocument
        ]
        self.client = client
        if not lazy_load_content:
            self.__get_content()
        self.metadata = {}

    def __get_content(self):
        if not self.__is_content_retrieved:
            with requests.Session() as session:
                response = self.client.http_get(
                    f"/api/parsejob/files/{self.id}/content", session=session
                )

                if self.file.fileType == FileTypeEnum.csv:
                    self.content = CsvDocument(self.client, response)
                elif self.file.fileType == FileTypeEnum.raw:
                    self.content = RawDocument(self.client, response)
                elif self.file.fileType == FileTypeEnum.xlsx:
                    self.content = XlsxDocument(self.client, response)
                elif self.file.fileType == FileTypeEnum.docX:
                    self.content = DocxDocument(self.client, response)
                elif (
                    self.file.fileType == FileTypeEnum.pdf
                    or self.file.fileType == FileTypeEnum.png
                    or self.file.fileType == FileTypeEnum.jpg
                    or self.file.fileType == FileTypeEnum.tif
                ):
                    self.content = PdfDocument(self.client, response)
                else:
                    raise Exception("Unknown file type " + self.file.fileType)

            self.__is_content_retrieved = True

    def get_markdown(
        self,
        generator_config: Dict[str, PiiState] = dict(),
        generator_default: PiiState = PiiState.Off,
    ) -> str:
        """Returns file in markdown format, redacted or synthesized based on config.

        Parameters
        ----------
        generator_config: Dict[str, PiiState]
            A dictionary of sensitive data entities. For each entity, indicates whether
            to redact, synthesize, or ignore it.
            Values must be one of "Redaction", "Synthesis", or "Off".

        generator_default: PiiState = PiiState.Redaction
            The default redaction used for all types not specified in generator_config.
            Values must be one of "Redaction", "Synthesis", or "Off".

        Returns
        -------
        str
            The file in markdown format, redacted or synthesized based on
            generator_config and generator_default.
        """
        self.__get_content()
        rawtext = self.content.get_markdown()
        filtered_entities = filter_entities_by_config(
            self.content.get_all_entities(),
            generator_config,
            generator_default,
        )
        if len(filtered_entities) == 0:
            return rawtext
        utf_compatible_filtered_entities = make_utf_compatible_entities(
            rawtext, filtered_entities
        )
        response = self.client.http_post(
            "/api/redact/known_entities",
            data={"knownEntities": utf_compatible_filtered_entities, "text": rawtext, "generatorConfig": generator_config, "generatorDefault": generator_default},
        )
        return response["redactedText"]

    def describe(self):
        """Print the parsed file path."""
        return f"{self.parsed_file_path}"

    def get_all_entities(self) -> List[SingleDetectionResult]:
        """Returns a list of all the detected entities in the file.

        Returns
        -------
        List[SingleDetectionResult]
            A list of detected entities in the file.
        """
        self.__get_content()
        return self.content.get_all_entities()

    def get_entities(
        self,
        generator_config: Dict[str, PiiState] = dict(),
        generator_default: PiiState = PiiState.Redaction,
        allow_overlap: bool = False,
    ) -> List[SingleDetectionResult]:
        """Returns a list of entities in the document. The entities are filtered by the
        generator_default configuration.

        Parameters
        ----------
        entities: List[Dict]
            A list of entities to redact.

        generator_default: PiiState
            The default redaction used for all types not specified in generator_config.
            Values must be one of "Redaction", "Synthesis", or "Off".

        generator_config: Dict[str, PiiState]
            A dictionary of sensitive data entities. For each entity, indicates whether
            to redact, synthesize, or ignore it.
            Values must be one of "Redaction", "Synthesis", or "Off".

        Returns
        -------
        List[SingleDetectionResult]
            A list of the detected entities. Each item in list contains the entity type,
            source start index, source end index, the entity text, and replacement text.
        """
        self.__get_content()
        all_entities = self.content.get_all_entities()
        rawtext = self.content.get_markdown()
        filtered_entities = filter_entities_by_config(
            all_entities, generator_config, generator_default
        )
        if allow_overlap:
            return filtered_entities
        utf_compatible_filtered_entities = make_utf_compatible_entities(
            rawtext, filtered_entities
        )
        response = self.client.http_post(
            "/api/redact/known_entities",
            data={"knownEntities": utf_compatible_filtered_entities},
        )
        return [
            SingleDetectionResult(
                x["start"], x["end"], x["label"], x["text"], x["score"]
            )
            for x in list(response["deIdentifyResults"])
        ]

    def is_sensitive(
        self, sensitive_entity_types: List[str], start: int = 0, end: int = -1
    ) -> bool:
        """Returns True if the element contains sensitive data, False otherwise.
        Arguments:
            sensitive_entity_types: List[str]
                A list of sensitive entity types to check for.
            start: int = 0
                The start index to check for sensitive data.
            end: int = -1
                The end index to check for sensitive data.
        Returns:
            bool
                True if the element contains sensitive data, False otherwise.
        """
        all_entities = self.get_entities()
        entities = [
            ent for ent in all_entities if ent["label"] in sensitive_entity_types
        ]
        filtered_entities = self._find_intersecting_entites(start, end, entities)
        return len(filtered_entities) > 0

    @staticmethod
    def _make_entity_metadata(entity_list: List[Dict]) -> Dict[str, List[str]]:
        """Flattens a list of entity spans into a dictionary of entities per type"""
        entity_dict = {}
        for entity in entity_list:
            entity_type = entity["label"]
            entity_list = entity_dict.get(entity_type, [])
            entity_text = entity["text"]
            if entity_text not in entity_list:
                entity_list.append(entity_text)
            entity_dict[entity_type] = entity_list
        return entity_dict

    @staticmethod
    def _find_intersecting_entites(
        start: int, end: int, entities: List[SingleDetectionResult]
    ) -> List[Dict]:
        """Finds entities that intersect with the given start and end gindices
        Args:
            start: int
                The start index to check for intersecting entities.
            end: int
                The end index to check for intersecting entities. If -1, will return all
                entities that occur after start
        Returns:
            List[Dict]
                A list of entities that intersect with the given start and end indices
        """
        intersecting_entities = []
        for entity in entities:
            entity_start = entity["start"]
            entity_end = entity["end"]
            if (entity_start <= end or end == -1) and entity_end >= start:
                intersecting_entities.append(entity)
        return intersecting_entities

    def get_chunks(
        self,
        max_chars=15_000,
        generator_config: Dict[str, PiiState] = {},
        generator_default: PiiState = PiiState.Off,
        metadata_entities: List[str] = [],
        include_metadata=True,
    ) -> List:
        """Returns a list of chunks of text from the document.  The chunks are filtered
        by the generator_default configuration.

        Arguments:
            max_chars: int = 15_000
                The maximum number of characters in each chunk.

            generator_config: Dict[str, PiiState]
                A dictionary of sensitive data entities. For each entity, indicates
                whether to redact, synthesize, or ignore it.
                Values must be one of "Redaction", "Synthesis", or "Off".

            generator_default: PiiState = PiiState.Redaction
                The default redaction used for all types not specified in
                generator_config.
                Values must be one of "Redaction", "Synthesis", or "Off".


            include_metadata: bool = True
                If True, the metadata will be included in the chunk.
        Returns:
            List[str]
                A list of strings containing the chunks of text.
        """
        text = self.get_markdown(generator_config, generator_default)
        all_entities = self.get_all_entities()
        entities = [ent for ent in all_entities if ent["label"] in metadata_entities]
        output = []
        for chunk in split_markdown(text, max_chars):
            start, end = chunk["indices"]
            headers = chunk["headers"]
            sensitive_entity_types = [
                label for label, key in generator_config.items() if key != PiiState.Off
            ]

            chunk_text = text[start:end]
            is_sensitive = self.is_sensitive(
                sensitive_entity_types, start, end  # type: ignore
            )
            chunk_dict = {"text": chunk_text, "is_sensitive": is_sensitive}
            if include_metadata:
                entity_metdata = self._make_entity_metadata(  # type: ignore
                    self._find_intersecting_entites(
                        start, end, entities  # type: ignore
                    )
                )

                metadata = {"headers": headers, "entities": entity_metdata}
                metadata.update(self.metadata)
                chunk_dict["metadata"] = metadata
            output.append(chunk_dict)
        return output
