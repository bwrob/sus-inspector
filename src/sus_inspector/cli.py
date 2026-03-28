"""CLI commands for sus-inspector, including global injection."""

from __future__ import annotations

import site
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

console = Console()


INJECTION_MARKER = "# --- Added by sus-inspector ---"
INJECTION_END_MARKER = "# ------------------------------"


def get_injection_code() -> str:
    """Return the code to be injected into usercustomize.py.

    Returns:
        str: Python code block.

    """
    return f"""
{INJECTION_MARKER}
try:
    import builtins

    from sus_inspector import sus

    builtins.sus = sus
except ImportError:
    pass
{INJECTION_END_MARKER}
"""


def get_target_info(*, is_global_user: bool) -> tuple[Path, str]:
    """Return the site-packages directory and the filename to use.

    Args:
        is_global_user: Whether to target global user site-packages.

    Returns:
        tuple[Path, str]: (target_directory, filename).

    """
    if is_global_user:
        # User-specific global site-packages
        return Path(site.getusersitepackages()), "usercustomize.py"

    # Virtual environment or system-wide site-packages
    # We prefer the first one in the list
    site_packages = site.getsitepackages()
    if site_packages:
        target_dir = Path(site_packages[0])
    else:
        target_dir = Path(site.getusersitepackages())
    return target_dir, "sitecustomize.py"


def _ensure_dir(target_dir: Path) -> bool:
    """Ensure the target directory exists.

    Args:
        target_dir: Directory to ensure.

    Returns:
        bool: True if successful.

    """
    if not target_dir.exists():
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            console.print(f"[red]Error creating directory {target_dir}:[/red] {e}")
            return False
    return True


def _check_already_injected(target_path: Path, filename: str) -> bool:
    """Check if sus is already injected into the target file.

    Args:
        target_path: Path to the file.
        filename: Name of the file for display.

    Returns:
        bool: True if already injected.

    """
    if target_path.exists():
        with target_path.open(encoding="utf-8") as f:
            content = f.read()
            if INJECTION_MARKER in content:
                msg = f"[green]sus is already injected into {filename}![/green]"
                console.print(msg)
                return True
    return False


def _write_injection(target_path: Path) -> None:
    """Write the injection code to the target file.

    Args:
        target_path: Path to the file.

    """
    try:
        with target_path.open("a", encoding="utf-8") as f:
            if target_path.exists() and target_path.stat().st_size > 0:
                _ = f.write("\n")
            _ = f.write(get_injection_code())
        s_msg = (
            f"\n[bold green]Success![/bold green] Injected: [blue]{target_path}[/blue]"
        )
        console.print(s_msg)
    except OSError as e:
        console.print(f"[red]Failed to write to {target_path}:[/red] {e}")
        sys.exit(1)


def inject_permanently(*, is_global_user: bool = False) -> None:
    """Inject sus permanently into builtins. Targets venv by default.

    Args:
        is_global_user: Whether to target global user site-packages.

    """
    target_dir, filename = get_target_info(is_global_user=is_global_user)
    target_path = target_dir / filename
    scope_name = "GLOBAL USER" if is_global_user else "VIRTUAL ENV"

    msg = (
        f"This command will inject [bold]sus[/bold] into your environment.\n\n"
        f"• Target: [blue]{target_path}[/blue]\n"
        "• [bold]sus[/bold] will be available globally in this environment.\n"
        "• [italic]try/except[/italic] ensures your Python won't break."
    )
    console.print(Panel(msg, title=f"🔍 Setup ({scope_name})", expand=False))

    prompt = f"Do you want to proceed with the {scope_name.lower()} installation?"
    if not Confirm.ask(prompt):
        console.print("[red]Aborted.[/red]")
        return

    if not _ensure_dir(target_dir):
        sys.exit(1)

    if _check_already_injected(target_path, filename):
        return

    _write_injection(target_path)


def remove_injection(*, is_global_user: bool = False) -> None:
    """Remove the sus-inspector injection. Targets venv by default.

    Args:
        is_global_user: Whether to target global user site-packages.

    """
    target_dir, filename = get_target_info(is_global_user=is_global_user)
    target_path = target_dir / filename

    if not target_path.exists():
        console.print(f"[yellow]No {filename} found at {target_path}.[/yellow]")
        return

    with target_path.open(encoding="utf-8") as f:
        lines = f.readlines()

    new_lines: list[str] = []
    in_block = False
    found = False

    for line in lines:
        if INJECTION_MARKER in line:
            in_block = True
            found = True
            continue
        if INJECTION_END_MARKER in line:
            in_block = False
            continue
        if not in_block:
            new_lines.append(line)

    if not found:
        path_str = str(target_path)
        msg = f"[yellow]No sus-inspector injection found in {path_str}.[/yellow]"
        console.print(msg)
        return

    try:
        with target_path.open("w", encoding="utf-8") as f:
            f.writelines(new_lines)
        path_str = str(target_path)
        msg = f"[bold green]Success![/bold green] Removed from {path_str}."
        console.print(msg)
    except OSError as e:
        console.print(f"[red]Failed to update {target_path}:[/red] {e}")
        sys.exit(1)
