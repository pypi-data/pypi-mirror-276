from typing import Any, ClassVar, Literal, TypeVar, overload

from django.db import models
from django.db.models.base import Model
from django.db.models.expressions import Combinable
from django.db.models.fields import BooleanField

_T = TypeVar("_T", bound=Model)

class BaseUserManager(models.Manager[_T]):
    @classmethod
    def normalize_email(cls, email: str | None) -> str: ...
    def make_random_password(self, length: int = ..., allowed_chars: str = ...) -> str: ...
    def get_by_natural_key(self, username: str | None) -> _T: ...

class AbstractBaseUser(models.Model):
    REQUIRED_FIELDS: ClassVar[list[str]]

    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active: bool | BooleanField[bool | Combinable, bool]

    def get_username(self) -> str: ...
    def natural_key(self) -> tuple[str]: ...
    @property
    def is_anonymous(self) -> Literal[False]: ...
    @property
    def is_authenticated(self) -> Literal[True]: ...
    def set_password(self, raw_password: str | None) -> None: ...
    def check_password(self, raw_password: str) -> bool: ...
    async def acheck_password(self, raw_password: str) -> bool: ...
    def set_unusable_password(self) -> None: ...
    def has_usable_password(self) -> bool: ...
    def get_session_auth_hash(self) -> str: ...
    def get_session_auth_fallback_hash(self) -> str: ...
    @classmethod
    def get_email_field_name(cls) -> str: ...
    @classmethod
    @overload
    def normalize_username(cls, username: str) -> str: ...
    @classmethod
    @overload
    def normalize_username(cls, username: Any) -> Any: ...
