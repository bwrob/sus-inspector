"""CLI commands for sus-inspector, including global injection."""

from __future__ import annotations

import os
import site
import sys

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

console = Console()


INJECTION_MARKER = "# --- Added by sus-inspector ---"
INJECTION_END_MARKER = "# ------------------------------"


def get_injection_code() -> str:
    """Return the code to be injected into usercustomize.py."""
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


def get_target_info(is_global: bool) -> tuple[str, str]:
    """Return the site-packages directory and the filename to use."""
    if is_global:
        # User-specific global site-packages
        return site.getusersitepackages(), "usercustomize.py"

    # Virtual environment or system-wide site-packages
    # We prefer the first one in the list
    site_packages = site.getsitepackages()
    target_dir = site_packages[0] if site_packages else site.getusersitepackages()
    return target_dir, "sitecustomize.py"


def inject_permanently(is_global: bool = False) -> None:
    """Inject sus permanently into builtins. Targets venv by default."""
    target_dir, filename = get_target_info(is_global)
    target_path = os.path.join(target_dir, filename)

    scope_name = "GLOBAL USER" if is_global else "VIRTUAL ENV"

    console.print(
        Panel(
            f"[bold yellow]Injection: sus-inspector ({scope_name})[/bold yellow]\n\n"
            f"This command will attempt to inject [bold]sus[/bold] into your environment.\n\n"
            f"• Target: [blue]{target_path}[/blue]\n"
            "• Once injected, [bold]sus[/bold] will be available in every Python "
            "script run in this environment without an import.\n"
            "• A [italic]try/except[/italic] block ensures your Python won't break if you "
            "uninstall the package later.",
            title="🔍 Setup",
            expand=False,
        )
    )

    if not Confirm.ask(f"Do you want to proceed with the {scope_name.lower()} installation?"):
        console.print("[red]Aborted.[/red]")
        return

    # 1. Ensure directory exists
    if not os.path.exists(target_dir):
        try:
            os.makedirs(target_dir)
        except Exception as e:
            console.print(f"[red]Error creating directory {target_dir}:[/red] {e}")
            sys.exit(1)

    # 2. Check for existing injection
    injection_code = get_injection_code()
    if os.path.exists(target_path):
        with open(target_path) as f:
            content = f.read()
            if INJECTION_MARKER in content:
                console.print(f"[green]sus is already injected into {filename}![/green]")
                return

    # 3. Append the code
    try:
        with open(target_path, "a") as f:
            # Ensure there's a newline if the file already exists and isn't empty
            if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
                f.write("\n")
            f.write(injection_code)
        console.print(
            f"\n[bold green]Success![/bold green] Injected into: [blue]{target_path}[/blue]\n"
            "Restart your Python shell and try typing [bold]sus / ...[/bold]"
        )
    except Exception as e:
        console.print(f"[red]Failed to write to {target_path}:[/red] {e}")
        sys.exit(1)


def remove_injection(is_global: bool = False) -> None:
    """Remove the sus-inspector injection. Targets venv by default."""
    target_dir, filename = get_target_info(is_global)
    target_path = os.path.join(target_dir, filename)

    if not os.path.exists(target_path):
        console.print(f"[yellow]No {filename} found at {target_path}.[/yellow]")
        return

    with open(target_path) as f:
        lines = f.readlines()

    new_lines = []
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
        console.print(f"[yellow]No sus-inspector injection found in {target_path}.[/yellow]")
        return

    try:
        with open(target_path, "w") as f:
            f.writelines(new_lines)
        console.print(f"[bold green]Success![/bold green] Injection removed from {target_path}.")
    except Exception as e:
        console.print(f"[red]Failed to update {target_path}:[/red] {e}")
        sys.exit(1)

