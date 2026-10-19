# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

  Add a pet. The owner enters a pet’s basic details (name, species) so the app can track care for each animal.
Schedule a care task for a pet. The owner picks a pet and creates a task such as a walk, feeding, or medication, with a time and how often it repeats (once, daily, or weekly).
View today’s schedule. The owner sees every task across all their pets in one list, ordered by time, and can mark tasks complete.

Core actions: add a pet, schedule a task for a pet, view today’s tasks across all pets in time order.
Task: represents one care activity (description, time, frequency, completion status). It only knows about itself and can mark itself complete.
Pet: stores a pet’s details and owns a list of its tasks.
Owner: manages multiple pets and can return every task across all of them through get_all_tasks().
Scheduler: the “brain.” It reads tasks through the Owner and handles sorting, filtering, conflict detection, and completing tasks.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After asking my AI assistant to review my skeleton, I changed the return types of Pet.get_tasks() and Owner.get_all_tasks() from None to list[Task]. During the algorithm phase the design changed further. I added a pet_name field to Task, set automatically by Pet.add_task(), so the scheduler could filter by pet and put a recurring task’s next occurrence on the right pet. Sorting and conflict checks also use the due date as well as the time, so tomorrow’s copy of a recurring task doesn’t conflict with today’s. I kept the AI’s suggestion that the Scheduler read tasks through Owner.get_all_tasks() instead of looping over pets itself.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

My scheduler considers four things: the time of day (HH:MM), the due date, whether a task is completed, and how often it repeats (once, daily, or weekly). It orders tasks by due date and then time, ignores completed tasks when looking for conflicts, and creates the next occurrence of daily and weekly tasks automatically. 

- How did you decide which constraints mattered most?

 I decided time mattered most because a pet owner mainly needs to know what to do next and when, and double-booked times are the most obvious problem to warn about. I left out priority and duration to keep the system simple and readable, since the core scenario works without them.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

My scheduler only flags two tasks as conflicting when they have exactly the same date and time. Tasks have no duration, so it can’t tell that a walk at 07:00 that lasts an hour overlaps with a task at 07:30. 


- Why is that tradeoff reasonable for this scenario?


This tradeoff is reasonable because exact matching is simple, easy to test, and enough to warn an owner about obvious double-booking. Catching real overlaps would need a duration field and a comparison of time ranges, which would add complexity this project doesn’t need yet.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used my AI coding assistant across the whole build. In Phase 1 I used it to turn my brainstormed attributes and methods into a Mermaid class diagram and then into a dataclass skeleton, and I asked it to review that skeleton for missing relationships. In Phase 2 I used it in agent mode to implement the four classes in pawpal_system.py and to draft the pytest tests. In Phase 4 I used a separate chat to plan the algorithms, and agent mode to add recurring tasks across pawpal_system.py and main.py. In Phase 5 I asked it to explain each test before I kept it. In Phase 6 I used it to connect the Streamlit app to the scheduler, update the UML, and polish the README. I also used it to debug git when my pushes were rejected because VS Code and the GitHub repo were out of sync.

Agent mode was the most effective feature because it could edit several files together, and attaching my real files meant it worked from my actual code instead of guessing. Using a separate chat for planning each phase kept every conversation focused on one job. That kept things more organized.

- What kinds of prompts or questions were most helpful?

The most helpful prompts were specific ones that named the exact behavior I wanted. For example, I told it that Scheduler.sort_by_time() had to get its tasks through Owner.get_all_tasks(), which kept it from putting the pet-looping logic in the wrong place. Asking it to review a skeleton I had already written was also more useful than asking it to design from scratch, because I had something concrete to react to.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

The generated Task class had no default values, so creating a task meant passing description, time, frequency, completed, and due_date every time. I didn’t accept that as-is. I added defaults (frequency="once", completed=False, and due_date set to today) because the demo and tests became repetitive otherwise, and the defaults matched my UML. I also left filter_tasks(), detect_conflicts(), and mark_task_complete() as stubs instead of letting the AI build them early, since they belong to the algorithm phase.

- How did you evaluate or verify what the AI suggested?

To verify the AI’s work, I didn’t just trust its report that checks passed. I read the code to confirm the Scheduler goes through Owner.get_all_tasks(), ran python main.py with tasks added out of time order to check that both pets’ tasks printed sorted, and ran python -m pytest, which showed 11 passed.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I wrote 11 pytest tests covering the behaviors the scheduler depends on most. They check that tasks added out of order come back in chronological order across pets, that completing a daily task creates a copy for the next day on the same pet (and a weekly task one 7 days later, with a one-time task creating none), and that conflict detection flags pending tasks at the same date and time while ignoring completed tasks and tasks on different dates. I also tested edge cases: an owner or pet with no tasks, and filtering by a pet name that doesn’t exist.


- Why were these tests important?

Sorting, recurrence, and conflict detection are the logic the UI relies on, and they're the easiest places for quiet bugs to hide. A wrong sort order, a recurring task added to the wrong pet, or a false conflict warning would all look fine at a glance and only show up when someone used the app.

**b. Confidence**

- How confident are you that your scheduler works correctly?

I’m fairly confident, about 4 out of 5, because all 11 tests pass and I also checked the behavior by running main.py and the Streamlit app. I held back a star because the tests don’t cover everything.

- What edge cases would you test next if you had more time?

 If I had more time, I’d test times that aren’t zero-padded (like 1:00, which I found sorts incorrectly), a task with a frequency other than once, daily, or weekly, a recurring task whose pet can’t be found, tasks with equal times staying in the order they were added, and filtering with both a pet and a status at once. I’d also add a check for a month-end recurrence date.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I’m most satisfied with how the Scheduler works across pets. Owner.get_all_tasks() collects every pet’s tasks in one place, so sorting, filtering, and conflict detection all build on it without repeating the loop. I’m also happy that I built and tested the logic in the terminal first, so when I connected it to the Streamlit app, everything already worked and the UI only had to call my methods.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I’d add task duration and priority so conflict detection could catch overlapping tasks instead of only exact matches, and so the scheduler could do more than order tasks by time. I’d also store times as real time objects or normalize them on input, so a time like 1:00 can’t sort in the wrong place. The app also loses everything when it restarts, since data only lives in session state, so saving pets and tasks to a file would make it more useful. Finally, I’d let users edit or delete tasks.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The most important thing I learned is that working with AI means checking its work instead of trusting it. The assistant wrote a lot of useful code, but I found problems by testing it myself. When I tried a time like 1:00 in the app, I found that it sorted in the wrong place, because the times are stored as text. When I asked the assistant to explain my tests, it pointed out that one conflict test would pass even if conflict detection never fired, so I learned to ask whether a test could actually fail. The design decisions stayed mine: what the classes are, that the Scheduler reads through the Owner, and what a conflict means. The assistant was fastest when I gave it small, specific tasks and then verified each result.