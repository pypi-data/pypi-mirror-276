from ._utils import gen_id


class FileProvider:
    def id(self) -> str:
        return gen_id("file", sep="-")
