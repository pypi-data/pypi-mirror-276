from __future__ import annotations

import weakref
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar, overload

from typing_extensions import Self

from .optional import Empty, Of, Optional

_V = TypeVar("_V")


class OptionalProperty(Generic[_V]):
    """An optional property.

    This construct holds a value only if was set. Otherwise, a callable object supplies
    the default value.

    Example usage:
        ```python-interactive

        >>> from optional import OptionalProperty

        >>> class Foo:
        ...     @OptionalProperty
        ...     def my_property(self):
        ...         return "default"

        >>> obj=Foo()
        >>> # Get the default value
        >>> obj.my_property
        'default'
        >>> # Check wether the value is present
        >>> Foo.my_property.is_present(obj)
        False
        >>> # Set another value and retrieve it
        >>> obj.my_property="other"
        >>> obj.my_property
        'other'
        >>> Foo.my_property.is_present(obj)
        True
        >>> # Just use python syntax to restore to the default value
        >>> del obj.my_property
        >>> obj.my_property
        'default'

        ```

    The type parameter `_V` if the type accepted and returned by the property.

    """

    def __init__(
        self,
        fget: Callable[[Any], _V],
    ) -> None:
        super().__init__()
        if not callable(fget):
            error_msg = f"{fget!r} is not callable."
            raise TypeError(error_msg)
        self._values: dict[int, _Entry[_V]] = {}
        self.__doc__ = fget.__doc__
        self.__func__ = fget

    @overload
    def __get__(self, instance: None, owner: type[Any]) -> Self:  # pragma: nocover
        ...

    @overload
    def __get__(self, instance: Any, owner: type[Any]) -> _V:  # pragma: nocover
        ...

    def __get__(self, instance: object | None, owner: type[Any]) -> _V | Self:
        if instance is not None:
            entry = self._entry(instance)
            if entry.value.has_value:
                return entry.value.value
            return self.__func__(instance)
        return self

    def __set__(self, __instance: Any, __value: _V) -> None:
        self._entry(__instance).value = Of(__value)

    def _entry(self, obj: object) -> _Entry[_V]:
        entry = self._values.get(id(obj))
        if entry is None:

            def _finalyze(x: int) -> None:
                if x in self._values:
                    del self._values[x]

            entry = _Entry[_V](weakref.finalize(obj, _finalyze, id(obj)))
            self._values[id(obj)] = entry
        return entry

    def __delete__(self, instance: object) -> None:
        self._entry(instance).finalizer()

    def is_present(self, obj: object) -> bool:
        """Check wether the property was set.

        Args:
            obj: The object to check

        Returns:
            `True` if the property was set. Otherwise returns `False`
        """
        return bool(self.raw(obj))

    def raw(self, obj: Any) -> Optional[_V]:
        """Retrieve the raw optional object.

        Args:
            obj (Any): Theobject to check

        Returns:
            The raw optional object powering the property.
        """
        return self._entry(obj).value


@dataclass()
class _Entry(Generic[_V]):
    finalizer: weakref.finalize
    value: Optional[_V] = field(default_factory=Empty)


def optionalproperty(func: Callable[[Any], _V]) -> OptionalProperty[_V]:
    """Alias for [OptionalProperty][optional.OptionalProperty].

    Args:
        func: The default value supplier.

    Returns:
        An optional property construct.
    """
    return OptionalProperty(func)
