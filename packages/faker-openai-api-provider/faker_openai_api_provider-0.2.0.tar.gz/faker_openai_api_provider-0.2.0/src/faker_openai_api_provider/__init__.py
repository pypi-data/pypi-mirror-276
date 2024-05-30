from typing import Any

from faker.providers import BaseProvider

from ._chat import ChatProvider
from ._file import FileProvider
from ._assistants import AssistantProvider
from ._thread import ThreadProvider
from ._vector_store import VectorStoreProvider


class OpenAiApiProvider(BaseProvider):
    def __init__(self, generator: Any) -> None:
        super().__init__(generator)
        self._api = OpenAiApiProvider.Api()

    def openai(self):
        return self._api

    class Api:
        def __init__(self) -> None:
            self.chat = ChatProvider()
            self.file = FileProvider()
            self.beta = OpenAiApiProvider.Api.BetaProviders()

        class BetaProviders:
            def __init__(self) -> None:
                self.assistant = AssistantProvider()
                self.thread = ThreadProvider()
                self.vector_store = VectorStoreProvider()
