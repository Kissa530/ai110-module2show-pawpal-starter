# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Features

- **Manage pets and tasks:** Add pets to an owner with `Owner.add_pet()` and add tasks to a pet with `Pet.add_task()`. Each task is associated with its pet.
- **View an owner's tasks:** `Owner.get_all_tasks()` collects tasks from all pets.
- **Sort the schedule by time:** `Scheduler.sort_by_time()` returns tasks in ascending time order.
- **Filter tasks:** `Scheduler.filter_tasks()` filters by pet name, completion status, or both.
- **Detect schedule conflicts:** `Scheduler.detect_conflicts()` reports pending tasks with the same due date and time.
- **Complete and recur tasks:** `Scheduler.mark_task_complete()` marks a task complete and creates its next daily or weekly occurrence. One-time tasks do not create a copy.

## What PawPal+ does

The app lets a user:

- Enter an owner name and add pets with a name and species
- Schedule tasks for each pet with a time and a frequency (once, daily, or weekly)
- See every pet's tasks in one schedule, sorted by date and time
- Filter the schedule by pet or by pending/completed status
- Get a warning when two pending tasks are scheduled at the same time
- Mark tasks complete, which automatically creates the next daily or weekly occurrence

The logic is covered by automated tests for sorting, recurrence, conflict detection, and edge cases.


## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.


## 🖥️ Sample Output

Output from `python main.py`:

```
Today's Schedule
----------------
07:30 | Buddy | Morning walk
08:00 | Mochi | Breakfast
14:00 | Buddy | Afternoon walk
18:00 | Mochi | Evening meal
```



## 🧪 Testing PawPal+

Run the tests from the repo root:

```
python -m pytest
```

The suite covers:
- **Sorting:** tasks added out of order come back in chronological order across pets.
- **Recurrence:** completing a daily task creates a task for the next day on the same pet, a weekly task creates one 7 days later, and a one-time task creates none.
- **Conflict detection:** two pending tasks at the same date and time produce a warning, while completed tasks and tasks on different dates do not.
- **Edge cases:** an owner or pet with no tasks, and filtering by a pet name that doesn't exist.
- **Basics:** marking a task complete and adding a task to a pet.

Sample test output:

```
================================================= test session starts =================================================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0 -- C:\Python314\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\issam\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 11 items

tests/test_pawpal.py::test_task_completion PASSED                                                                [  9%]
tests/test_pawpal.py::test_task_addition_increases_pet_task_count PASSED                                         [ 18%]
tests/test_pawpal.py::test_detect_conflicts_reports_pending_tasks_at_same_slot PASSED                            [ 27%]
tests/test_pawpal.py::test_detect_conflicts_ignores_completed_or_different_date_tasks PASSED                     [ 36%]
tests/test_pawpal.py::test_sort_tasks_chronologically_across_pets PASSED                                         [ 45%]
tests/test_pawpal.py::test_daily_completion_creates_next_day_task_on_same_pet PASSED                             [ 54%]
tests/test_pawpal.py::test_weekly_completion_creates_task_seven_days_later PASSED                                [ 63%]
tests/test_pawpal.py::test_one_time_completion_creates_no_copy PASSED                                            [ 72%]
tests/test_pawpal.py::test_detect_conflicts_for_pending_tasks_at_same_date_and_time PASSED                       [ 81%]
tests/test_pawpal.py::test_empty_owner_and_pet_have_no_tasks PASSED                                              [ 90%]
tests/test_pawpal.py::test_filter_by_unknown_pet_returns_no_tasks PASSED                                         [100%]

================================================= 11 passed in 0.04s ==================================================
```

**Confidence Level: ★★★★☆ (4/5)**

All 11 tests pass and they cover the main behaviors and several edge cases. I held back a star because sorting assumes zero-padded `HH:MM` times, conflict detection only checks exact matches (no durations), and some tests don't check every field of a recurring task.


## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts all tasks across every pet by due date, then by `HH:MM` time, so tomorrow's tasks come after today's. |
| Filtering | `Scheduler.filter_tasks(pet_name, completed)` | Returns tasks for one pet, only completed or pending tasks, or both filters combined. With no arguments it returns every task. |
| Conflict handling | `Scheduler.detect_conflicts()` | Returns a warning for each date and time with more than one pending task, for the same pet or different pets. Matches exact times only (no durations) and skips completed tasks. |
| Recurring tasks | `Scheduler.mark_task_complete()` | Marks the task done and, for `daily` or `weekly` tasks, adds a new task to the same pet due 1 or 7 days later using `timedelta`. One-time tasks are only marked complete. |



## 📸 Demo Walkthrough

**What the app lets you do**
- Add pets with a name and species.
- Schedule a task for a pet with a description, a time, and a frequency (once, daily, or weekly).
- Mark tasks complete from a list of pending tasks.
- View a schedule sorted by time, filtered by pet or status, with a table of the results.

**Example workflow**
1. Enter an owner name and add two pets, such as Mochi (cat) and Buddy (dog).
2. Schedule a few tasks for each pet, entering them in any order.
3. Check the Schedule section: tasks from both pets appear sorted by time.
4. Add two tasks at the same time. A yellow warning names both tasks, their pets, and the time, and tells you to move one.
5. Mark a daily task complete. The task is checked off and a new copy appears dated for the next day.
6. Use the pet and status filters to narrow the table.

**Key Scheduler behaviors shown**
- Sorting puts tasks from different pets in one chronological list.
- Conflict warnings appear above the table and disappear once the conflict is resolved.
- Recurring tasks create their next occurrence automatically.

**Sample CLI output from `python main.py`**

```
Schedule (sorted by time)
-------------------------
2026-10-19 07:30 | Buddy | Morning walk
2026-10-19 08:00 | Mochi | Breakfast
2026-10-19 12:00 | Mochi | Grooming
2026-10-19 12:00 | Buddy | Medication
2026-10-19 14:00 | Buddy | Afternoon walk
2026-10-19 18:00 | Mochi | Evening meal
2026-10-20 18:00 | Mochi | Evening meal

Mochi's Tasks
-------------
2026-10-19 18:00 | Mochi | Evening meal
2026-10-19 08:00 | Mochi | Breakfast
2026-10-19 12:00 | Mochi | Grooming
2026-10-20 18:00 | Mochi | Evening meal

Completed Tasks
---------------
2026-10-19 18:00 | Mochi | Evening meal

Schedule Conflict Warnings
--------------------------
Conflict on 2026-10-19 at 12:00: Mochi: Grooming; Buddy: Medication

Daily Recurrence
----------------
Next Evening meal: 2026-10-20 at 18:00
```



## Implementation Summary

PawPal+ is a pet care scheduler built in Python. The logic lives in
pawpal_system.py and is made of four classes that work together:

- Task: one care activity (description, time, frequency, due date, completion status, and its pet's name).
- Pet: stores a pet's details and its own list of tasks.
- Owner: manages multiple pets and gathers every pet's tasks with get_all_tasks().
- Scheduler: reads tasks through Owner.get_all_tasks() to sort, filter, detect
  conflicts, and create the next occurrence of recurring tasks.

main.py is a CLI demo of these features, app.py is the Streamlit interface on top
of them, and tests/test_pawpal.py has 11 pytest tests covering sorting, recurrence,
conflict detection, filtering, and edge cases.