"""Run a small PawPal+ schedule demo."""

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    """Create and print a sample pet care schedule."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "cat")
    buddy = Pet("Buddy", "dog")
    owner.add_pet(mochi)
    owner.add_pet(buddy)

    mochi.add_task(Task("Evening meal", "18:00"))
    buddy.add_task(Task("Morning walk", "07:30"))
    mochi.add_task(Task("Breakfast", "08:00"))
    buddy.add_task(Task("Afternoon walk", "14:00"))

    pet_names_by_task_id = {
        id(task): pet.name
        for pet in owner.pets
        for task in pet.get_tasks()
    }

    print("Today's Schedule")
    print("----------------")
    for task in Scheduler(owner).sort_by_time():
        print(f"{task.time} | {pet_names_by_task_id[id(task)]} | {task.description}")


if __name__ == "__main__":
    main()
