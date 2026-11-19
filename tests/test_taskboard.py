"""Tests for existing features; contributors add tests for new features."""

import tempfile
import unittest
from pathlib import Path

from taskboard import add_task, get_tasks, mark_done


class TaskboardTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "tasks.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_starts_empty(self):
        self.assertEqual(get_tasks(self.data_file), [])

    def test_add_creates_task(self):
        task = add_task("Learn Git", self.data_file)
        self.assertEqual(task["id"], 1)
        self.assertEqual(task["title"], "Learn Git")
        self.assertFalse(task["done"])
        self.assertEqual(len(get_tasks(self.data_file)), 1)

    def test_add_rejects_blank_title(self):
        with self.assertRaises(ValueError):
            add_task("   ", self.data_file)

    def test_done_marks_task_complete(self):
        add_task("Open a PR", self.data_file)
        updated = mark_done(1, self.data_file)
        self.assertTrue(updated["done"])
        self.assertTrue(get_tasks(self.data_file)[0]["done"])

    def test_done_unknown_id_raises(self):
        with self.assertRaises(ValueError):
            mark_done(999, self.data_file)

    def test_ids_are_stable_across_additions(self):
        add_task("First", self.data_file)
        second = add_task("Second", self.data_file)
        self.assertEqual(second["id"], 2)


if __name__ == "__main__":
    unittest.main()
