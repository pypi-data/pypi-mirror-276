import httpx


class SyncAPIClient:
    _request: httpx.Client

    def __init__(self, *, base_url: str, api_key: str, timeout: int = 120) -> None:
        self._request = httpx.Client(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=timeout,
        )
