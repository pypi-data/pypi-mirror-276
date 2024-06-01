import os

from . import resources
from ._client import SyncAPIClient


class KwnnAI(SyncAPIClient):
    chat: resources.Chat

    def __init__(
        self,
        *,
        base_url: str = None,
        api_key: str | None = None,
        timeout: int = 120,
    ) -> None:
        self.api_key = api_key

        if api_key is None:
            api_key = os.environ.get("KWNN_API_KEY")
        if api_key is None:
            raise ValueError("api_key must be set.")

        super().__init__(base_url=base_url, api_key=api_key, timeout=timeout)

        self.chat = resources.Chat(self)
