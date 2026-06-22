#!/usr/bin/env python3
"""A simple TODO list CLI."""

import argparse
import json
import sys
from pathlib import Path

TODO_FILE = Path.home() / ".todos.json"


def load_todos() -> list:
    """Load todos from file."""
    if TODO_FILE.exists():
        return json.loads(TODO_FILE.read_text())
    return []


def save_todos(todos: list) -> None:
    """Save todos to file."""
    TODO_FILE.write_text(json.dumps(todos))


def add_todo(text: str) -> None:
    """Add a new todo."""
    todos = load_todos()
    todos.append({"text": text, "done": False})
    save_todos(todos)
    print(f"Added: {text}")


def list_todos() -> None:
    """List all todos."""
    todos = load_todos()
    if not todos:
        print("No todos yet!")
        return
    for i, todo in enumerate(todos, 1):
        status = "x" if todo["done"] else " "
        print(f"[{status}] {i}. {todo['text']}")


def done_todo(task_id: int) -> int:
    """Mark a todo as done by 1-based ID. Returns exit code."""
    todos = load_todos()
    if task_id < 1 or task_id > len(todos):
        print(f"Error: Invalid task ID {task_id}", file=sys.stderr)
        return 1
    todo = todos[task_id - 1]
    if todo["done"]:
        print(f"Already done: {todo['text']}")
    else:
        todo["done"] = True
        save_todos(todos)
        print(f"Completed: {todo['text']}")
    return 0


def remove_todo(task_id: int) -> int:
    """Remove a todo by 1-based ID. Returns exit code."""
    todos = load_todos()
    if task_id < 1 or task_id > len(todos):
        print(f"Error: Invalid task ID {task_id}", file=sys.stderr)
        return 1
    todo = todos.pop(task_id - 1)
    save_todos(todos)
    print(f"Removed: {todo['text']}")
    return 0


def clear_todos() -> None:
    """Clear all completed todos."""
    todos = load_todos()
    completed_count = sum(1 for t in todos if t["done"])
    if completed_count == 0:
        print("No completed todos to clear")
        return
    todos = [t for t in todos if not t["done"]]
    save_todos(todos)
    print(f"Cleared {completed_count} completed todos")


def main() -> int:
    """Main entry point. Returns exit code."""
    parser = argparse.ArgumentParser(description="Simple TODO list CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add command
    add_parser = subparsers.add_parser("add", help="Add a new todo")
    add_parser.add_argument("text", nargs="+", help="The todo text")

    # list command
    subparsers.add_parser("list", help="List all todos")

    # done command
    done_parser = subparsers.add_parser("done", help="Mark a todo as done")
    done_parser.add_argument("id", type=int, help="The todo ID to mark as done")

    # remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a todo")
    remove_parser.add_argument("id", type=int, help="The todo ID to remove")

    # clear command
    subparsers.add_parser("clear", help="Clear all completed todos")

    args = parser.parse_args()

    if args.command == "add":
        add_todo(" ".join(args.text))
        return 0
    elif args.command == "list":
        list_todos()
        return 0
    elif args.command == "done":
        return done_todo(args.id)
    elif args.command == "remove":
        return remove_todo(args.id)
    elif args.command == "clear":
        clear_todos()
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
