from ._utils import gen_id


class VectorStoreProvider:
    def __init__(self) -> None:
        self.file_batch = VectorStoreProvider.VectorStoreFileBatchProvider()

    def id(self) -> str:
        return gen_id("vs")

    class VectorStoreFileBatchProvider:
        def id(self) -> str:
            return gen_id("vsfb")
