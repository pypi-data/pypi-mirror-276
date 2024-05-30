from ._utils import gen_id


class ChatProvider:
    def __init__(self) -> None:
        self.completion = ChatProvider.CompletionProvider()

    class CompletionProvider:
        def id(self) -> str:
            return gen_id("chatcmpl")
