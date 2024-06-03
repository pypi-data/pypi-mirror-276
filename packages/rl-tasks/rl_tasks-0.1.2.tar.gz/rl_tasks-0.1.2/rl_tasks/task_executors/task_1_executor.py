import rl_test_task_1
from rl_test_common import Common

from .base.task_executor import TaskExecutor


class Task1Executor(TaskExecutor):
    __common: Common = Common()

    def execute(self, request: str) -> None:
        if request == '1':
            client: rl_test_task_1.Client = rl_test_task_1.Client()
            client.client_code()

            self.__common.clear_screen()

        else:
            return super().execute(request)
