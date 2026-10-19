from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def build_owner_with_two_pets() -> tuple[Owner, Pet, Pet]:
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "cat")
    buddy = Pet("Buddy", "dog")
    owner.add_pet(mochi)
    owner.add_pet(buddy)
    return owner, mochi, buddy


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


def test_sort_tasks_chronologically_across_pets() -> None:
    owner, mochi, buddy = build_owner_with_two_pets()
    late = Task("Evening walk", "18:00")
    early = Task("Breakfast", "07:00")
    midday = Task("Lunch", "12:00")
    mochi.add_task(late)
    buddy.add_task(early)
    mochi.add_task(midday)

    assert Scheduler(owner).sort_by_time() == [early, midday, late]


def test_daily_completion_creates_next_day_task_on_same_pet() -> None:
    owner, mochi, _ = build_owner_with_two_pets()
    due_date = date(2026, 1, 1)
    task = Task("Medication", "08:00", frequency="daily", due_date=due_date)
    mochi.add_task(task)

    Scheduler(owner).mark_task_complete(task)

    assert task.completed is True
    assert mochi.tasks[1].description == task.description
    assert mochi.tasks[1].due_date == due_date + timedelta(days=1)
    assert mochi.tasks[1].pet_name == mochi.name
    assert len(mochi.tasks) == 2
    assert owner.pets[1].tasks == []


def test_weekly_completion_creates_task_seven_days_later() -> None:
    owner, mochi, _ = build_owner_with_two_pets()
    due_date = date(2026, 1, 1)
    task = Task("Grooming", "10:00", frequency="weekly", due_date=due_date)
    mochi.add_task(task)

    Scheduler(owner).mark_task_complete(task)

    assert task.completed is True
    assert mochi.tasks[1].due_date == due_date + timedelta(days=7)


def test_one_time_completion_creates_no_copy() -> None:
    owner, mochi, _ = build_owner_with_two_pets()
    task = Task("Feed", "08:00", due_date=date(2026, 1, 1))
    mochi.add_task(task)

    Scheduler(owner).mark_task_complete(task)

    assert task.completed is True
    assert mochi.tasks == [task]


def test_detect_conflicts_for_pending_tasks_at_same_date_and_time() -> None:
    owner, mochi, buddy = build_owner_with_two_pets()
    due_date = date(2026, 1, 1)
    mochi.add_task(Task("Grooming", "12:00", due_date=due_date))
    buddy.add_task(Task("Medication", "12:00", due_date=due_date))

    warnings = Scheduler(owner).detect_conflicts()

    assert len(warnings) == 1
    assert "Mochi: Grooming" in warnings[0]
    assert "Buddy: Medication" in warnings[0]


def test_empty_owner_and_pet_have_no_tasks() -> None:
    empty_owner = Owner("Jordan")
    empty_pet_owner = Owner("Jordan", [Pet("Mochi", "cat")])

    assert Scheduler(empty_owner).sort_by_time() == []
    assert Scheduler(empty_pet_owner).filter_tasks() == []
    assert Scheduler(empty_pet_owner).detect_conflicts() == []


def test_filter_by_unknown_pet_returns_no_tasks() -> None:
    owner, mochi, _ = build_owner_with_two_pets()
    mochi.add_task(Task("Feed", "08:00"))

    assert Scheduler(owner).filter_tasks(pet_name="Unknown") == []
