

from datetime import datetime

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Keep one Owner alive across Streamlit reruns
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

owner = st.session_state.owner

st.title("🐾 PawPal+")

st.markdown(
    """
**PawPal+** is a pet care planning assistant. Add your pets, schedule care tasks for them,
and see everything in one schedule sorted by time.
"""
)

st.divider()

# ---------------------------------------------------------------- Owner & pets
st.subheader("Owner and Pets")
owner.name = st.text_input("Owner name", value=owner.name)

col_a, col_b = st.columns(2)
with col_a:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_b:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if not pet_name.strip():
        st.error("Please enter a pet name.")
    elif any(p.name.lower() == pet_name.strip().lower() for p in owner.pets):
        st.warning(f"{pet_name} is already on your list.")
    else:
        owner.add_pet(Pet(name=pet_name.strip(), species=species))
        st.success(f"Added {pet_name.strip()} the {species}!")

if owner.pets:
    st.write("Your pets:")
    st.table([{"Name": p.name, "Species": p.species, "Tasks": len(p.get_tasks())} for p in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ----------------------------------------------------------------------- Tasks
st.subheader("Schedule a Task")

if owner.pets:
    chosen_pet_name = st.selectbox("Pet", [p.name for p in owner.pets])

    col1, col2, col3 = st.columns(3)
    with col1:
        task_description = st.text_input("Task", value="Morning walk")
    with col2:
        task_time = st.text_input("Time (HH:MM)", value="08:00")
    with col3:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add task"):
        try:
            datetime.strptime(task_time, "%H:%M")
        except ValueError:
            st.error("Time must be in 24-hour HH:MM format, like 07:30 or 18:00.")
        else:
            pet = next(p for p in owner.pets if p.name == chosen_pet_name)
            pet.add_task(Task(description=task_description, time=task_time, frequency=frequency))
            st.success(f"Added '{task_description}' at {task_time} for {chosen_pet_name}.")
else:
    st.info("Add a pet first, then you can schedule tasks for it.")

st.divider()

# -------------------------------------------------------------------- Schedule
st.subheader("Today's Schedule")

scheduler = Scheduler(owner)
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        st.warning(warning)
else:
    st.success("No task conflicts found.")

filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    selected_pet = st.selectbox(
        "Filter by pet",
        ["All pets", *[pet.name for pet in owner.pets]],
    )
with filter_col2:
    selected_status = st.selectbox(
        "Filter by status",
        ["All tasks", "Pending", "Completed"],
    )

filtered_tasks = scheduler.filter_tasks(
    pet_name=None if selected_pet == "All pets" else selected_pet,
    completed=(
        None
        if selected_status == "All tasks"
        else selected_status == "Completed"
    ),
)
sorted_tasks = sorted(filtered_tasks, key=lambda task: task.time)

if sorted_tasks:
    st.table(
        [
            {
                "Time": task.time,
                "Pet": task.pet_name,
                "Task": task.description,
                "Frequency": task.frequency,
                "Done": "yes" if task.completed else "no",
            }
            for task in sorted_tasks
        ]
    )
else:
    st.info("No tasks match these filters.")

pending_tasks = [task for task in sorted_tasks if not task.completed]
if pending_tasks:
    st.subheader("Mark a Task Complete")
    selected_task_index = st.selectbox(
        "Pending task",
        range(len(pending_tasks)),
        format_func=lambda index: (
            f"{pending_tasks[index].time} - {pending_tasks[index].pet_name}: "
            f"{pending_tasks[index].description}"
        ),
    )
    if st.button("Mark complete"):
        task = pending_tasks[selected_task_index]
        recurring = task.frequency in ("daily", "weekly")
        scheduler.mark_task_complete(task)
        if recurring:
            st.success("Task completed. The next occurrence was added.")
        else:
            st.success("Task completed.")
else:
    st.info("There are no pending tasks in this view to mark complete.")