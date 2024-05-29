from collections import namedtuple
from collections.abc import Iterable
from typing import Any

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.utils import CursorWrapper
from django.db.models.base import Model

TableInfo = namedtuple("TableInfo", ["name", "type"])

FieldInfo = namedtuple(
    "FieldInfo",
    ["name", "type_code", "display_size", "internal_size", "precision", "scale", "null_ok", "default", "collation"],
)

class BaseDatabaseIntrospection:
    data_types_reverse: Any
    connection: BaseDatabaseWrapper
    def __init__(self, connection: BaseDatabaseWrapper) -> None: ...
    def get_field_type(self, data_type: str, description: FieldInfo) -> str: ...
    def identifier_converter(self, name: str) -> str: ...
    def table_names(self, cursor: CursorWrapper | None = ..., include_views: bool = ...) -> list[str]: ...
    def get_table_list(self, cursor: CursorWrapper | None) -> Any: ...
    def get_table_description(self, cursor: CursorWrapper | None, table_name: str) -> Any: ...
    def get_migratable_models(self) -> Iterable[type[Model]]: ...
    def django_table_names(self, only_existing: bool = ..., include_views: bool = ...) -> list[str]: ...
    def installed_models(self, tables: list[str]) -> set[type[Model]]: ...
    def sequence_list(self) -> list[dict[str, str]]: ...
    def get_sequences(self, cursor: CursorWrapper | None, table_name: str, table_fields: Any = ...) -> Any: ...
    def get_relations(self, cursor: CursorWrapper | None, table_name: str) -> dict[str, tuple[str, str]]: ...
    def get_primary_key_column(self, cursor: CursorWrapper | None, table_name: str) -> str | None: ...
    def get_primary_key_columns(self, cursor: CursorWrapper | None, table_name: str) -> list[str] | None: ...
    def get_constraints(self, cursor: CursorWrapper | None, table_name: str) -> Any: ...
