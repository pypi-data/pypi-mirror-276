# SPDX-FileCopyrightText: Christian Heinze
#
# SPDX-License-Identifier: Apache-2.0
"""Chain implementation."""

from __future__ import annotations

import dataclasses
import os
import reprlib
from collections.abc import Callable, Generator, Iterable, Iterator
from types import EllipsisType
from typing import TYPE_CHECKING, Any, Generic, TypeAlias, TypeVar

from .checks import is_iterable

if TYPE_CHECKING:  # pragma: no cover
    import sys

    if sys.version_info < (3, 11):
        from typing_extensions import Self
    else:
        from typing import Self

T = TypeVar("T")
Transformation: TypeAlias = Callable[[T], T]
Yields: TypeAlias = Generator[T, None, None]


@dataclasses.dataclass(slots=True, kw_only=True)
class ChainResult(Generic[T]):
    value: T
    condition: BaseException | None

    def unpack(self) -> tuple[T, BaseException | None]:
        return dataclasses.astuple(self)


class Chain(Generic[T]):
    """Function chain.

    Gathers a sequence of transformations (single (non-optional) argument callables
    with identical in- and output type) and when called applies them in sequence
    to an object.
    """

    __slots__ = (
        "functions",
        "controller",
        "cycle_limit",
    )

    @staticmethod
    def _format_n_max() -> int:
        """Maximal number of callables shown by __repr__."""
        try:
            return int(os.environ["INSEQUENCE_CHAIN_TERMS"])
        except (KeyError, ValueError):
            return 5

    def __init__(
        self,
        *functions: Transformation[T] | None,
        controller: Transformation[Yields[Transformation[T]]] | None = None,
        cycle_limit: int | None = 1,
    ):
        """Initialize chain instance.

        Parameters
        ----------
        functions
            Functions to be applied in the order provided; see controller. `None` is
            allowed to have static conditional inclusion; that is, include terms
            of the form `function if condition else None`.
        controller
            Before executing the chain's functions, this function is called with the
            tuple of functions (turned into a generator; see cycle_limit). The
            execution then runs through the returned iterable and executes each
            function in sequence.

            Controllers can themselves be chained, allow to add logging or profiling
            (not exception handling though), and may modify the original functions,
            e.g., by composition.
        cycle_limit
            Number of cycles through the functions during execution. If None, then
            an infinite cycle is started and some function needs to raise StopIteration
            at some point to break the loop. If zero or negative, then no function
            is considered during execution.

            A generator implementing multiple cycles (according to cycle_limit) is
            created from the function tuple. The contoller is applied to this
            generator.

        """
        # this is somewhat inefficient with long | sequences but not copying upon
        # each | call goes against expectations and may be the source of subtle bugs
        self.functions = tuple(
            function for function in functions if function is not None
        )
        self.controller = controller
        self.cycle_limit = cycle_limit

    def __repr__(self) -> str:
        chain_repr = reprlib.Repr()
        chain_repr.maxtuple = self._format_n_max()

        out = [type(self).__name__, chain_repr.repr(self.functions)[:-1]]
        if self.controller is not None:
            out.append(f", controller={self.controller!r}")
        if self.cycle_limit != 1:
            out.append(f", cycle_limit={self.cycle_limit!r}")
        out.append(")")
        return "".join(out)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.functions == other.functions
            and self.controller == other.controller
            and self.cycle_limit == other.cycle_limit
        )

    def __iter__(self) -> Iterator[Transformation[T]]:
        """Obtain an iterator.

        Returns
        -------
        If no controller is set and the cycle limit equals one, then standard iterator
        of the function tuple is returned. If a controller is set or the cycle limit
        differs from one, then the returned iterator yields the chain as its only
        iteration value.

        """
        if self.controller is not None or self.cycle_limit != 1:
            return iter((self,))
        return iter(self.functions)

    def _yield_functions(self) -> Yields[Transformation[T]]:
        cycle = 0
        while self.cycle_limit is None or cycle < self.cycle_limit:
            yield from self.functions
            cycle += 1

    def run(self, object_: T, /) -> ChainResult[T]:
        """Apply functions in sequence.

        Returns
        -------
        Chain result holding the result and the first exception raised duing the chain
        excecution. The returned result is obtained by applying only the steps up to
        the first exception; in case of an immutable input, the actions of the raising
        function will not be reflected in the result.

        """
        generator = self._yield_functions()
        functions = generator if self.controller is None else self.controller(generator)
        condition: BaseException | None = None
        # implements the identity if functions is empty
        for function in functions:
            try:
                if isinstance(function, Chain):
                    object_, condition = function.run(object_).unpack()
                else:
                    object_ = function(object_)
            except Exception as err:
                return ChainResult(
                    value=object_,
                    condition=type(err)(f"failed when executing {function!r}: {err}"),
                )
            if condition is not None:
                return ChainResult(value=object_, condition=condition)

        return ChainResult(value=object_, condition=condition)

    def __call__(self, object_: T, /) -> T:
        """Apply functions in sequence.

        If a function raises StopIteration, then the sequential application is
        stop and the current state of the result is returned. This will include
        all modifications by earlier function calls but in case of an immutable
        argument the raising function's actions will be lost.
        """
        result = self.run(object_)
        if result.condition is None or isinstance(result.condition, StopIteration):
            return result.value
        raise result.condition

    def copy(
        self,
        controlled_by: Transformation[Yields[Transformation[T]]]
        | None
        | EllipsisType = ...,
        with_cycle_limit: int | None | EllipsisType = ...,
    ) -> Self:
        """Shallow copy with new controller and cycle limit.

        Returns
        -------
        A shallow copy of the chain with controller set to controlled_by and cycle
        limit by with_cycle_limit.

        If ... is provided to controlled_by or with_cycle_limit, then the chain's
        values are copied.

        """
        if controlled_by is ...:
            controlled_by = self.controller
        if with_cycle_limit is ...:
            with_cycle_limit = self.cycle_limit

        new_chain = type(self)(controller=controlled_by, cycle_limit=with_cycle_limit)
        # no need to copy immutable funciton tuple
        new_chain.functions = self.functions
        return new_chain

    def __add__(
        self, other: Iterable[Transformation[T]] | Transformation[T] | None
    ) -> Self:
        """Compose with other callable(s)."""
        if other is None:
            return self.copy(
                controlled_by=self.controller, with_cycle_limit=self.cycle_limit
            )
        if is_iterable(other):
            # iter handles the controller and cycle_limit
            return type(self)(*self, *other)
        return type(self)(*self, other)

    def __radd__(
        self, other: Iterable[Transformation[T]] | Transformation[T] | None
    ) -> Self:
        """Right compose with other callable(s)."""
        if other is None:
            return self.copy(
                controlled_by=self.controller, with_cycle_limit=self.cycle_limit
            )
        if is_iterable(other):
            # iter handles the controller and cycle_limit
            return type(self)(*other, *self)
        return type(self)(other, *self)
