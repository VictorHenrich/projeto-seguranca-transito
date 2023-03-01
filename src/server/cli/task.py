from abc import ABC, abstractmethod


class Task:
    def __init__(self, name: str, shortname: str, description: str) -> None:
        self.__name: str = name
        self.__shortname: str = shortname
        self.__description: str = description

    @property
    def name(self) -> str:
        return self.__name

    @property
    def shortname(self) -> str:
        return self.__shortname

    @property
    def description(self) -> str:
        return self.__description

    @abstractmethod
    def execute(self, props: None) -> None:
        ...
