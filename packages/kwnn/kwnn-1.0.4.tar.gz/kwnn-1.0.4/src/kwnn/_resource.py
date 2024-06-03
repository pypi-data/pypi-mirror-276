class SyncAPIResource:
    _client = None

    def __init__(self, client) -> None:
        self._client = client
