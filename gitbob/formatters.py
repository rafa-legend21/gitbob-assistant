"""
Output formatting utilities
"""

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.markdown import Markdown
from typing import List, Dict, Any


console = Console()


def print_success(message: str):
    """Print success message"""
    console.print(f"[green]✓[/green] {message}")


def print_error(message: str):
    """Print error message"""
    console.print(f"[red]✗[/red] {message}", style="red")


def print_warning(message: str):
    """Print warning message"""
    console.print(f"[yellow]⚠[/yellow] {message}", style="yellow")


def print_info(message: str):
    """Print info message"""
    console.print(f"[blue]ℹ[/blue] {message}", style="blue")


def print_header(title: str):
    """Print section header"""
    console.print(f"\n[bold cyan]{title}[/bold cyan]")
    console.print("─" * len(title))


def print_commit_message(message: str):
    """Print formatted commit message"""
    console.print("\n[bold]Generated Commit Message:[/bold]")
    panel = Panel(
        message,
        border_style="green",
        padding=(1, 2),
    )
    console.print(panel)


def print_branch_names(names: List[str]):
    """Print branch name suggestions"""
    console.print("\n[bold]Suggested Branch Names:[/bold]")
    for i, name in enumerate(names, 1):
        console.print(f"  [cyan]{i}.[/cyan] {name}")


def print_pr_description(description: str):
    """Print formatted PR description"""
    console.print("\n[bold]Generated PR Description:[/bold]")
    md = Markdown(description)
    console.print(md)


def print_diff_stats(stats: Dict[str, int]):
    """Print diff statistics"""
    table = Table(show_header=False, box=None)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Files changed", str(stats.get('files_changed', 0)))
    table.add_row("Additions", f"+{stats.get('additions', 0)}")
    table.add_row("Deletions", f"-{stats.get('deletions', 0)}")
    
    console.print(table)


def print_repo_info(info: Dict[str, Any]):
    """Print repository information"""
    console.print("\n[bold]Repository Information:[/bold]")
    console.print(f"  Path: {info.get('path', 'Unknown')}")
    console.print(f"  Branch: [cyan]{info.get('branch', 'Unknown')}[/cyan]")
    console.print(f"  Remote: {info.get('remote', 'None')}")
    
    has_staged = info.get('has_staged', False)
    status = "[green]Yes[/green]" if has_staged else "[yellow]No[/yellow]"
    console.print(f"  Staged changes: {status}")


def print_file_list(files: List[str], title: str = "Files"):
    """Print list of files"""
    console.print(f"\n[bold]{title}:[/bold]")
    for file in files:
        console.print(f"  [dim]•[/dim] {file}")


def print_commits(commits: List[Dict[str, str]], max_display: int = 10):
    """Print commit history"""
    console.print(f"\n[bold]Recent Commits:[/bold]")
    
    for i, commit in enumerate(commits[:max_display]):
        short_hash = commit.get('short_hash', commit.get('hash', '')[:7])
        message = commit.get('message', '').split('\n')[0]  # First line only
        author = commit.get('author', 'Unknown')
        
        console.print(f"  [yellow]{short_hash}[/yellow] {message} [dim]({author})[/dim]")
    
    if len(commits) > max_display:
        remaining = len(commits) - max_display
        console.print(f"  [dim]... and {remaining} more commits[/dim]")


def confirm_action(prompt: str, default: bool = True) -> bool:
    """Ask user for confirmation
    
    Args:
        prompt: Confirmation prompt
        default: Default value if user just presses Enter
        
    Returns:
        True if confirmed, False otherwise
    """
    default_str = "Y/n" if default else "y/N"
    response = console.input(f"\n{prompt} [{default_str}]: ").strip().lower()
    
    if not response:
        return default
    
    return response in ['y', 'yes']


def get_user_input(prompt: str, default: str = "") -> str:
    """Get user input
    
    Args:
        prompt: Input prompt
        default: Default value
        
    Returns:
        User input or default
    """
    if default:
        response = console.input(f"{prompt} [{default}]: ").strip()
        return response if response else default
    else:
        return console.input(f"{prompt}: ").strip()


def get_choice(options: List[str], prompt: str = "Select an option") -> int:
    """Get user choice from list of options
    
    Args:
        options: List of options
        prompt: Selection prompt
        
    Returns:
        Index of selected option (0-based)
    """
    console.print(f"\n[bold]{prompt}:[/bold]")
    for i, option in enumerate(options, 1):
        console.print(f"  [cyan]{i}.[/cyan] {option}")
    
    while True:
        try:
            choice = console.input("\nEnter number (or press Enter for #1): ").strip()
            
            if not choice:
                return 0  # Default to first option
            
            index = int(choice) - 1
            if 0 <= index < len(options):
                return index
            else:
                print_error(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print_error("Please enter a valid number")


def print_loading(message: str = "Processing..."):
    """Print loading message"""
    console.print(f"[dim]{message}[/dim]")


def print_separator():
    """Print separator line"""
    console.print("\n" + "─" * 60 + "\n")


def format_code_block(code: str, language: str = "text") -> str:
    """Format code block with syntax highlighting
    
    Args:
        code: Code content
        language: Programming language
        
    Returns:
        Formatted code string
    """
    syntax = Syntax(code, language, theme="monokai", line_numbers=False)
    return syntax


def print_help_text(command: str, description: str, examples: List[str]):
    """Print help text for a command
    
    Args:
        command: Command name
        description: Command description
        examples: List of usage examples
    """
    console.print(f"\n[bold cyan]{command}[/bold cyan]")
    console.print(f"{description}\n")
    
    if examples:
        console.print("[bold]Examples:[/bold]")
        for example in examples:
            console.print(f"  [dim]$[/dim] {example}")

# Made with Bob
