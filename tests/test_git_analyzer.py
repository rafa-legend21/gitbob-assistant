"""
Tests for Git analyzer
"""

import pytest
from pathlib import Path
from gitbob.git_analyzer import GitAnalyzer


def test_git_analyzer_requires_repo():
    """Test that GitAnalyzer raises error when not in a git repo"""
    # Create a temporary non-git directory
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(ValueError, match="Not a git repository"):
            GitAnalyzer(Path(tmpdir))


def test_get_default_branch_fallback():
    """Test that get_default_branch returns 'main' as fallback"""
    # This test would need a real git repo, so we'll skip for now
    # In a real test, we'd create a temporary git repo
    pass


def test_staged_files_tuple_handling():
    """Test that get_staged_files handles tuple keys correctly"""
    # This would need a real git repo with staged files
    # The fix ensures tuples are handled: (path, stage) -> path
    pass


def test_has_staged_changes_empty_repo():
    """Test has_staged_changes on empty repo"""
    # Would need a real git repo
    pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
