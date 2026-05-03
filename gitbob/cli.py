"""
Command-line interface for GitBob Assistant
"""

import click
import sys
from pathlib import Path
from typing import Optional

from .config import get_config, Config
from .git_analyzer import GitAnalyzer
from .bob_client import BobClient, MockBobClient
from .prompts import PromptTemplates, truncate_diff, format_file_changes
from . import formatters as fmt


@click.group()
@click.version_option(version="0.1.0")
@click.option('--config', type=click.Path(exists=True), help='Path to config file')
@click.option('--mock', is_flag=True, help='Use mock API client for testing')
@click.pass_context
def cli(ctx, config: Optional[str], mock: bool):
    """GitBob Assistant - AI-powered Git workflow automation
    
    Streamline your Git operations with intelligent commit messages,
    branch names, and PR descriptions powered by IBM Bob.
    """
    ctx.ensure_object(dict)
    
    # Load configuration
    config_path = Path(config) if config else None
    ctx.obj['config'] = get_config(config_path)
    ctx.obj['mock'] = mock


@cli.command()
@click.option('--edit/--no-edit', default=True, help='Allow editing before commit')
@click.option('--push', is_flag=True, help='Push after committing')
@click.pass_context
def commit(ctx, edit: bool, push: bool):
    """Generate and create a commit with AI-generated message
    
    Analyzes staged changes and generates a conventional commit message.
    """
    config: Config = ctx.obj['config']
    use_mock: bool = ctx.obj['mock']
    
    try:
        # Initialize components
        try:
            git = GitAnalyzer()
        except ValueError as e:
            fmt.print_error(str(e))
            fmt.print_info("Make sure you're in a git repository. Run 'git init' if needed.")
            sys.exit(1)
        
        bob = MockBobClient(config) if use_mock else BobClient(config)
        
        # Check for staged changes
        if not git.has_staged_changes():
            fmt.print_error("No staged changes found.")
            fmt.print_info("Stage your changes first with: git add <files>")
            fmt.print_info("Or stage all changes with: git add .")
            sys.exit(1)
        
        # Get repository info
        repo_info = git.get_repo_info()
        fmt.print_repo_info(repo_info)
        
        # Get staged files and diff
        staged_files = git.get_staged_files()
        diff_content = git.get_staged_diff()
        
        # Show what's being committed
        fmt.print_file_list(staged_files, "Staged Files")
        
        # Analyze diff stats
        stats = git.analyze_diff_stats(diff_content)
        fmt.print_diff_stats(stats)
        
        # Generate commit message
        fmt.print_loading("Generating commit message...")
        
        # Prepare prompt
        truncated_diff = truncate_diff(diff_content, max_lines=500)
        formatted_files = format_file_changes(staged_files, max_files=20)
        prompt = PromptTemplates.commit_message(truncated_diff, formatted_files)
        
        # Generate message
        commit_message = bob.generate_commit_message(prompt)
        
        # Display generated message
        fmt.print_commit_message(commit_message)
        
        # Allow editing if requested
        if edit:
            if not fmt.confirm_action("Use this commit message?", default=True):
                fmt.print_info("Opening editor to modify message...")
                # In a real implementation, would open editor here
                # For now, allow manual input
                custom_message = fmt.get_user_input("Enter custom message (or press Enter to cancel)", "")
                if custom_message:
                    commit_message = custom_message
                else:
                    fmt.print_warning("Commit cancelled")
                    sys.exit(0)
        
        # Commit changes
        if git.commit_changes(commit_message):
            fmt.print_success("Changes committed successfully!")
            
            if push:
                fmt.print_info("Pushing changes...")
                # In real implementation, would push here
                fmt.print_success("Changes pushed!")
        else:
            fmt.print_error("Failed to commit changes")
            sys.exit(1)
            
    except Exception as e:
        fmt.print_error(f"Error: {e}")
        sys.exit(1)


@cli.command()
@click.argument('description', required=False)
@click.option('--create', is_flag=True, help='Create the branch immediately')
@click.pass_context
def branch(ctx, description: Optional[str], create: bool):
    """Generate branch name suggestions
    
    Suggests branch names based on your description and recent work.
    """
    config: Config = ctx.obj['config']
    use_mock: bool = ctx.obj['mock']
    
    try:
        # Initialize components
        try:
            git = GitAnalyzer()
        except ValueError as e:
            fmt.print_error(str(e))
            fmt.print_info("Make sure you're in a git repository.")
            sys.exit(1)
        
        bob = MockBobClient(config) if use_mock else BobClient(config)
        
        # Get description if not provided
        if not description:
            description = fmt.get_user_input("Briefly describe the work you're doing")
            if not description:
                fmt.print_error("Description is required")
                sys.exit(1)
        
        # Get context
        current_branch = git.get_current_branch()
        recent_commits = git.get_recent_commits(count=5)
        
        fmt.print_info(f"Current branch: {current_branch}")
        
        # Generate branch names
        fmt.print_loading("Generating branch name suggestions...")
        
        commit_messages = [c['message'] for c in recent_commits]
        prompt = PromptTemplates.branch_name(description, current_branch, commit_messages)
        
        branch_names = bob.generate_branch_names(prompt)
        
        if not branch_names:
            fmt.print_error("Failed to generate branch names")
            sys.exit(1)
        
        # Display suggestions
        fmt.print_branch_names(branch_names)
        
        # Create branch if requested
        if create or fmt.confirm_action("Create a branch?", default=False):
            choice = fmt.get_choice(branch_names, "Select branch to create")
            selected_branch = branch_names[choice]
            
            if git.create_branch(selected_branch):
                fmt.print_success(f"Created and switched to branch: {selected_branch}")
            else:
                fmt.print_error("Failed to create branch")
                sys.exit(1)
        
    except Exception as e:
        fmt.print_error(f"Error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--base', default=None, help='Base branch (default: main/master)')
@click.option('--copy', is_flag=True, help='Copy to clipboard')
@click.pass_context
def pr(ctx, base: Optional[str], copy: bool):
    """Generate PR description from commits
    
    Creates a comprehensive PR description based on commits and changes.
    """
    config: Config = ctx.obj['config']
    use_mock: bool = ctx.obj['mock']
    
    try:
        # Initialize components
        try:
            git = GitAnalyzer()
        except ValueError as e:
            fmt.print_error(str(e))
            fmt.print_info("Make sure you're in a git repository.")
            sys.exit(1)
        
        bob = MockBobClient(config) if use_mock else BobClient(config)
        
        # Get base branch
        if not base:
            base = git.get_default_branch()
            fmt.print_info(f"Auto-detected base branch: {base}")
        
        current_branch = git.get_current_branch()
        
        if current_branch == base:
            fmt.print_error(f"Already on base branch '{base}'.")
            fmt.print_info("Switch to a feature branch first with: git checkout -b feature/your-branch")
            sys.exit(1)
        
        fmt.print_info(f"Generating PR description: {current_branch} → {base}")
        
        # Get commits and changes
        try:
            commits = git.get_commits_between_branches(base, current_branch)
        except ValueError as e:
            fmt.print_error(f"Failed to get commits: {e}")
            fmt.print_info(f"Make sure branch '{base}' exists.")
            sys.exit(1)
        
        if not commits:
            fmt.print_warning(f"No commits found between {base} and {current_branch}")
            fmt.print_info("This might be because:")
            fmt.print_info(f"  - Branch '{current_branch}' is up to date with '{base}'")
            fmt.print_info(f"  - Branch '{base}' doesn't exist")
            fmt.print_info("Creating a simple PR description anyway...")
        
        changed_files = git.get_changed_files_between_branches(base, current_branch)
        
        # Show context
        fmt.print_commits(commits)
        fmt.print_file_list(changed_files, f"Files Changed ({len(changed_files)})")
        
        # Generate PR description
        fmt.print_loading("Generating PR description...")
        
        formatted_files = format_file_changes(changed_files, max_files=30)
        prompt = PromptTemplates.pr_description(commits, formatted_files, base, current_branch)
        
        pr_description = bob.generate_pr_description(prompt)
        
        # Display description
        fmt.print_pr_description(pr_description)
        
        # Copy to clipboard if requested
        if copy:
            try:
                import pyperclip
                pyperclip.copy(pr_description)
                fmt.print_success("PR description copied to clipboard!")
            except ImportError:
                fmt.print_warning("pyperclip not installed. Install with: pip install pyperclip")
        
    except Exception as e:
        fmt.print_error(f"Error: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def config_cmd(ctx):
    """Show current configuration"""
    config: Config = ctx.obj['config']
    
    fmt.print_header("GitBob Configuration")
    
    # Show key configuration values
    fmt.console.print(f"\nConfig file: {config.config_path}")
    fmt.console.print(f"API endpoint: {config.get('ibm_bob.endpoint')}")
    fmt.console.print(f"Model: {config.get('ibm_bob.model')}")
    fmt.console.print(f"Cache enabled: {config.get('cache.enabled')}")
    fmt.console.print(f"Cache directory: {config.get('cache.directory')}")
    
    # Test API connection
    use_mock: bool = ctx.obj['mock']
    if not use_mock:
        fmt.print_loading("\nTesting API connection...")
        try:
            bob = BobClient(config)
            if bob.test_connection():
                fmt.print_success("API connection successful!")
            else:
                fmt.print_error("API connection failed")
        except Exception as e:
            fmt.print_error(f"API connection failed: {e}")


@cli.command()
def init():
    """Initialize GitBob configuration
    
    Creates a configuration file in ~/.gitbob/config.yaml
    """
    config_dir = Path.home() / ".gitbob"
    config_file = config_dir / "config.yaml"
    
    if config_file.exists():
        if not fmt.confirm_action(f"Config file already exists at {config_file}. Overwrite?", default=False):
            fmt.print_info("Initialization cancelled")
            return
    
    # Create config directory
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy example config
    example_config = Path(__file__).parent.parent / "config.example.yaml"
    
    if example_config.exists():
        import shutil
        shutil.copy(example_config, config_file)
        fmt.print_success(f"Configuration file created at {config_file}")
        fmt.print_info("Edit the file to add your IBM Bob API key")
    else:
        fmt.print_error("Example config file not found")
        sys.exit(1)


if __name__ == '__main__':
    cli()

# Made with Bob
