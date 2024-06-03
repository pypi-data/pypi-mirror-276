import typing as t

from .chat_completion import ChatCompletion, MessageContent


class ChatCompletionChunk(ChatCompletion):
    message: t.List[MessageContent] = []
