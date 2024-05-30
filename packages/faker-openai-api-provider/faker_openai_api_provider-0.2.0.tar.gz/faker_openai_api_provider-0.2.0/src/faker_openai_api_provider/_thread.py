from ._utils import gen_id


class ThreadProvider:
    def __init__(self) -> None:
        self.message = ThreadProvider.MessageProvider()
        self.run = ThreadProvider.RunProvider()

    def id(self) -> str:
        return gen_id("thread")

    class MessageProvider:
        def id(self) -> str:
            return gen_id("msg")

    class RunProvider:
        def __init__(self) -> None:
            self.step = ThreadProvider.RunProvider.StepProvider()

        def id(self) -> str:
            return gen_id("run")

        class StepProvider:
            def __init__(self) -> None:
                self.step_details = (
                    ThreadProvider.RunProvider.StepProvider.StepDetailsProvider()
                )

            def id(self) -> str:
                return gen_id("step")

            class StepDetailsProvider:

                def __init__(self) -> None:
                    self.tool_call = (
                        ThreadProvider.RunProvider.StepProvider.StepDetailsProvider.ToolCallProvider()
                    )

                class ToolCallProvider:
                    def id(self) -> str:
                        return gen_id("call")
