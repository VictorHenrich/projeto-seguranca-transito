from typing import TypeAlias, Dict, Sequence
from argparse import ArgumentParser, _SubParsersAction

from .task import Task
from patterns.command import ICommand


ITask: TypeAlias = ICommand[None]
Tasks: TypeAlias = Dict[str, ITask]


class TaskManager:
    def __init__(self, name: str, subparser: _SubParsersAction) -> None:
        self.__argument_parser: ArgumentParser = subparser.add_parser(name)
        self.__name: str = name
        self.__tasks: Tasks = {}

    @property
    def name(self) -> str:
        return self.__name

    @property
    def subparser(self) -> ArgumentParser:
        return self.__argument_parser

    @property
    def tasks(self) -> Tasks:
        return self.__tasks

    def add_task(self, task: Task):
        self.__tasks[task.name] = task

        names: Sequence[str] = f"-{task.shortname}", f"--{task.name}"

        self.__argument_parser.add_argument(
            *names, help=task.description, action="store_true"
        )

    def execute(self, props: Sequence[str]) -> None:
        tasks: Sequence[ITask] = [
            task for task_name, task in self.__tasks.items() if task_name in props
        ]

        [task.execute(None) for task in tasks]
