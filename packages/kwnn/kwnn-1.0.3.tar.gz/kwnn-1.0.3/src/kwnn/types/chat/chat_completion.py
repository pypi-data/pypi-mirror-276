import typing as t

from pydantic import UUID4, BaseModel


class MessageContent(BaseModel):
    content: str


class ChatCompletion(BaseModel):
    cid: t.Optional[UUID4] = None
    mid: t.Optional[UUID4] = None
    message: t.List[MessageContent] = []
