"""Skeleton classes for the PawPal+ pet care system."""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


@dataclass
class Task:
    description: str
    time: str
    frequency: str = "once"
    completed: bool = False
    due_date: date = field(default_factory=date.today)
    pet_name: Optional[str] = None

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
        task.pet_name = self.name
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

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> list[Task]:
        """Return tasks matching the optional pet name and completion status."""
        tasks = self.owner.get_all_tasks()
        return [
            task
            for task in tasks
            if (pet_name is None or task.pet_name == pet_name)
            and (completed is None or task.completed == completed)
        ]

    def detect_conflicts(self) -> list[str]:
        """Return warnings for pending tasks sharing a due date and time."""
        tasks_by_slot: dict[tuple[date, str], list[Task]] = {}
        for task in self.owner.get_all_tasks():
            if not task.completed:
                slot = (task.due_date, task.time)
                tasks_by_slot.setdefault(slot, []).append(task)

        warnings = []
        for (due_date, task_time), tasks in tasks_by_slot.items():
            if len(tasks) > 1:
                conflicts = "; ".join(
                    f"{task.pet_name}: {task.description}" for task in tasks
                )
                warnings.append(
                    f"Conflict on {due_date:%Y-%m-%d} at {task_time}: {conflicts}"
                )
        return warnings

    def mark_task_complete(self, task: Task) -> None:
        """Complete a task and add its next daily or weekly occurrence."""
        recurrence_days = {"daily": 1, "weekly": 7}
        pet = None
        if task.frequency in recurrence_days:
            pet = next(
                (pet for pet in self.owner.pets if pet.name == task.pet_name),
                None,
            )
            if pet is None:
                raise ValueError(
                    f"No pet found for task associated with {task.pet_name!r}."
                )

        task.mark_complete()
        if pet is not None:
            pet.add_task(
                Task(
                    description=task.description,
                    time=task.time,
                    frequency=task.frequency,
                    due_date=task.due_date
                    + timedelta(days=recurrence_days[task.frequency]),
                )
            )
