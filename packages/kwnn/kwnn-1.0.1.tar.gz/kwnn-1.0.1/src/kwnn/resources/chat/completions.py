from typing import overload, Union, Generator, Optional
from typing_extensions import Literal
from ..._resource import SyncAPIResource
from ...types.chat import ChatCompletion, ChatCompletionChunk

# from openai._utils import required_args
import json
import httpx


class Completions(SyncAPIResource):
    # @overload
    # def create(
    #     self,
    #     *,
    #     cid: str = None,
    #     content: str,
    # ) -> ChatCompletion:
    #     ...

    # @overload
    # def create(
    #     self,
    #     *,
    #     cid: str = None,
    #     content: str,
    #     stream: Literal[True],
    # ) -> Generator[ChatCompletionChunk, None, None]:
    #     ...

    def create(
        self,
        *,
        cid: Optional[str] = None,
        content: str,
        stream: Literal[True, False] = False,
    ):
        try:
            data = {"cid": cid, "content": content, "stream": stream}
            if not cid:
                del data["cid"]

            if stream:
                return self._create_stream(data)
            else:
                return self._create_single_response(data)
        except Exception as e:
            raise e

    def _create_stream(self, data) -> Generator[ChatCompletionChunk, None, None]:
        with self._client._request.stream(
            "POST",
            "api/v1/chat",
            json=data,
        ) as response:
            for chunk in response.iter_bytes():
                chunk = chunk.decode("utf-8")
                chunk = json.loads(chunk)

                if chunk.get("code", None) is None:
                    raise Exception("Invalid response")
                if chunk.get("code") > 0:
                    raise Exception(chunk.get("message"))

                chunk = chunk.get("data")

                yield ChatCompletionChunk(**chunk)

    def _create_single_response(self, data) -> ChatCompletion:
        response = self._client._request.post(
            "/api/v1/chat",
            json=data,
        )

        if response.status_code != httpx.codes.OK:
            raise Exception(response.text)

        response = response.json()
        if response.get("code", None) is None:
            raise Exception("Invalid response")
        if response.get("code") > 0:
            raise Exception(response.get("message"))

        response = response.get("data")

        return ChatCompletion(**response)

    # def create(
    #     self,
    #     *,
    #     cid: Optional[str] = None,
    #     content: str,
    #     stream: bool = False,
    # ):
    #     try:
    #         data = {"cid": cid, "content": content, "stream": stream}
    #         if not cid:
    #             del data["cid"]

    #         if stream:
    #             print("stream")
    #             url = f"{self._client._base_url}api/v1/chat"

    #             with httpx.stream(
    #                 "POST",
    #                 url,
    #                 json=data,
    #                 headers=self._client._request.headers,
    #                 timeout=self._client._request.timeout,
    #             ) as response:
    #                 for chunk in response.iter_bytes():
    #                     chunk = chunk.decode("utf-8")
    #                     chunk = json.loads(chunk)

    #                     if chunk.get("code", None) is None:
    #                         raise Exception("Invalid response")
    #                     if chunk.get("code") > 0:
    #                         raise Exception(chunk.get("message"))

    #                     chunk = chunk.get("data")

    #                     yield ChatCompletionChunk(**chunk)
    #         else:
    #             print("no stream")
    #             response = self._client._request.post(
    #                 "/api/v1/chat",
    #                 json=data,
    #             )

    #             if response.status_code != httpx.codes.OK:
    #                 raise Exception(response.text)

    #             response = response.json()
    #             if response.get("code"):
    #                 if response.get("code") > 0:
    #                     raise Exception(response.get("message"))

    #             print(response)

    #             response = response.get("data")

    #             return ChatCompletion(**response)
    #     except Exception as e:
    #         raise e

    # @required_args(["content"], ["cid", "content"])
    # def create(
    #     self,
    #     *,
    #     cid: str = None,
    #     content: str,
    # ) -> ChatCompletion:
    #     try:
    #         data = {"cid": cid, "content": content}
    #         if not cid:
    #             del data["cid"]

    #         print(data)

    #         response = self._client._request.post(
    #             "/api/v1/chat",
    #             json=data,
    #         ).json()

    #         print(response)

    #         if response.get("code"):
    #             if response.get("code") > 0:
    #                 raise Exception(response.get("message"))

    #         response = response.get("data")

    #         return ChatCompletion(**response)
    #     except Exception as e:
    #         raise e

    # @required_args(["content", "stream"], ["cid", "content", "stream"])
    # def create(
    #     self,
    #     *,
    #     cid: str = None,
    #     content: str,
    #     stream: Literal[True],
    # ) -> ChatCompletionChunk:
    #     try:
    #         data = {"cid": cid, "content": content, "stream": stream}
    #         if not cid:
    #             del data["cid"]

    #         print(data)

    #         response = self._client._request.post(
    #             "/api/v1/chat",
    #             json=data,
    #         ).json()

    #         print(response)

    #         if response.get("code"):
    #             if response.get("code") > 0:
    #                 raise Exception(response.get("message"))

    #         response = response.get("data")

    #         return ChatCompletionChunk(**response)
    #     except Exception as e:
    #         raise e
