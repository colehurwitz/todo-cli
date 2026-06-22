#!/usr/bin/env python3
"""A simple TODO list CLI - basic version with only add and list."""

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


def done_todo(task_id: int) -> None:
    """Mark a todo as done by 1-based ID."""
    todos = load_todos()
    if task_id < 1 or task_id > len(todos):
        print(f"Error: Invalid task ID {task_id}")
        sys.exit(1)
    todo = todos[task_id - 1]
    if todo["done"]:
        print(f"Already done: {todo['text']}")
    else:
        todo["done"] = True
        save_todos(todos)
        print(f"Completed: {todo['text']}")


def remove_todo(task_id: int) -> None:
    """Remove a todo by 1-based ID."""
    todos = load_todos()
    if task_id < 1 or task_id > len(todos):
        print(f"Error: Invalid task ID {task_id}")
        sys.exit(1)
    todo = todos.pop(task_id - 1)
    save_todos(todos)
    print(f"Removed: {todo['text']}")


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


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: todo.py <command> [args]")
        print("Commands: add <text>, list, done <id>, remove <id>, clear")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: add requires text")
            sys.exit(1)
        add_todo(" ".join(sys.argv[2:]))
    elif command == "list":
        list_todos()
    elif command == "done":
        if len(sys.argv) < 3:
            print("Error: done requires a task ID")
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print(f"Error: Invalid task ID '{sys.argv[2]}' - must be a number")
            sys.exit(1)
        done_todo(task_id)
    elif command == "remove":
        if len(sys.argv) < 3:
            print("Error: remove requires a task ID")
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print(f"Error: Invalid task ID '{sys.argv[2]}' - must be a number")
            sys.exit(1)
        remove_todo(task_id)
    elif command == "clear":
        clear_todos()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
