from collections.abc import Iterable, Iterator
from typing import Any, overload

from django.forms.fields import Field
from django.forms.forms import BaseForm
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList, RenderableFieldMixin
from django.forms.widgets import Widget
from django.utils.functional import _StrOrPromise, cached_property
from django.utils.safestring import SafeString
from typing_extensions import TypeAlias

_AttrsT: TypeAlias = dict[str, str | bool]

class BoundField(RenderableFieldMixin):
    form: BaseForm
    field: Field
    name: str
    html_name: str
    html_initial_name: str
    html_initial_id: str
    label: _StrOrPromise
    help_text: _StrOrPromise
    renderer: BaseRenderer
    def __init__(self, form: BaseForm, field: Field, name: str) -> None: ...
    @cached_property
    def subwidgets(self) -> list[BoundWidget]: ...
    def __bool__(self) -> bool: ...
    def __iter__(self) -> Iterator[BoundWidget]: ...
    def __len__(self) -> int: ...
    @overload
    def __getitem__(self, idx: int | str) -> BoundWidget: ...
    @overload
    def __getitem__(self, idx: slice) -> list[BoundWidget]: ...
    @property
    def errors(self) -> ErrorList: ...
    @property
    def template_name(self) -> str: ...
    def as_widget(
        self, widget: Widget | None = ..., attrs: _AttrsT | None = ..., only_initial: bool = ...
    ) -> SafeString: ...
    def as_text(self, attrs: _AttrsT | None = ..., **kwargs: Any) -> SafeString: ...
    def __html__(self) -> SafeString: ...
    def as_textarea(self, attrs: _AttrsT | None = ..., **kwargs: Any) -> SafeString: ...
    def as_hidden(self, attrs: _AttrsT | None = ..., **kwargs: Any) -> SafeString: ...
    @property
    def data(self) -> Any: ...
    def value(self) -> Any: ...
    def label_tag(
        self,
        contents: str | None = ...,
        attrs: _AttrsT | None = ...,
        label_suffix: str | None = ...,
        tag: str | None = ...,
    ) -> SafeString: ...
    def legend_tag(
        self, contents: str | None = ..., attrs: _AttrsT | None = ..., label_suffix: str | None = ...
    ) -> SafeString: ...
    def css_classes(self, extra_classes: str | Iterable[str] | None = ...) -> str: ...
    @property
    def is_hidden(self) -> bool: ...
    @property
    def auto_id(self) -> str: ...
    @property
    def id_for_label(self) -> str: ...
    @property
    def initial(self) -> Any: ...
    def build_widget_attrs(self, attrs: _AttrsT, widget: Widget | None = ...) -> _AttrsT: ...
    @property
    def widget_type(self) -> str: ...
    @property
    def use_fieldset(self) -> bool: ...

class BoundWidget:
    parent_widget: Widget
    data: dict[str, Any]
    renderer: BaseRenderer
    def __init__(self, parent_widget: Widget, data: dict[str, Any], renderer: BaseRenderer) -> None: ...
    def tag(self, wrap_label: bool = ...) -> SafeString: ...
    @property
    def template_name(self) -> str: ...
    @property
    def id_for_label(self) -> str: ...
    @property
    def choice_label(self) -> str: ...
