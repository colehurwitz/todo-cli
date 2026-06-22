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


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: todo.py <command> [args]")
        print("Commands: add <text>, list")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: add requires text")
            sys.exit(1)
        add_todo(" ".join(sys.argv[2:]))
    elif command == "list":
        list_todos()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
