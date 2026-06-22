"""Tests for the TODO CLI."""

import json
import sys

import pytest

import todo


@pytest.fixture(autouse=True)
def isolate_todo_file(tmp_path, monkeypatch):
    """Redirect TODO_FILE to a temp location for each test."""
    test_file = tmp_path / "test_todos.json"
    monkeypatch.setattr(todo, "TODO_FILE", test_file)
    return test_file


class TestAddTodo:
    """Tests for the add command."""

    def test_add_todo(self, capsys, isolate_todo_file):
        """Add a todo and verify it appears in storage and stdout."""
        todo.add_todo("Buy groceries")

        captured = capsys.readouterr()
        assert "Added: Buy groceries" in captured.out

        # Verify storage
        todos = json.loads(isolate_todo_file.read_text())
        assert len(todos) == 1
        assert todos[0]["text"] == "Buy groceries"
        assert todos[0]["done"] is False

    def test_add_multiple_words(self, capsys, isolate_todo_file):
        """Add a todo with multiple words."""
        todo.add_todo("Buy milk and eggs")

        captured = capsys.readouterr()
        assert "Added: Buy milk and eggs" in captured.out

        todos = json.loads(isolate_todo_file.read_text())
        assert todos[0]["text"] == "Buy milk and eggs"


class TestListTodos:
    """Tests for the list command."""

    def test_list_empty(self, capsys):
        """List with no todos shows appropriate message."""
        todo.list_todos()

        captured = capsys.readouterr()
        assert "No todos yet!" in captured.out

    def test_list_with_todos(self, capsys, isolate_todo_file):
        """List with todos shows numbered output format."""
        todo.add_todo("First task")
        todo.add_todo("Second task")
        capsys.readouterr()  # Clear add output

        todo.list_todos()

        captured = capsys.readouterr()
        assert "[ ] 1. First task" in captured.out
        assert "[ ] 2. Second task" in captured.out


class TestDoneTodo:
    """Tests for the done command."""

    def test_done_valid(self, capsys, isolate_todo_file):
        """Mark a todo as done and verify status changes."""
        todo.add_todo("Task to complete")
        capsys.readouterr()

        exit_code = todo.done_todo(1)

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Completed: Task to complete" in captured.out

        todos = json.loads(isolate_todo_file.read_text())
        assert todos[0]["done"] is True

    def test_done_invalid_id(self, capsys):
        """Try to mark non-existent ID, verify error message and exit code."""
        exit_code = todo.done_todo(99)

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Error: Invalid task ID 99" in captured.err

    def test_done_already_done(self, capsys, isolate_todo_file):
        """Mark same todo done twice, verify no error."""
        todo.add_todo("Task to complete")
        capsys.readouterr()

        todo.done_todo(1)
        capsys.readouterr()

        exit_code = todo.done_todo(1)

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Already done: Task to complete" in captured.out


class TestRemoveTodo:
    """Tests for the remove command."""

    def test_remove_valid(self, capsys, isolate_todo_file):
        """Add todo, remove it, verify it's gone from storage."""
        todo.add_todo("Task to remove")
        capsys.readouterr()

        exit_code = todo.remove_todo(1)

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Removed: Task to remove" in captured.out

        todos = json.loads(isolate_todo_file.read_text())
        assert len(todos) == 0

    def test_remove_invalid_id(self, capsys):
        """Try to remove non-existent ID, verify error."""
        exit_code = todo.remove_todo(99)

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Error: Invalid task ID 99" in captured.err


class TestClearTodos:
    """Tests for the clear command."""

    def test_clear_with_completed(self, capsys, isolate_todo_file):
        """Add todos, complete some, clear, verify only incomplete remain."""
        todo.add_todo("Keep this")
        todo.add_todo("Complete this")
        todo.add_todo("Also keep this")
        todo.done_todo(2)
        capsys.readouterr()

        todo.clear_todos()

        captured = capsys.readouterr()
        assert "Cleared 1 completed todos" in captured.out

        todos = json.loads(isolate_todo_file.read_text())
        assert len(todos) == 2
        assert todos[0]["text"] == "Keep this"
        assert todos[1]["text"] == "Also keep this"

    def test_clear_none_completed(self, capsys, isolate_todo_file):
        """Clear with no completed todos, verify message."""
        todo.add_todo("Not completed")
        capsys.readouterr()

        todo.clear_todos()

        captured = capsys.readouterr()
        assert "No completed todos to clear" in captured.out


class TestMainCLI:
    """Integration tests for the main CLI entry point."""

    def test_main_add(self, monkeypatch, capsys):
        """Test main() with add command."""
        monkeypatch.setattr(sys, "argv", ["todo", "add", "New", "task"])

        exit_code = todo.main()

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Added: New task" in captured.out

    def test_main_list(self, monkeypatch, capsys):
        """Test main() with list command."""
        monkeypatch.setattr(sys, "argv", ["todo", "list"])

        exit_code = todo.main()

        assert exit_code == 0

    def test_main_done_invalid(self, monkeypatch, capsys):
        """Test main() with done command on invalid ID."""
        monkeypatch.setattr(sys, "argv", ["todo", "done", "99"])

        exit_code = todo.main()

        assert exit_code == 1

    def test_main_remove_invalid(self, monkeypatch, capsys):
        """Test main() with remove command on invalid ID."""
        monkeypatch.setattr(sys, "argv", ["todo", "remove", "99"])

        exit_code = todo.main()

        assert exit_code == 1

    def test_main_clear(self, monkeypatch, capsys):
        """Test main() with clear command."""
        monkeypatch.setattr(sys, "argv", ["todo", "clear"])

        exit_code = todo.main()

        assert exit_code == 0
