"""Tiny, dependency-free task tracker for practicing Git pull requests."""

import argparse
import json
from pathlib import Path

DEFAULT_DATA_FILE = Path(__file__).with_name("tasks.json")


def read_state(data_file: Path = DEFAULT_DATA_FILE) -> dict:
    """Load tasks from disk or start with an empty task list."""
    if not data_file.exists():
        return {"next_id": 1, "tasks": []}
    return json.loads(data_file.read_text(encoding="utf-8"))


def write_state(state: dict, data_file: Path = DEFAULT_DATA_FILE) -> None:
    """Save the task list as readable JSON."""
    data_file.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def add_task(title: str, data_file: Path = DEFAULT_DATA_FILE) -> dict:
    """Create a task and return it."""
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty")
    state = read_state(data_file)
    task = {"id": state["next_id"], "title": title, "done": False}
    state["tasks"].append(task)
    state["next_id"] += 1
    write_state(state, data_file)
    return task


def get_tasks(data_file: Path = DEFAULT_DATA_FILE) -> list[dict]:
    """Return all tasks."""
    return read_state(data_file)["tasks"]


def mark_done(task_id: int, data_file: Path = DEFAULT_DATA_FILE) -> dict:
    """Complete a task by its numeric ID."""
    state = read_state(data_file)
    for task in state["tasks"]:
        if task["id"] == task_id:
            task["done"] = True
            write_state(state, data_file)
            return task
    raise ValueError(f"Task #{task_id} not found")

def delete_task(task_id: int, data_file: Path = DEFAULT_DATA_FILE) -> dict:
    """Delete a task by ID, returning the deleted task."""
    state = read_state(data_file)

    for index, task in enumerate(state["tasks"]):
        if task["id"] == task_id:
            deleted = state["tasks"].pop(index)
            write_state(state, data_file)
            return deleted

    raise ValueError(f"Task #{task_id} not found")

# CONTRIBUTOR CHALLENGE #1:
# Add delete_task(task_id, data_file), a "delete" CLI subcommand,
# and tests for deleting an existing or missing task.


def main() -> None:
    parser = argparse.ArgumentParser(description="Mini Task Tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title")
    subparsers.add_parser("list", help="Show all tasks")
    done_parser = subparsers.add_parser("done", help="Complete a task")
    done_parser.add_argument("id", type=int)
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int)

    args = parser.parse_args()
    try:
        if args.command == "add":
            task = add_task(args.title)
            print(f"Added #{task['id']}: {task['title']}")
        elif args.command == "list":
            tasks = get_tasks()
            if not tasks:
                print("No tasks yet. Add one with: python taskboard.py add \"My task\"")
            for task in tasks:
                marker = "x" if task["done"] else " "
                print(f"[{marker}] #{task['id']} {task['title']}")
        elif args.command == "done":
            task = mark_done(args.id)
            print(f"Completed #{task['id']}: {task['title']}")
        elif args.command == "delete":
            task = delete_task(args.id)
            print(f"Deleted #{task['id']}: {task['title']}")
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
