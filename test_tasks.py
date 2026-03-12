"""
TaskFlow - Week 5: Testing
Unit tests for core task logic using Python's built-in unittest.
Run with: python -m pytest test_tasks.py -v
"""

import unittest
import sys
import os


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "week2"))
from tasks import Task, TaskManager


class TestTask(unittest.TestCase):

    def test_task_created_with_defaults(self):
        task = Task("Write tests")
        self.assertEqual(task.title, "Write tests")
        self.assertEqual(task.priority, "medium")
        self.assertEqual(task.category, "general")
        self.assertFalse(task.done)

    def test_task_complete_sets_done_true(self):
        task = Task("Deploy app")
        task.complete()
        self.assertTrue(task.done)

    def test_task_repr_contains_title(self):
        task = Task("Review PR")
        self.assertIn("Review PR", repr(task))


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        """Fresh manager for each test."""
        self.tm = TaskManager()

    def test_add_task_increases_count(self):
        self.tm.add("Task A")
        self.tm.add("Task B")
        self.assertEqual(len(self.tm.list_all()), 2)

    def test_add_empty_title_raises(self):
        with self.assertRaises(ValueError):
            self.tm.add("   ")

    def test_complete_task_marks_done(self):
        task = self.tm.add("Fix bug")
        self.tm.complete(task.id)
        self.assertTrue(task.done)

    def test_complete_nonexistent_returns_false(self):
        result = self.tm.complete(9999)
        self.assertFalse(result)

    def test_delete_task_removes_it(self):
        task = self.tm.add("Old task")
        self.tm.delete(task.id)
        self.assertIsNone(self.tm.get_by_id(task.id))

    def test_filter_by_done(self):
        t1 = self.tm.add("Task 1")
        t2 = self.tm.add("Task 2")
        self.tm.complete(t1.id)
        pending = self.tm.filter(done=False)
        done = self.tm.filter(done=True)
        self.assertIn(t2, pending)
        self.assertIn(t1, done)

    def test_filter_by_priority(self):
        self.tm.add("Urgent", priority="high")
        self.tm.add("Chill task", priority="low")
        high = self.tm.filter(priority="high")
        self.assertEqual(len(high), 1)
        self.assertEqual(high[0].title, "Urgent")

    def test_update_title(self):
        task = self.tm.add("Old title")
        self.tm.update_title(task.id, "New title")
        self.assertEqual(task.title, "New title")

    def test_list_all_returns_all(self):
        for i in range(5):
            self.tm.add(f"Task {i}")
        self.assertEqual(len(self.tm.list_all()), 5)


if __name__ == "__main__":
    unittest.main()
