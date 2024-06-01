import httpx


class SyncAPIClient:
    _base_url = "https://www.kwniu.com/"
    _request: httpx.Client

    def __init__(self, *, base_url: str = None, api_key: str, timeout: int = 120) -> None:
        if base_url:
            self._base_url = base_url

        self._request = httpx.Client(
            base_url=self._base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=timeout,
        )
