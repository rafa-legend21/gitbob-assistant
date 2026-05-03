"""
Prompt templates for IBM Bob API
"""

from typing import Dict, List


class PromptTemplates:
    """Collection of prompt templates for different GitBob features"""
    
    @staticmethod
    def commit_message(diff_content: str, file_changes: List[str]) -> str:
        """Generate prompt for commit message generation
        
        Args:
            diff_content: Git diff output
            file_changes: List of changed files
            
        Returns:
            Formatted prompt for IBM Bob
        """
        files_summary = "\n".join([f"- {file}" for file in file_changes])
        
        return f"""You are a senior software developer writing a commit message. Analyze the following git diff and generate a conventional commit message.

Files changed:
{files_summary}

Diff:
{diff_content}

Requirements:
- Use conventional commit format: type(scope): subject
- Types: feat, fix, docs, style, refactor, test, chore
- Keep subject line under 72 characters
- Add bullet points for detailed changes in the body
- Be specific and technical
- Focus on what changed and why, not how
- Use imperative mood (e.g., "add" not "added")

Generate a commit message following this format:

type(scope): brief description

- Detailed change 1
- Detailed change 2
- Detailed change 3

Only output the commit message, nothing else."""
    
    @staticmethod
    def branch_name(description: str, current_branch: str, recent_commits: List[str]) -> str:
        """Generate prompt for branch name suggestion
        
        Args:
            description: User's description of the work
            current_branch: Current branch name
            recent_commits: List of recent commit messages
            
        Returns:
            Formatted prompt for IBM Bob
        """
        commits_summary = "\n".join([f"- {commit}" for commit in recent_commits[:5]])
        
        return f"""Generate git branch names based on the following information:

Work description: {description}

Current branch: {current_branch}

Recent commits:
{commits_summary}

Requirements:
- Use kebab-case (lowercase with hyphens)
- Include appropriate prefix: feature/, bugfix/, hotfix/, chore/, docs/, refactor/
- Keep under 50 characters total
- Be descriptive but concise
- Use clear, meaningful words
- Avoid abbreviations unless commonly understood

Generate exactly 3 branch name options, one per line, in this format:
1. branch-name-option-1
2. branch-name-option-2
3. branch-name-option-3

Only output the 3 numbered branch names, nothing else."""
    
    @staticmethod
    def pr_description(
        commits: List[Dict[str, str]], 
        file_changes: List[str],
        base_branch: str,
        current_branch: str
    ) -> str:
        """Generate prompt for PR description
        
        Args:
            commits: List of commit dictionaries with 'hash', 'message', 'author'
            file_changes: List of changed files
            base_branch: Base branch name
            current_branch: Current branch name
            
        Returns:
            Formatted prompt for IBM Bob
        """
        commits_summary = "\n".join([
            f"- {commit['hash'][:7]}: {commit['message']}" 
            for commit in commits
        ])
        
        files_summary = "\n".join([f"- {file}" for file in file_changes])
        
        return f"""Generate a comprehensive pull request description based on the following information:

Branch: {current_branch} → {base_branch}

Commits:
{commits_summary}

Files changed:
{files_summary}

Requirements:
- Use markdown formatting
- Include these sections: Summary, Changes, Testing, Related Issues
- Summary: 2-3 sentences explaining the overall purpose
- Changes: Bullet points of key changes (be specific)
- Testing: How the changes were tested
- Related Issues: Reference any issue numbers found in commits (e.g., "Closes #123")
- Be comprehensive but concise
- Use technical language appropriate for code review
- Highlight any breaking changes or important notes

Generate the PR description in markdown format:

## Summary
[2-3 sentence summary]

## Changes
- [Key change 1]
- [Key change 2]
- [Key change 3]

## Testing
- [Testing approach]

## Related Issues
[Issue references or "None"]

Only output the markdown PR description, nothing else."""
    
    @staticmethod
    def analyze_changes(diff_content: str) -> str:
        """Generate prompt for analyzing code changes
        
        Args:
            diff_content: Git diff output
            
        Returns:
            Formatted prompt for IBM Bob
        """
        return f"""Analyze the following git diff and provide a concise summary of the changes:

{diff_content}

Provide:
1. Overall purpose of the changes (1 sentence)
2. Key modifications (3-5 bullet points)
3. Potential impact areas

Keep the analysis technical and focused on what changed."""
    
    @staticmethod
    def suggest_scope(file_changes: List[str]) -> str:
        """Generate prompt for suggesting commit scope
        
        Args:
            file_changes: List of changed files
            
        Returns:
            Formatted prompt for IBM Bob
        """
        files_summary = "\n".join([f"- {file}" for file in file_changes])
        
        return f"""Based on the following changed files, suggest an appropriate scope for a conventional commit:

Files changed:
{files_summary}

Common scopes include: api, ui, auth, db, config, docs, test, core, utils

Suggest the most appropriate scope (single word, lowercase). Only output the scope word, nothing else."""


def truncate_diff(diff_content: str, max_lines: int = 500) -> str:
    """Truncate diff content if too large
    
    Args:
        diff_content: Full diff content
        max_lines: Maximum number of lines to include
        
    Returns:
        Truncated diff with summary if needed
    """
    lines = diff_content.split('\n')
    
    if len(lines) <= max_lines:
        return diff_content
    
    truncated = '\n'.join(lines[:max_lines])
    remaining = len(lines) - max_lines
    
    return f"{truncated}\n\n... ({remaining} more lines truncated for brevity)"


def format_file_changes(files: List[str], max_files: int = 20) -> List[str]:
    """Format and limit file changes list
    
    Args:
        files: List of file paths
        max_files: Maximum number of files to include
        
    Returns:
        Formatted list of file changes
    """
    if len(files) <= max_files:
        return files
    
    shown_files = files[:max_files]
    remaining = len(files) - max_files
    shown_files.append(f"... and {remaining} more files")
    
    return shown_files

# Made with Bob
