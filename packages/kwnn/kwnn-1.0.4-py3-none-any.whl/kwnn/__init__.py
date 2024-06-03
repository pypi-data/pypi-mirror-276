import os
from typing import Optional
from . import resources
from ._client import SyncAPIClient


class KwnnAI(SyncAPIClient):
    chat: resources.Chat

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: int = 120,
    ) -> None:
        self.api_key = api_key

        if api_key is None:
            api_key = os.environ.get("KWNN_API_KEY")
        if not api_key:
            raise ValueError(
                "api_key must be set. or by setting the KWNN_API_KEY environment variable"
            )

        if base_url is None:
            base_url = os.environ.get("KWNN_BASE_URL")
        if not base_url:
            base_url = "https://www.kwniu.com/api/v1"

        super().__init__(base_url=base_url, api_key=api_key, timeout=timeout)

        self.chat = resources.Chat(self)
