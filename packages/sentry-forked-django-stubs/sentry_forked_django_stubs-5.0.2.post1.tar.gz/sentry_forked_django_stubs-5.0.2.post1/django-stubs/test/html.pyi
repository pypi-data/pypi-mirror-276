from collections.abc import Sequence
from html.parser import HTMLParser
from re import Pattern
from typing import Any

from typing_extensions import TypeAlias

ASCII_WHITESPACE: Pattern[str]
BOOLEAN_ATTRIBUTES: set[str]

def normalize_whitespace(string: str) -> str: ...
def normalize_attributes(attributes: list[tuple[str, str | None]]) -> list[tuple[str, str | None]]: ...

_ElementAttribute: TypeAlias = tuple[str, str | None]

class Element:
    name: str | None
    attributes: list[_ElementAttribute]
    children: list[Any]
    def __init__(self, name: str | None, attributes: Sequence[_ElementAttribute]) -> None: ...
    def append(self, element: Element | str) -> None: ...
    def finalize(self) -> None: ...
    def __contains__(self, element: Element | str) -> bool: ...
    def count(self, element: Element | str) -> int: ...
    def __getitem__(self, key: int) -> Any: ...

class RootElement(Element):
    def __init__(self) -> None: ...

class HTMLParseError(Exception): ...

class Parser(HTMLParser):
    root: Any
    open_tags: Any
    element_positions: Any
    def __init__(self) -> None: ...
    def error(self, msg: str) -> HTMLParseError: ...
    def format_position(self, position: Any = ..., element: Any = ...) -> str: ...
    @property
    def current(self) -> Element: ...

def parse_html(html: str) -> Element: ...
