"""Skeleton classes for the PawPal+ pet care system."""

from dataclasses import dataclass, field
from datetime import date, time as Time
from typing import Optional


@dataclass
class Task:
    description: str
    time: Time
    frequency: str
    completed: bool
    due_date: date

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> None:
        pass


class Owner:
    name: str
    pets: list[Pet]

    def __init__(self, name: str, pets: Optional[list[Pet]] = None) -> None:
        self.name = name
        self.pets = pets if pets is not None else []

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> None:
        pass


class Scheduler:
    owner: Owner

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def sort_by_time(self) -> None:
        pass

    def filter_tasks(self) -> None:
        pass

    def detect_conflicts(self) -> None:
        pass

    def mark_task_complete(self, task: Task) -> None:
        pass
