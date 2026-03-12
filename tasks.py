"""
TaskFlow - Week 2: Core Concepts
Simple task manager using Python data structures.
"""

from datetime import datetime


class Task:
    """Represents a single task."""

    def __init__(self, title: str, priority: str = "medium", category: str = "general"):
        self.id = id(self)  # unique identifier
        self.title = title
        self.priority = priority      # low / medium / high
        self.category = category
        self.done = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def complete(self):
        self.done = True

    def __repr__(self):
        status = "✅" if self.done else "⬜"
        return f"[{status}] ({self.priority.upper()}) {self.title}  [{self.category}]"


class TaskManager:
    """Manages a collection of tasks."""

    def __init__(self):
        self._tasks: list[Task] = []

    # ── CREATE
    def add(self, title: str, priority: str = "medium", category: str = "general") -> Task:
        if not title.strip():
            raise ValueError("Task title cannot be empty.")
        task = Task(title.strip(), priority, category)
        self._tasks.append(task)
        print(f"Added: {task}")
        return task

    #  READ 
    def list_all(self) -> list[Task]:
        return self._tasks

    def get_by_id(self, task_id: int) -> Task | None:
        return next((t for t in self._tasks if t.id == task_id), None)

    def filter(self, done: bool | None = None, priority: str | None = None) -> list[Task]:
        result = self._tasks
        if done is not None:
            result = [t for t in result if t.done == done]
        if priority:
            result = [t for t in result if t.priority == priority]
        return result

    # UPDATE 
    def complete(self, task_id: int) -> bool:
        task = self.get_by_id(task_id)
        if task:
            task.complete()
            print(f"Completed: {task}")
            return True
        print(f"Task {task_id} not found.")
        return False

    def update_title(self, task_id: int, new_title: str) -> bool:
        task = self.get_by_id(task_id)
        if task:
            task.title = new_title.strip()
            print(f"Updated title: {task}")
            return True
        return False

    #  DELETE 
    def delete(self, task_id: int) -> bool:
        task = self.get_by_id(task_id)
        if task:
            self._tasks.remove(task)
            print(f"Deleted task: {task.title}")
            return True
        return False

    #  DISPLAY 
    def display(self):
        if not self._tasks:
            print("No tasks yet.")
            return
        print(f"\n{'─'*50}")
        print(f"  TaskFlow — {len(self._tasks)} task(s)")
        print(f"{'─'*50}")
        for task in self._tasks:
            print(f"  {task}")
        pending = len(self.filter(done=False))
        print(f"{'─'*50}")
        print(f"  {pending} pending  |  {len(self._tasks) - pending} done\n")


# Quick demo 
if __name__ == "__main__":
    tm = TaskManager()

    tm.add("Set up dev environment", priority="high", category="setup")
    tm.add("Read Flask documentation", priority="medium", category="learning")
    tm.add("Design database schema", priority="high", category="backend")
    tm.add("Write unit tests", priority="low", category="testing")

    tm.display()

    # complete the first task
    first_id = tm.list_all()[0].id
    tm.complete(first_id)

    # filter — show only pending
    print("Pending tasks:")
    for t in tm.filter(done=False):
        print(f"  {t}")
