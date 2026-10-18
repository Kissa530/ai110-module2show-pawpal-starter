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

After asking my AI assistant to review my skeleton, I made one change: I updated Pet.get_tasks() and Owner.get_all_tasks() to be annotated as returning list[Task] instead of None, since those methods are meant to give back tasks. The AI also suggested having the Scheduler get tasks through Owner.get_all_tasks() instead of looping over pets itself, and noted that I should clarify the Scheduler method signatures and decide what counts as a conflict. I didn’t change the skeleton for those, since they affect how I write the method bodies later, and I plan to follow them during implementation.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used my AI coding assistant across the whole build. In Phase 1 I used it to turn my brainstormed attributes and methods into a Mermaid class diagram and then into a dataclass skeleton, and I asked it to review that skeleton for missing relationships. In Phase 2 I used it in agent mode to implement the four classes in pawpal_system.py and to draft the pytest tests. I also used the AI to help me push the changes since it was rejecting at first due to the VS Code and the repo not being in sync.

- What kinds of prompts or questions were most helpful?

The most helpful prompts were specific ones that named the exact behavior I wanted. For example, I told it that Scheduler.sort_by_time() had to get its tasks through Owner.get_all_tasks(), which kept it from putting the pet-looping logic in the wrong place. Asking it to review a skeleton I had already written was also more useful than asking it to design from scratch, because I had something concrete to react to.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

The generated Task class had no default values, so creating a task meant passing description, time, frequency, completed, and due_date every time. I didn’t accept that as-is. I added defaults (frequency="once", completed=False, and due_date set to today) because the demo and tests became repetitive otherwise, and the defaults matched my UML. I also left filter_tasks(), detect_conflicts(), and mark_task_complete() as stubs instead of letting the AI build them early, since they belong to the algorithm phase.

- How did you evaluate or verify what the AI suggested?

To verify the AI’s work, I didn’t just trust its report that checks passed. I read the code to confirm the Scheduler goes through Owner.get_all_tasks(), ran python main.py with tasks added out of time order to check that both pets’ tasks printed sorted, and ran python -m pytest, which showed 2 passed.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
