# import streamlit as st
# from pawpal_system import Owner, Pet, Task, Scheduler

# if "owner" not in st.session_state:
#     st.session_state.owner = Owner("Jordan")

# owner = st.session_state.owner

# st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# st.title("🐾 PawPal+")

# st.markdown(
#     """
# Welcome to the PawPal+ starter app.

# This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
# but **it does not implement the project logic**. Your job is to design the system and build it.

# Use this app as your interactive demo once your backend classes/functions exist.
# """
# )

# with st.expander("Scenario", expanded=True):
#     st.markdown(
#         """
# **PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
# for their pet(s) based on constraints like time, priority, and preferences.

# You will design and implement the scheduling logic and connect it to this Streamlit UI.
# """
#     )

# with st.expander("What you need to build", expanded=True):
#     st.markdown(
#         """
# At minimum, your system should:
# - Represent pet care tasks (what needs to happen, how long it takes, priority)
# - Represent the pet and the owner (basic info and preferences)
# - Build a plan/schedule for a day that chooses and orders tasks based on constraints
# - Explain the plan (why each task was chosen and when it happens)
# """
#     )

# st.divider()

# st.subheader("Quick Demo Inputs (UI only)")
# owner_name = st.text_input("Owner name", value="Jordan")
# pet_name = st.text_input("Pet name", value="Mochi")
# species = st.selectbox("Species", ["dog", "cat", "other"])

# st.markdown("### Tasks")
# st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

# if "tasks" not in st.session_state:
#     st.session_state.tasks = []

# col1, col2, col3 = st.columns(3)
# with col1:
#     task_title = st.text_input("Task title", value="Morning walk")
# with col2:
#     duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
# with col3:
#     priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

# if st.button("Add task"):
#     st.session_state.tasks.append(
#         {"title": task_title, "duration_minutes": int(duration), "priority": priority}
#     )

# if st.session_state.tasks:
#     st.write("Current tasks:")
#     st.table(st.session_state.tasks)
# else:
#     st.info("No tasks yet. Add one above.")

# st.divider()

# st.subheader("Build Schedule")
# st.caption("This button should call your scheduling logic once you implement it.")

# if st.button("Generate schedule"):
#     st.warning(
#         "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
#     )
#     st.markdown(
#         """
# Suggested approach:
# 1. Design your UML (draft).
# 2. Create class stubs (no logic).
# 3. Implement scheduling behavior.
# 4. Connect your scheduler here and display results.
# """
#     )

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
sorted_tasks = scheduler.sort_by_time()

if sorted_tasks:
    pet_names_by_task_id = {
        id(task): pet.name for pet in owner.pets for task in pet.get_tasks()
    }
    st.table(
        [
            {
                "Time": task.time,
                "Pet": pet_names_by_task_id[id(task)],
                "Task": task.description,
                "Frequency": task.frequency,
                "Done": "yes" if task.completed else "no",
            }
            for task in sorted_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")