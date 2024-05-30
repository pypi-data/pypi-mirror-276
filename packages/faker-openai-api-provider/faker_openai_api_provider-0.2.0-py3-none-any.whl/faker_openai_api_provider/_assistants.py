from ._utils import gen_id


class AssistantProvider:
    def id(self) -> str:
        return gen_id("asst")
