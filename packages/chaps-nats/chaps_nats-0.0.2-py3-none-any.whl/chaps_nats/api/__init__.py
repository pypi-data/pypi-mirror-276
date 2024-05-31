import rich

try:
    import fastapi
except ImportError:
    rich.print("[bold red]Error importing fastapi ![/red]")

from .jobs_api import *
