from pawpal_system import Pet, Task


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
