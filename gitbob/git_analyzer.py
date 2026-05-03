"""
Git repository analysis and operations
"""

import git
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime


class GitAnalyzer:
    """Analyze Git repository and extract information"""
    
    def __init__(self, repo_path: Optional[Path] = None):
        """Initialize Git analyzer
        
        Args:
            repo_path: Path to git repository. If None, uses current directory.
        """
        try:
            self.repo = git.Repo(repo_path or Path.cwd(), search_parent_directories=True)
        except git.InvalidGitRepositoryError:
            raise ValueError("Not a git repository. Please run this command from within a git repository.")
    
    def get_staged_diff(self) -> str:
        """Get diff of staged changes
        
        Returns:
            Diff content as string
        """
        try:
            # Get diff of staged changes
            diff = self.repo.git.diff('--cached', '--no-color')
            return diff
        except git.GitCommandError as e:
            raise ValueError(f"Failed to get staged diff: {e}")
    
    def get_staged_files(self) -> List[str]:
        """Get list of staged files
        
        Returns:
            List of file paths
        """
        try:
            # Get list of staged files
            diff_index = self.repo.index.diff('HEAD')
            return [item.a_path for item in diff_index]
        except Exception:
            # If no HEAD (initial commit), get all staged files
            # entries.keys() returns tuples (path, stage), we need the path
            return [str(path[0]) if isinstance(path, tuple) else str(path)
                    for path in self.repo.index.entries.keys()]
    
    def has_staged_changes(self) -> bool:
        """Check if there are staged changes
        
        Returns:
            True if there are staged changes, False otherwise
        """
        try:
            diff = self.repo.git.diff('--cached', '--name-only')
            return bool(diff.strip())
        except git.GitCommandError:
            return False
    
    def get_current_branch(self) -> str:
        """Get current branch name
        
        Returns:
            Branch name
        """
        try:
            return self.repo.active_branch.name
        except TypeError:
            # Detached HEAD state
            return self.repo.head.commit.hexsha[:7]
    
    def get_recent_commits(self, count: int = 10) -> List[Dict[str, str]]:
        """Get recent commits
        
        Args:
            count: Number of commits to retrieve
            
        Returns:
            List of commit dictionaries
        """
        commits = []
        try:
            for commit in self.repo.iter_commits(max_count=count):
                commits.append({
                    'hash': commit.hexsha,
                    'short_hash': commit.hexsha[:7],
                    'message': commit.message.strip(),
                    'author': commit.author.name,
                    'date': datetime.fromtimestamp(commit.committed_date).isoformat(),
                })
        except git.GitCommandError:
            pass
        
        return commits
    
    def get_commits_between_branches(
        self, 
        base_branch: str, 
        current_branch: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """Get commits between two branches
        
        Args:
            base_branch: Base branch name
            current_branch: Current branch name. If None, uses active branch.
            
        Returns:
            List of commit dictionaries
        """
        if current_branch is None:
            current_branch = self.get_current_branch()
        
        commits = []
        try:
            # Get commits in current branch that are not in base branch
            commit_range = f"{base_branch}..{current_branch}"
            for commit in self.repo.iter_commits(commit_range):
                commits.append({
                    'hash': commit.hexsha,
                    'short_hash': commit.hexsha[:7],
                    'message': commit.message.strip(),
                    'author': commit.author.name,
                    'date': datetime.fromtimestamp(commit.committed_date).isoformat(),
                })
        except git.GitCommandError as e:
            raise ValueError(f"Failed to get commits between branches: {e}")
        
        return commits
    
    def get_changed_files_between_branches(
        self, 
        base_branch: str, 
        current_branch: Optional[str] = None
    ) -> List[str]:
        """Get files changed between two branches
        
        Args:
            base_branch: Base branch name
            current_branch: Current branch name. If None, uses active branch.
            
        Returns:
            List of changed file paths
        """
        if current_branch is None:
            current_branch = self.get_current_branch()
        
        try:
            # Get diff between branches
            diff = self.repo.git.diff(
                '--name-only', 
                f"{base_branch}...{current_branch}"
            )
            return [f for f in diff.split('\n') if f.strip()]
        except git.GitCommandError as e:
            raise ValueError(f"Failed to get changed files: {e}")
    
    def get_default_branch(self) -> str:
        """Get default branch name (main or master)
        
        Returns:
            Default branch name
        """
        try:
            # First, check local branches
            branches = [str(b.name) for b in self.repo.branches]
            if 'main' in branches:
                return 'main'
            elif 'master' in branches:
                return 'master'
            
            # Try to get remote default branch
            try:
                remote = self.repo.remote()
                refs = remote.refs
                
                # Check for main or master
                for ref in refs:
                    if ref.name.endswith('/main'):
                        return 'main'
                    elif ref.name.endswith('/master'):
                        return 'master'
            except Exception:
                pass
            
            # If we have any branches, return the first one
            if branches:
                return branches[0]
            
            # Fallback to main
            return 'main'
        except Exception:
            return 'main'
    
    def create_branch(self, branch_name: str) -> bool:
        """Create a new branch
        
        Args:
            branch_name: Name of the branch to create
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.repo.git.checkout('-b', branch_name)
            return True
        except git.GitCommandError as e:
            print(f"Failed to create branch: {e}")
            return False
    
    def commit_changes(self, message: str) -> bool:
        """Commit staged changes
        
        Args:
            message: Commit message
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.repo.index.commit(message)
            return True
        except git.GitCommandError as e:
            print(f"Failed to commit changes: {e}")
            return False
    
    def get_repo_info(self) -> Dict[str, Any]:
        """Get repository information
        
        Returns:
            Dictionary with repository info
        """
        try:
            remote_url = self.repo.remote().url
        except Exception:
            remote_url = "No remote configured"
        
        return {
            'path': str(self.repo.working_dir),
            'branch': self.get_current_branch(),
            'remote': remote_url,
            'has_staged': self.has_staged_changes(),
        }
    
    def analyze_diff_stats(self, diff_content: str) -> Dict[str, int]:
        """Analyze diff statistics
        
        Args:
            diff_content: Diff content
            
        Returns:
            Dictionary with statistics
        """
        lines = diff_content.split('\n')
        
        stats = {
            'additions': 0,
            'deletions': 0,
            'files_changed': 0,
        }
        
        files = set()
        for line in lines:
            if line.startswith('+++') or line.startswith('---'):
                # Extract filename
                if line.startswith('+++') and not line.startswith('+++ /dev/null'):
                    filename = line[6:].split('\t')[0]
                    files.add(filename)
            elif line.startswith('+') and not line.startswith('+++'):
                stats['additions'] += 1
            elif line.startswith('-') and not line.startswith('---'):
                stats['deletions'] += 1
        
        stats['files_changed'] = len(files)
        
        return stats
    
    def get_file_type_summary(self, files: List[str]) -> Dict[str, int]:
        """Get summary of file types changed
        
        Args:
            files: List of file paths
            
        Returns:
            Dictionary mapping file extensions to counts
        """
        summary = {}
        
        for file in files:
            ext = Path(file).suffix or 'no_extension'
            summary[ext] = summary.get(ext, 0) + 1
        
        return summary

# Made with Bob
