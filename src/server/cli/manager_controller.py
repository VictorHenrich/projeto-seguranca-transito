from typing import Union, Mapping, TypeAlias, Collection, Type, Callable, Tuple
from argparse import ArgumentParser, Namespace, _SubParsersAction

from patterns.command import ICommand
from .task_manager import TaskManager
from .task import Task


ITaskManager: TypeAlias = ICommand[Collection[str]]
DecoratorAddTask: TypeAlias = Callable[[Type[Task]], Type[Task]]


class ManagerController:
    def __init__(self, name: str, description: str, version: Union[str, int]) -> None:
        argument, subparser = self.__handle_parsers(name, description, version)

        self.__argument: ArgumentParser = argument

        self.__subparser: _SubParsersAction = subparser

        self.__managers: Mapping[str, ITaskManager] = {}

    def __handle_parsers(
        self, name: str, description: str, version: Union[str, int]
    ) -> Tuple[ArgumentParser, _SubParsersAction]:
        argument: ArgumentParser = ArgumentParser(
            prog=name.upper(), description=description.upper()
        )

        subparser: _SubParsersAction = argument.add_subparsers(
            dest="module",
            description="These modules are the task managers created in the system.",
            title="Task Managers",
            required=True,
        )

        argument.add_argument(
            "-v", "--version", action="version", version=f"{name.title()} {version}"
        )

        return argument, subparser

    def __get_task_manager(self, name: str) -> TaskManager:
        for key, manager in self.__managers.items():
            if key == name and type(manager) is TaskManager:
                return manager

        raise Exception("Task Manager not found!")

    def create_task_manager(self, name: str) -> None:
        task_manager: ITaskManager = TaskManager(name, self.__subparser)

        self.__managers[task_manager.name] = task_manager

    def add_task(
        self, manager_name: str, name: str, shortname: str, description: str
    ) -> DecoratorAddTask:
        def decorator(cls: Type[Task]) -> Type[Task]:
            manager: TaskManager = self.__get_task_manager(manager_name)

            task: Task = cls(name, shortname, description)

            manager.add_task(task)

            return cls

        return decorator

    def run(self) -> None:
        namespaces: Namespace = self.__argument.parse_args()

        try:
            task_manager: ITaskManager = self.__get_task_manager(namespaces.module)

        except IndexError:
            self.__argument.print_help()

        else:
            args: Collection[str] = [
                key for key, value in namespaces.__dict__.items() if value is True
            ]

            task_manager.execute(args)
