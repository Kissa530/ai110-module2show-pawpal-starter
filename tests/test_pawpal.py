from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion() -> None:
    task = Task(description="Feed", time="08:00")

    task.mark_complete()

    assert task.completed is True


def test_task_addition_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", species="cat")
    task = Task(description="Feed", time="08:00")
    initial_count = len(pet.tasks)

    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1


def test_detect_conflicts_reports_pending_tasks_at_same_slot() -> None:
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "cat")
    buddy = Pet("Buddy", "dog")
    owner.add_pet(mochi)
    owner.add_pet(buddy)
    mochi.add_task(Task("Grooming", "12:00"))
    buddy.add_task(Task("Medication", "12:00"))

    warnings = Scheduler(owner).detect_conflicts()

    assert len(warnings) == 1
    assert "Mochi: Grooming" in warnings[0]
    assert "Buddy: Medication" in warnings[0]


def test_detect_conflicts_ignores_completed_or_different_date_tasks() -> None:
    owner = Owner("Jordan")
    pet = Pet("Mochi", "cat")
    owner.add_pet(pet)
    completed = Task("First grooming", "12:00")
    completed.mark_complete()
    pet.add_task(completed)
    pet.add_task(
        Task("Next grooming", "12:00", due_date=date.today() + timedelta(days=1))
    )

    assert Scheduler(owner).detect_conflicts() == []
