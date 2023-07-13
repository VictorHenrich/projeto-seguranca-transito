from typing import Union, TypeAlias, Collection, Type, Callable, List
from argparse import ArgumentParser, Namespace, _SubParsersAction

from patterns.command import ICommand
from .task_manager import TaskManager
from .task import Task


ITaskManager: TypeAlias = ICommand[Collection[str]]
DecoratorAddTask: TypeAlias = Callable[[Type[Task]], Type[Task]]


class CLI:
    __argument: ArgumentParser

    __subparser: _SubParsersAction

    __managers: List[TaskManager] = []

    @classmethod
    def set_config(
        cls, name: str, description: str, version: Union[str, int], *task_managers: str
    ):
        cls.__argument = ArgumentParser(
            prog=name.upper(), description=description.upper()
        )

        cls.__subparser = cls.__argument.add_subparsers(
            dest="module",
            description="These modules are the task managers created in the system.",
            title="Task Managers",
            required=True,
        )

        cls.__argument.add_argument(
            "-v", "--version", action="version", version=f"{name.title()} {version}"
        )

        for task_manager_name in task_managers:
            cls.create_task_manager(task_manager_name)

    @classmethod
    def __get_task_manager(cls, name: str) -> TaskManager:
        for manager in cls.__managers:
            if manager.name == name:
                return manager

        raise Exception("Task Manager not found!")

    @classmethod
    def create_task_manager(cls, name: str) -> None:
        task_manager: ITaskManager = TaskManager(name, cls.__subparser)

        cls.__managers.append(task_manager)

    @classmethod
    def add_task(
        cls, manager_name: str, name: str, shortname: str, description: str
    ) -> DecoratorAddTask:
        def decorator(c: Type[Task]) -> Type[Task]:
            manager: TaskManager = cls.__get_task_manager(manager_name)

            task: Task = c(name, shortname, description)

            manager.add_task(task)

            return c

        return decorator

    @classmethod
    def run(cls) -> None:
        namespaces: Namespace = cls.__argument.parse_args()

        try:
            task_manager: ITaskManager = cls.__get_task_manager(namespaces.module)

        except IndexError:
            cls.__argument.print_help()

        else:
            args: Collection[str] = [
                key for key, value in namespaces.__dict__.items() if value is True
            ]

            task_manager.execute(args)
