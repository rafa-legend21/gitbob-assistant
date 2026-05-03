"""
Tests for prompt templates
"""

import pytest
from gitbob.prompts import PromptTemplates, truncate_diff, format_file_changes


def test_commit_message_prompt():
    """Test commit message prompt generation"""
    diff = "+++ b/auth.py\n+def login():\n+    pass"
    files = ["auth.py", "config.py"]
    
    prompt = PromptTemplates.commit_message(diff, files)
    
    assert "conventional commit" in prompt.lower()
    assert "auth.py" in prompt
    assert "config.py" in prompt
    assert diff in prompt


def test_branch_name_prompt():
    """Test branch name prompt generation"""
    description = "add user authentication"
    current_branch = "main"
    commits = ["Initial commit", "Add config"]
    
    prompt = PromptTemplates.branch_name(description, current_branch, commits)
    
    assert description in prompt
    assert current_branch in prompt
    assert "kebab-case" in prompt.lower()


def test_pr_description_prompt():
    """Test PR description prompt generation"""
    commits = [
        {"hash": "abc123", "message": "feat: add login", "author": "John"},
        {"hash": "def456", "message": "fix: bug in auth", "author": "Jane"},
    ]
    files = ["auth.py", "login.py"]
    
    prompt = PromptTemplates.pr_description(commits, files, "main", "feature/auth")
    
    assert "abc123" in prompt
    assert "def456" in prompt
    assert "auth.py" in prompt
    assert "Summary" in prompt


def test_truncate_diff():
    """Test diff truncation"""
    # Short diff - should not truncate
    short_diff = "\n".join([f"line {i}" for i in range(100)])
    result = truncate_diff(short_diff, max_lines=500)
    assert result == short_diff
    
    # Long diff - should truncate
    long_diff = "\n".join([f"line {i}" for i in range(1000)])
    result = truncate_diff(long_diff, max_lines=500)
    assert len(result.split('\n')) < 1000
    assert "truncated" in result.lower()


def test_format_file_changes():
    """Test file changes formatting"""
    # Few files - should not truncate
    few_files = ["file1.py", "file2.py", "file3.py"]
    result = format_file_changes(few_files, max_files=20)
    assert len(result) == 3
    
    # Many files - should truncate
    many_files = [f"file{i}.py" for i in range(50)]
    result = format_file_changes(many_files, max_files=20)
    assert len(result) == 21  # 20 files + 1 summary line
    assert "more files" in result[-1]

# Made with Bob
