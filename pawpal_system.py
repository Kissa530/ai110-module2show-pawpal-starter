"""Skeleton classes for the PawPal+ pet care system."""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Task:
    description: str
    time: str
    frequency: str = "once"
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        return self.tasks


class Owner:
    name: str
    pets: list[Pet]

    def __init__(self, name: str, pets: Optional[list[Pet]] = None) -> None:
        """Initialize an owner with an optional pet list."""
        self.name = name
        self.pets = pets if pets is not None else []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return the tasks belonging to all of this owner's pets."""
        return [task for pet in self.pets for task in pet.get_tasks()]


class Scheduler:
    owner: Owner

    def __init__(self, owner: Owner) -> None:
        """Initialize a scheduler for an owner."""
        self.owner = owner

    def sort_by_time(self) -> list[Task]:
        """Return the owner's tasks sorted by their HH:MM time."""
        tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda task: task.time)

    def filter_tasks(self) -> None:
        """Filter tasks."""
        pass

    def detect_conflicts(self) -> None:
        """Detect scheduling conflicts."""
        pass

    def mark_task_complete(self, task: Task) -> None:
        """Mark a task as complete."""
        pass
