from typing import Union, Mapping, TypeAlias, Sequence, Type, Callable
from argparse import ArgumentParser, Namespace, _SubParsersAction

from patterns.command import ICommand
from .task_manager import TaskManager
from .task import Task

ITask: TypeAlias = ICommand[None, None]
ITaskManager: TypeAlias = ICommand[Sequence[str], None]


class ManagerController:
    def __init__(self, name: str, description: str, version: Union[str, int]) -> None:
        self.__argparser: ArgumentParser = ArgumentParser(
            prog=name.upper(), description=description.upper(), version=version
        )

        self.__subparser: _SubParsersAction[
            ArgumentParser
        ] = self.__argparser.add_subparsers(
            dest="module",
            description="These modules are the task managers created in the system.",
            title="Task Managers",
            required=True,
        )

        self.__managers: Mapping[str, ITaskManager] = {}

    def __get_task_manager(self, name: str) -> ITaskManager:
        task_manager: ITaskManager = [
            manager for key, manager in self.__managers.items() if key == name
        ][0]

        return task_manager

    def create_task_manager(self, name: str) -> None:
        task_manager: ITaskManager = TaskManager(name, self.__subparser)

        self.__managers[task_manager.name] = task_manager

    def add_task(
        self, manager_name: str, name: str, shortname: str, description: str
    ) -> Callable[[Type[ITask]], Type[ITask]]:
        def wrapper(cls: Type[Task]) -> Type[Task]:
            manager: TaskManager = self.__get_task_manager(manager_name)

            task: ITask = cls(name, shortname, description)

            manager.add_task(task)

            return cls

        return wrapper

    def run(self) -> None:
        namespaces: Namespace = self.__argument.parse_args()

        try:
            task_manager: ITaskManager = self.__get_task_manager(namespaces.module)

        except IndexError:
            self.__argument.print_help()

        else:
            args: Sequence[str] = [
                key for key, value in namespaces.__dict__.items() if value is True
            ]

            task_manager.execute(args)
