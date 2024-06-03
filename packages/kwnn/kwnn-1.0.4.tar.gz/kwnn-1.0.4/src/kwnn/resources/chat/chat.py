from .completions import Completions
from ..._resource import SyncAPIResource


class Chat(SyncAPIResource):
    @property
    def completions(self) -> Completions:
        return Completions(self._client)
