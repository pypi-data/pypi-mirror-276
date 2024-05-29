import os

from typing import List, Optional, Union

import requests

from tonic_textual.classes.httpclient import HttpClient
from tonic_textual.classes.pipeline import Pipeline


class TonicTextualParse:
    """Wrapper class for invoking Tonic Textual API

    Parameters
    ----------
    base_url : str
        The URL to your Tonic Textual instance. Do not include trailing backslashes.
    api_key : str
        Your API token. This argument is optional. Instead of providing the API token
        here, it is recommended that you set the API key in your environment as the
        value of TONIC_TEXTUAL_API_KEY.
    verify: bool
        Whether SSL Certification verification is performed.  This is enabled by
        default.
    Examples
    --------
    >>> TonicTextual("http://localhost:3000")
    """

    def __init__(
        self, base_url: str, api_key: Optional[str] = None, verify: bool = True
    ):
        if api_key is None:
            api_key = os.environ.get("TONIC_TEXTUAL_API_KEY")
            if api_key is None:
                raise Exception(
                    "No API key provided. Either provide an API key, or set the API "
                    "key as the value of the TONIC_TEXTUAL_API_KEY environment "
                    "variable."
                )
        self.api_key = api_key
        self.client = HttpClient(base_url, self.api_key, verify)
        self.verify = verify

    def get_pipelines(self) -> List[Pipeline]:
        with requests.Session() as session:
            response = self.client.http_get("/api/parsejobconfig", session=session)
            pipelines: List[Pipeline] = []
            for x in response:
                pipelines.append(Pipeline(x["name"], x["id"], self.client))
            return pipelines

    def get_pipeline_by_id(self, pipeline_id: str) -> Union[Pipeline, None]:
        pipelines = self.get_pipelines()
        found_pipelines = list(filter(lambda x: x.id == pipeline_id, pipelines))
        if len(found_pipelines) == 0:
            return None

        if len(found_pipelines) > 1:
            raise Exception(
                "Found more than 1 pipeline with this ID.  This shouldn't happen."
            )

        return found_pipelines[0]
