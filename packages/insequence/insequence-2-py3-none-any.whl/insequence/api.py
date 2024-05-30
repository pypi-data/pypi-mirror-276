# SPDX-FileCopyrightText: Christian Heinze
#
# SPDX-License-Identifier: Apache-2.0
"""Decorators, controllers, and other API components."""

from __future__ import annotations

import contextlib
import importlib
import types
import weakref
from collections.abc import Callable
from typing import (
    TYPE_CHECKING,
    Any,
    Concatenate,
    Generic,
    ParamSpec,
    TypeAlias,
    TypeVar,
    overload,
)

if TYPE_CHECKING:  # pragma: no cover
    from contextlib import AbstractContextManager

    Context: TypeAlias = (
        AbstractContextManager[Any] | Callable[[], AbstractContextManager[Any]]
    )

from ._action import BaseAction
from .chain import Chain, Transformation, Yields

T = TypeVar("T")
P = ParamSpec("P")


class Action(BaseAction[T, P, Chain[T]]):
    __slots__ = ()

    def __init__(
        self,
        function: Callable[Concatenate[T, P], T],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ):
        """Initialize action instance.

        Parameters
        ----------
        function
            Function to be called when its first argument is supplied via the
            action's __call__ method.
        args
            Argument used when calling function.
        kwargs
            Keyword arguments used when calling function.

        """
        super().__init__(Chain, function, *args, **kwargs)


def _attributes(**kwargs: Any) -> Callable[[T], T]:
    def set_attributes(object_: T) -> T:
        not_present = object()
        for name, value in kwargs.items():
            old_value = getattr(object_, name, not_present)
            if old_value is not_present:
                continue
            setattr(object_, name, value)

        return object_

    return set_attributes


@overload
def action(
    function: Callable[Concatenate[T, P], T],
) -> Callable[P, Action[T, P]]: ...


@overload
def action(
    function: None = ...,
) -> Callable[[Callable[Concatenate[T, P], T]], Callable[P, Action[T, P]]]: ...


def action(
    function: Callable[Concatenate[T, P], T] | None = None,
) -> (
    Callable[P, Action[T, P]]
    | Callable[[Callable[Concatenate[T, P], T]], Callable[P, Action[T, P]]]
):
    """Turn a callable into a function factory.

    The function factory takes the second to last argument of the original function
    and returns a callable (action) that can be called with the first argument to the
    original function alone and triggers a call of original function with all arguments.

    The returned function will inherit the module, name, __qualname__, and docstring
    from the original function. The original function's docstring should be
    formulated accordingly; in particular, do not mention the first argument in the
    parameter list and add an appropriate return value description.
    """

    def create_build_action(
        function: Callable[Concatenate[T, P], T],
    ) -> Callable[P, Action[T, P]]:
        # equivalent to functools.wraps in this case but needs not extra import
        @_attributes(
            __module__=function.__module__,
            __name__=function.__name__,
            __qualname__=function.__qualname__,
            __doc__=function.__doc__,
        )
        def build_action(*args: P.args, **kwargs: P.kwargs) -> Action[T, P]:
            return Action(function, *args, **kwargs)

        if isinstance(function, types.FunctionType):
            if function.__name__ == (lambda: ...).__name__:
                return build_action
            with contextlib.suppress(Exception):
                # function.__globals___ yields the same dictionary if __module__
                # has not been modified. Using this construct allows returning
                # action decorated functions without storing the action function in
                # that code's module; see controller below.
                importlib.import_module(function.__module__).__dict__.setdefault(
                    Action.function_store_name(), weakref.WeakValueDictionary()
                )[function.__module__, function.__qualname__] = function

        return build_action

    return create_build_action(function) if function else create_build_action


@overload
def controller(
    function: Callable[
        Concatenate[Yields[Transformation[T]], P], Yields[Transformation[T]]
    ],
) -> Callable[P, Action[Chain[T], P]]: ...


@overload
def controller(
    function: None = ...,
) -> Callable[
    [Callable[Concatenate[Yields[Transformation[T]], P], Yields[Transformation[T]]]],
    Callable[P, Action[Chain[T], P]],
]: ...


def controller(
    function: Callable[
        Concatenate[Yields[Transformation[T]], P], Yields[Transformation[T]]
    ]
    | None = None,
) -> (
    Callable[P, Action[Chain[T], P]]
    | Callable[
        [
            Callable[
                Concatenate[Yields[Transformation[T]], P], Yields[Transformation[T]]
            ]
        ],
        Callable[P, Action[Chain[T], P]],
    ]
):
    """Turn a callable into a chain modifier factory.

    The action decorator is applied to the decorated function. Then a second
    factory is created using the action decorator which generates callables that
    compose a chain's controller with a controller generated via the decorated
    function.
    """

    def create_modify_chain(
        function: Callable[
            Concatenate[Yields[Transformation[T]], P], Yields[Transformation[T]]
        ],
    ) -> Callable[P, Action[Chain[T], P]]:
        controller_ = action(function)

        @action
        @_attributes(
            __module__=function.__module__,
            __name__=f"{function.__name__}_wrapper",
            __qualname__=f"{function.__qualname__}_wrapper",
            __doc__=function.__doc__,
        )
        def modify_chain(
            chain: Chain[T], /, *args: P.args, **kwargs: P.kwargs
        ) -> Chain[T]:
            return chain.copy(
                controlled_by=chain.controller + controller_(*args, **kwargs)
            )

        return modify_chain

    return create_modify_chain(function) if function else create_modify_chain


class modifiers(Generic[T]):  # noqa [N801]
    """Namespace for builtin chain modifiers."""

    def __init__(self, *args: Any, **kwargs: Any):
        raise NotImplementedError(
            f"class {type(self).__name__} does not support instantiation"
        )

    @staticmethod
    @action
    def repeat(chain: Chain[T], limit: int | None = None) -> Chain[T]:
        """Repeatedly cycle through chain.

        Create a new chain with cycle limit equal to limit and the input chain as its
        sole function. Thus, the original chain is repeated as specified by limit and
        controllers already present in the chain take effect during each cycle. For
        example, skip is applied during each run the chain not the complete new
        sequence of functions.

        Parameters
        ----------
        limit
            Number of cycles through the iterable. If None, then cycles indefinitely
            (there is not limit on the number of cycles).

        """
        if limit is not None and limit < 1:
            raise ValueError("limit is nonpositive")
        return Chain(chain, cycle_limit=limit)

    @staticmethod
    @controller
    def use_context(
        generator: Yields[Transformation[T]],
        manager: AbstractContextManager[Any]
        | Callable[[], AbstractContextManager[Any]],
    ) -> Yields[Transformation[T]]:
        """Execute each function inside a context.

        Parameters
        ----------
        manager
            Execution context. If a context manager is supplied, then it must support
            multiple entry/exit rounds as a fresh context is set up for each function.

        """
        for object_ in generator:
            manager_ = manager() if callable(manager) else manager
            with manager_:
                yield object_

    @staticmethod
    @controller
    def prepend(
        generator: Yields[Transformation[T]], function: Transformation[T]
    ) -> Yields[Transformation[T]]:
        """Prepend an operation to each function.

        Parameters
        ----------
        function
            Action to be taken before each call of a chain function.

        """
        for transform in generator:
            yield Chain(function, transform)

    @staticmethod
    @controller
    def append(
        generator: Yields[Transformation[T]], function: Transformation[T]
    ) -> Yields[Transformation[T]]:
        """Append an operation to each function.

        Parameters
        ----------
        function
            Action to be taken after each call of a chain function.

        """
        for transform in generator:
            yield Chain(transform, function)

    @staticmethod
    @controller
    def skip(
        generator: Yields[Transformation[T]], *skip: str | int
    ) -> Yields[Transformation[T]]:
        """Skip specified callables."""
        skip_ = set(skip)
        for i, object_ in enumerate(generator):
            if i in skip_:
                continue
            if getattr(object_, "marker", None) in skip_:
                continue

            yield object_

    @staticmethod
    @controller
    def window(
        generator: Yields[Transformation[T]],
        start: int | str | None = None,
        end: int | str | None = None,
        start_inclusive: bool = True,
        end_inclusive: bool = False,
    ) -> Yields[Transformation[T]]:
        """Run a window of a chain defined by integer indexes or markers/tags.

        Only the first occurence of a marker is considered. Later occurences are
        ignored.

        Parameter
        ---------
        start
            Specifies the start of the window via either an integer index or a tag.
        end
            Specifies the start of the window via either an integer index or a tag.
        start_inclusive
            If True, then the start is contained in the window.
        end_inclusive
            If True, then the end is contained in the window.

        """
        has_started = start is None
        has_ended = False
        for i, function in enumerate(generator):
            if not has_started and not has_ended:
                if isinstance(start, int):
                    has_started = start <= i
                else:
                    has_started = getattr(function, "marker", None) == start

                if has_started and not start_inclusive:
                    continue

            # end is checked before start to cover the case that end occurs before start
            if not has_ended and end is not None:
                if isinstance(end, int):
                    has_ended = end <= i
                else:
                    has_ended = getattr(function, "marker", None) == end

                if has_ended and end_inclusive:
                    yield function

            if has_started and not has_ended:
                yield function
