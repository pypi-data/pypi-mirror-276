from typing import Any

from .base import BaseCommand as BaseCommand
from .base import CommandError as CommandError
from .base import CommandParser as CommandParser
from .base import handle_default_options as handle_default_options

def find_commands(management_dir: str) -> list[str]: ...
def load_command_class(app_name: str, name: str) -> BaseCommand: ...
def get_commands() -> dict[str, str]: ...
def call_command(command_name: BaseCommand | str, *args: Any, **options: Any) -> str: ...

class ManagementUtility:
    argv: list[str]
    prog_name: str
    settings_exception: Exception | None
    def __init__(self, argv: list[str] | None = ...) -> None: ...
    def main_help_text(self, commands_only: bool = ...) -> str: ...
    def fetch_command(self, subcommand: str) -> BaseCommand: ...
    def autocomplete(self) -> None: ...
    def execute(self) -> None: ...

def execute_from_command_line(argv: list[str] | None = ...) -> None: ...
