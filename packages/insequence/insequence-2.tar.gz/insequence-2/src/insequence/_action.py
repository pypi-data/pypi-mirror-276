# SPDX-FileCopyrightText: Christian Heinze
#
# SPDX-License-Identifier: Apache-2.0
"""Action base class."""

from __future__ import annotations

import importlib
import inspect
import os
import pickle
import reprlib
import types
from collections.abc import Callable, Iterable
from typing import (
    TYPE_CHECKING,
    Any,
    Concatenate,
    Generic,
    ParamSpec,
    Protocol,
    TypeAlias,
    TypeVar,
    cast,
)

from .checks import is_iterable

if TYPE_CHECKING:  # pragma: no cover
    import sys

    if sys.version_info < (3, 11):
        from typing_extensions import Self
    else:
        from typing import Self

T = TypeVar("T")
Transformation: TypeAlias = Callable[[T], T]


class ChainLike(Protocol[T]):
    def __init__(self, *functions: Transformation[T]): ...
    def __call__(self, object_: T, /) -> T: ...


TChainLike = TypeVar("TChainLike", bound=ChainLike[Any])
P = ParamSpec("P")


class BaseAction(Generic[T, P, TChainLike]):
    """Action base class."""

    __slots__ = (
        "chaintype",
        "function",
        "args",
        "kwargs",
        "marker",
        #
        "__weakref__",
    )

    @staticmethod
    def function_store_name() -> str:
        try:
            return os.environ["INSEQUENCE_FUNCTION_STORE"]
        except (KeyError, ValueError):
            return f"__{__package__}_funcs__"

    @staticmethod
    def _format_max_args() -> int:
        """Maximal number of (keyword) arguments shown by __repr__."""
        try:
            return int(os.environ["INSEQUENCE_MAX_ARGS"])
        except (KeyError, ValueError):
            return 5

    def __init__(
        self,
        chaintype: type[TChainLike],
        function: Callable[Concatenate[T, P], T],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ):
        try:
            inspect.signature(function).bind(None, *args, **kwargs)
        except TypeError as err:
            raise type(err)(f"{function!r} {err}") from None

        self.chaintype = chaintype
        self.function = function
        self.args = args
        self.kwargs = kwargs

        self.marker: str | None = None

    def tag(self, marker: str | None, /) -> Self:
        """Add marker to action.

        The marker has no internal use. It is meant mainly for indexing/slicing when
        the action is part of a chain.
        """
        self.marker = marker
        return self

    def _compile_named_parameters(self) -> dict[str, Any]:
        signature = inspect.signature(self.function)
        first_parameter, *_ = signature.parameters
        args_specification = signature.bind(None, *self.args, **self.kwargs).arguments
        return cast(
            dict[str, Any],
            {
                k: v
                for k, v in args_specification.items()
                if k not in {first_parameter, "kwargs"}
            }
            | args_specification.get("kwargs", {}),
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        if not (
            self.chaintype == other.chaintype
            and self.function == other.function
            and (self.marker == other.marker or not self.marker and not other.marker)
        ):
            return False
        # shortcut
        if self.args == other.args and self.kwargs == other.kwargs:
            return True
        # check if difference is only due to assignment to args/kwargs
        # no need for special handling of position/keyword-only needed
        # for pure equality checking
        if self._compile_named_parameters() == other._compile_named_parameters():
            return True
        return False

    # ensures that action_.function = action_ does not exceed the recursion depth
    @reprlib.recursive_repr()
    def __repr__(self) -> str:
        try:
            name = self.function.__qualname__
        except AttributeError:
            name = repr(self.function)

        args = [
            *(repr(x) for x in cast(tuple[Any, ...], self.args)),
            *(f"{k}={v!r}" for k, v in cast(dict[str, Any], self.kwargs).items()),
        ]
        n_args_shown = min(len(args), self._format_max_args())
        n_trailing_args = n_args_shown // 2
        n_leading_args = n_args_shown - n_trailing_args
        if n_args_shown < len(args):
            args_shown = args[:n_leading_args] + ["..."]
            if n_trailing_args > 0:
                args_shown.extend(args[-n_trailing_args:])
        else:
            args_shown = args
        components = ", ".join(args_shown)

        out = [name, "(", components, ")"]
        if self.marker:
            out.append(f".tag({self.marker!r})")
        return "".join(out)

    @property
    def _slotnames(self) -> Iterable[str]:
        import itertools

        return itertools.chain.from_iterable(
            getattr(type_, "__slots__", ()) for type_ in type(self).__mro__
        )

    def __getstate__(self) -> tuple[None, dict[str, Any]]:
        """Prepare state for pickling.

        If the function's module has a symbol with name equal to the return value
        of function_store_name function and bound to a mapping which associates
        the function object with the key (function's module, function's __qualname__),
        then that key replaces the function before pickling.
        """
        slots = {name: getattr(self, name) for name in self._slotnames}

        if isinstance(self.function, types.FunctionType):
            key = module, _ = self.function.__module__, self.function.__qualname__
            # function.__globals__ does not react to modification of function.__module__
            store = getattr(
                importlib.import_module(self.function.__module__),
                self.function_store_name(),
                None,
            )
            if store is not None and key in store:
                slots["function"] = key
                slots["module"] = module

        return None, slots

    def __setstate__(self, state: tuple[None, dict[str, Any]]) -> None:
        _, slots = state

        if "function" in slots and not callable(slots["function"]):
            try:
                module = importlib.import_module(slots["module"])
                slots["function"] = getattr(module, self.function_store_name())[
                    slots["function"]
                ]
            except (AttributeError, KeyError, ImportError) as err:
                raise pickle.UnpicklingError("failed to recover function") from err

        for name in self._slotnames:
            if name == "__weakref__":
                continue
            setattr(self, name, slots[name])

    def __call__(self, object_: T, /) -> T:
        return self.function(object_, *self.args, **self.kwargs)

    def __add__(
        self, other: Transformation[T] | Iterable[Transformation[T]] | None
    ) -> TChainLike:
        """Compose the action with other callables."""
        if other is None:
            return self.chaintype(self)
        if is_iterable(other):
            return self.chaintype(self, *other)
        return self.chaintype(self, other)

    def __radd__(
        self, other: Transformation[T] | Iterable[Transformation[T]] | None
    ) -> TChainLike:
        """Right compose the action with other callables."""
        if other is None:
            return self.chaintype(self)
        if is_iterable(other):
            return self.chaintype(*other, self)
        return self.chaintype(other, self)
