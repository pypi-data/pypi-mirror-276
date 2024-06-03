from enum import Enum, auto
from pydantic import BaseModel, field_validator
from typing import Any, TypeVar, Generator, Generic, AsyncGenerator
from cycls import UI
from datetime import datetime
from socketio import AsyncClient, Client  # type: ignore[import-untyped]
import uuid
import httpx
import json


MessageContent = TypeVar("MessageContent", bound=UI.Text | UI.Image | None)


class InputTypeHint(Enum):
    EMPTY = auto()
    MESSAGE = auto()
    CONVERSATION_ID = auto()
    USER = auto()
    SESSION = auto()
    FULL = auto()
    MESSAGE_CONTENT = auto()


class MessageRole(Enum):
    ASSISTANT = "assistant"
    USER = "user"
    CYCLS = "cycls"


class Message(BaseModel, Generic[MessageContent]):
    id: str
    created_at: datetime
    content: MessageContent
    role: MessageRole = MessageRole.ASSISTANT
    meta: dict[str, Any] | None = None

    @field_validator("content", mode="before")
    @classmethod
    def create_content(cls, values: dict[str, Any]):
        if values is None:
            return None
        content_type = values.get("type")
        if content_type == "text":
            return UI.Text(**values)
        elif content_type == "image":
            return UI.Image(**values)
        else:
            raise ValueError(f"Unknown content type: {content_type}")


Meta = dict[str, Any]
ConversationID = str


class ConversationSession(BaseModel):
    id: str
    messages: list[Message]
    meta: dict[str, str] | None = {}


class Response(BaseModel):
    messages: list[UI.Text | UI.Image]
    meta: dict[str, Any] | None = None


class AsyncSendBase:
    def __init__(self, sio: AsyncClient, user_message_id, url:str) -> None:
        self.sio = sio
        self.user_message_id = user_message_id
        self.url = url

    def send_message_data(
        self, content, id, stream: bool = False, finish_reason: str | None = None
    ):
        if isinstance(content, BaseModel):
            content = content.model_dump(mode="json", exclude_none=True)
        elif not content:
            content = {'type': 'text', 'text':''}
        data = {
            "content": content,
            "id": id,
            "user_message_id": self.user_message_id,
            "finish_reason": finish_reason,
            "stream": stream,
        }
        return data


class SendBase:
    def __init__(self, sio: Client, user_message_id, url:str) -> None:
        self.sio = sio
        self.user_message_id = user_message_id
        self.url = url

    def send_message_data(
        self, content, id, stream: bool = False, finish_reason: str | None = None
    ):
        if isinstance(content, BaseModel):
            content = content.model_dump(mode="json", exclude_none=True)
        elif not content:
            content = {'type': 'text', 'text':''}
        data = {
            "content": content,
            "id": id,
            "user_message_id": self.user_message_id,
            "finish_reason": finish_reason,
            "stream": stream,
        }
        return data


class AsyncSend(AsyncSendBase):
    async def finish(self, id):
        data = self.send_message_data(None, id, True, "finish")
        async with httpx.AsyncClient() as client:
            await client.post(self.url + '/chat_app/send_message', json=data)

    async def text(self, message):
        id = str(uuid.uuid4())
        content = UI.Text(text=message)
        data = self.send_message_data(content=content, id=id)
        async with httpx.AsyncClient() as client:
            await client.post(self.url + '/chat_app/send_message', json=data)


class SyncSend(SendBase):
    def finish(self, id):
        data = self.send_message_data(None, id, True, "finish")
        httpx.post(self.url + '/chat_app/send_message', json=data)

    def text(self, message):
        id = str(uuid.uuid4())
        content = UI.Text(text=message)
        data = self.send_message_data(content=content, id=id)
        httpx.post(self.url + '/chat_app/send_message', json=data)


class AsyncSendStream(AsyncSendBase):
    async def text(self, message_stream: AsyncGenerator):
        id = str(uuid.uuid4())
        timeout = httpx.Timeout(120, connect=60)
        async with httpx.AsyncClient(timeout=timeout) as client:
            async with client.stream("POST", self.url+'/chat_app/send_message') as response:
                async for chunk in message_stream:
                    try:
                        await response.aclose()
                        data = self.send_message_data(UI.Text(text=chunk), id, True)
                        async with client.stream("POST", self.url+'/chat_app/send_message', json=json.dumps(data) + "\n") as response:
                            pass
                    except Exception as e:
                        print(f'we got theis error {e}')
                        data = self.send_message_data(None, id, True, "error")
                        async with client.stream("POST", self.url+'/chat_app/send_message', json=json.dumps(data) + "\n") as response:
                            break
        return True, id



class SyncSendStream(SendBase):
    def text(self, message_stream: Generator):
        id = str(uuid.uuid4())
        timeout = httpx.Timeout(120, connect=60)
        with httpx.Client(timeout=timeout) as client:
            with client.stream("POST", self.url+'/chat_app/send_message') as response:
                for chunk in message_stream:
                    try:
                        response.close()
                        data = self.send_message_data(UI.Text(text=chunk), id, True)
                        with client.stream("POST", self.url+'/chat_app/send_message', json=json.dumps(data) + "\n") as response:
                            pass
                    except Exception as e:
                        data = self.send_message_data(None, id, True, "error")
                        print(f'we got an error {e}')
                        with client.stream("POST", self.url+'/chat_app/send_message', json=json.dumps(data) + "\n") as response:
                            break
        return True, id



class UserMessage(BaseModel):
    message: Message
    session: ConversationSession
    meta: dict[str, Any] | None = None


class Context:
    id: str
    history: list[Message]
    message: Message
    meta: dict[str, Any] | None = None

    def __init__(self, message, session):
        m = UserMessage(message=message, session=session)
        self.message = m.message
        self.id = m.session.id
        self.meta = m.session.meta
        self.history = m.session.messages


class SyncContext(Context):
    send: SyncSend
    stream: SyncSendStream

    def __init__(self, message, session, sio, url):
        super().__init__(message, session)
        self.send = SyncSend(sio=sio, user_message_id=self.message.id, url=url)
        self.stream = SyncSendStream(sio=sio, user_message_id=self.message.id, url=url)


class AsyncContext(Context):
    send: AsyncSend
    stream: AsyncSendStream

    def __init__(self, message, session, sio, url):
        super().__init__(message, session)
        self.send = AsyncSend(sio=sio, user_message_id=self.message.id, url=url)
        self.stream = AsyncSendStream(sio=sio, user_message_id=self.message.id, url=url)
