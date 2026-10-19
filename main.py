"""Run a small PawPal+ schedule demo."""

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    """Create and print a sample pet care schedule."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "cat")
    buddy = Pet("Buddy", "dog")
    owner.add_pet(mochi)
    owner.add_pet(buddy)

    evening_meal = Task("Evening meal", "18:00", frequency="daily")
    mochi.add_task(evening_meal)
    buddy.add_task(Task("Morning walk", "07:30"))
    mochi.add_task(Task("Breakfast", "08:00"))
    buddy.add_task(Task("Afternoon walk", "14:00"))
    mochi.add_task(Task("Grooming", "12:00"))
    buddy.add_task(Task("Medication", "12:00"))

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(evening_meal)

    results = (
        ("Schedule (sorted by time)", scheduler.sort_by_time()),
        ("Mochi's Tasks", scheduler.filter_tasks(pet_name="Mochi")),
        ("Completed Tasks", scheduler.filter_tasks(completed=True)),
    )

    for title, tasks in results:
        print(f"\n{title}")
        print("-" * len(title))
        for task in tasks:
            print(
                f"{task.due_date:%Y-%m-%d} {task.time} | "
                f"{task.pet_name} | {task.description}"
            )

    conflict_warnings = scheduler.detect_conflicts()
    print("\nSchedule Conflict Warnings")
    print("--------------------------")
    if conflict_warnings:
        for warning in conflict_warnings:
            print(warning)
    else:
        print("No conflicts found.")

    next_meal = next(
        task
        for task in mochi.get_tasks()
        if task.description == evening_meal.description and not task.completed
    )
    print("\nDaily Recurrence")
    print("----------------")
    print(f"Next {next_meal.description}: {next_meal.due_date:%Y-%m-%d} at {next_meal.time}")


if __name__ == "__main__":
    main()
