# SPDX-FileCopyrightText: Christian Heinze
#
# SPDX-License-Identifier: Apache-2.0
"""Test action."""

import functools
import pickle
import weakref
from collections.abc import Callable, Iterator
from typing import Any

import pytest
from base import TransformationFactory
from insequence._action import BaseAction


class SimpleChain:
    def __init__(self, *functions: Callable[[int], int]):
        self.functions = functions

    def __call__(self, argument: int, /) -> int:
        for function in self.functions:
            argument = function(argument)
        return argument

    def __iter__(self) -> Iterator[Callable[[int], int]]:
        return iter(self.functions)


def has_args_and_kwargs(x: int, y: int, *args: int, **kwargs: int) -> int:
    return (x - y) * (sum(args) + sum(kwargs.values()))


def test_init___if_required_argument_is_not_given___complains():
    with pytest.raises(TypeError, match="has_args_and_kwargs"):
        BaseAction(SimpleChain, has_args_and_kwargs)  # type: ignore


def test_init___when_given_args_and_kwargs___stores_givens_correctly():
    action = BaseAction(SimpleChain, has_args_and_kwargs, 1, 2, 3, 4, 5, z=3, a=4)

    assert action.chaintype is SimpleChain
    assert action.function is has_args_and_kwargs
    assert action.args == (1, 2, 3, 4, 5)
    assert action.kwargs == {"z": 3, "a": 4}
    assert action.marker is None


def test_slots___adding_new_attributes___raises_an_error():
    action = BaseAction(SimpleChain, has_args_and_kwargs, y=1)

    with pytest.raises(AttributeError):
        action.uuu = 5  # type: ignore


def test_slots___weakref___are_possible():
    action = BaseAction(SimpleChain, has_args_and_kwargs, y=1)

    r = weakref.ref(action)

    assert r() == action


@pytest.mark.parametrize("tag", ["abc", None])
def test_tag___given_input___sets_marker(tag: str):
    action = BaseAction(SimpleChain, has_args_and_kwargs, y=1)

    action.tag(tag)

    assert action.marker == tag


@pytest.mark.parametrize(("x", "y", "z"), [(1, 2, 3), (4, 5, 6), (7, 8, 9)])
def test_call___given_input___generates_expected_output(x: int, y: int, z: int):
    action = BaseAction(SimpleChain, has_args_and_kwargs, y=y, z=z)
    another_action = BaseAction(SimpleChain, has_args_and_kwargs, y, z)

    assert action(x) == another_action(x) == (x - y) * z


def test_add___composing_with_none___returns_chain_containing_the_action():
    action = BaseAction(SimpleChain, has_args_and_kwargs, y=1)

    chain = action + None

    assert isinstance(chain, SimpleChain)
    assert chain.functions == (action,)


def test_add__composing_with_a_single_callable___generates_a_two_callable_chain():
    first = BaseAction(SimpleChain, has_args_and_kwargs, 1, 1)
    second = BaseAction(SimpleChain, has_args_and_kwargs, 0, 2)

    chain = first + second

    assert isinstance(chain, SimpleChain)
    assert chain.functions == (first, second)
    assert chain(3) == 4


def test_add___composing_with_an_iterable_of_callables___generates_a_multi_chain(
    transformations: TransformationFactory,
):
    callables = transformations.create("abc")
    action = BaseAction(SimpleChain, has_args_and_kwargs, y=1)

    chain = action + callables

    assert isinstance(chain, SimpleChain)
    assert chain.functions == (action, *callables)
    assert chain(1) == 0
    assert transformations.summary == "abc"


def test_radd___composing_with_none___returns_chain_containing_the_action():
    action = BaseAction(SimpleChain, has_args_and_kwargs, y=1)

    chain = None + action

    assert isinstance(chain, SimpleChain)
    assert chain.functions == (action,)


def test_radd__composing_with_a_single_callable___generates_a_two_callable_chain():
    first = BaseAction(SimpleChain, has_args_and_kwargs, 1, 1)

    def second(x: int) -> int:
        return 2 * x

    chain = second + first

    assert isinstance(chain, SimpleChain)
    assert chain.functions == (second, first)
    assert chain(3) == 5


def test_radd___composing_with_an_iterable_of_callables___generates_a_multi_chain(
    transformations: TransformationFactory,
):
    callables = transformations.create("abc")
    action = BaseAction(SimpleChain, has_args_and_kwargs, y=1)

    chain = callables + action

    assert isinstance(chain, SimpleChain)
    assert chain.functions == (*callables, action)
    assert chain(1) == 0
    assert transformations.summary == "abc"


def test_baseaction___when_pickled_with_picklable_function___can_be_unpickled():
    action = BaseAction(SimpleChain, has_args_and_kwargs, 1, 2, 3, z=2, w=4)

    pickled_action = pickle.dumps(action)
    recovered_action = pickle.loads(pickled_action)

    assert action == recovered_action


class Test:
    def __call__(self, x: int, y: int) -> int:
        return x + y


def test_baseaction___when_pickled_with_callable_class_instance___can_be_unpickled():
    action = BaseAction(SimpleChain, Test(), y=1)

    pickled_action = pickle.dumps(action)
    recovered_action = pickle.loads(pickled_action)

    # equality checkfails as ID is different
    assert isinstance(recovered_action.function, Test)


def test_eq___given_obviously_different_action___returns_false():
    action = BaseAction(SimpleChain, has_args_and_kwargs, y=1)

    def other(x: int) -> int:
        return x

    other_action = BaseAction(SimpleChain, other)

    assert action != other_action


def test_eq___if_equality_cannot_be_decided___forward_decisionmaking():
    action = BaseAction(SimpleChain, has_args_and_kwargs, y=1)

    class EqualsEverything:
        def __eq__(self, _: Any) -> bool:
            return True

    assert action == EqualsEverything()


def test_eq___given_obviously_equal_actions___returns_true():
    action = BaseAction(SimpleChain, has_args_and_kwargs, y=1)
    other_action = BaseAction(SimpleChain, has_args_and_kwargs, y=1)

    assert action == other_action


def test_eq___given_empty_string_and_none_as_marker___is_considered_equal():
    action = BaseAction(SimpleChain, has_args_and_kwargs, y=1)
    other_action = BaseAction(SimpleChain, has_args_and_kwargs, y=1).tag("")

    assert action == other_action


def test_eq___given_args_kwargs_mismatch___detects_equality_if_appropriate():
    action = BaseAction(SimpleChain, has_args_and_kwargs, 1, z=1)
    other_action = BaseAction(SimpleChain, has_args_and_kwargs, y=1, z=1)

    assert action == other_action


def test_eq___given_args_kwargs_mismatch___detects_inequality_if_appropriate():
    action = BaseAction(SimpleChain, has_args_and_kwargs, 1, z=1)
    other_action = BaseAction(SimpleChain, has_args_and_kwargs, y=2, z=1)

    assert action != other_action


def test_eq___given_subclass_instance___delegates_decision():
    action = BaseAction(SimpleChain, has_args_and_kwargs, 1, z=1)

    class SubAction(BaseAction):  # type: ignore
        def __eq__(self, other: Any) -> bool:
            return True

    other_action = SubAction(SimpleChain, has_args_and_kwargs, y=2, z=1)

    assert action == other_action


def test_baseaction___when_given_a_partial_function___works_correctly():
    # only named arguments here to keep x unfrozen
    partialed_func = functools.partial(has_args_and_kwargs, y=0, z=2)
    action = BaseAction(SimpleChain, partialed_func, w=2)

    assert action(1) == 4


def test_repr___given_an_action_wrapping_a_function___generates_expected_str():
    action = BaseAction(SimpleChain, has_args_and_kwargs, 1, 2, 3, k=1, z=2)

    assert repr(action) == "has_args_and_kwargs(1, 2, 3, k=1, z=2)"


@pytest.mark.parametrize(
    ("max_args", "args_repr"),
    [
        (1, "1, ..."),
        (2, "1, ..., 7"),
        (3, "1, 2, ..., 7"),
        (5, "1, 2, 3, ..., 6, 7"),
        (7, "1, 2, 3, 4, 5, 6, 7"),
    ],
)
def test_repr___given_many_arguments___reduces_presentation(
    max_args: int, args_repr: str, monkeypatch: Any
):
    monkeypatch.setenv("INSEQUENCE_MAX_ARGS", str(max_args))

    action = BaseAction(SimpleChain, has_args_and_kwargs, 1, 2, 3, 4, 5, 6, 7)

    assert repr(action) == f"has_args_and_kwargs({args_repr})"


def test_repr___given_many_keyword_arguments___reduces_presentation():
    action = BaseAction(SimpleChain, has_args_and_kwargs, 1, 2, 3, a=4, b=5, c=6)

    assert repr(action) == "has_args_and_kwargs(1, 2, 3, ..., b=5, c=6)"


def test_repr___given_many_keyword_arguments_with_marker___reduces_presentation():
    action = BaseAction(SimpleChain, has_args_and_kwargs, 1, 2, 3, a=4, b=5, c=6).tag(
        "a"
    )

    assert repr(action) == "has_args_and_kwargs(1, 2, 3, ..., b=5, c=6).tag('a')"


def test_repr___given_an_action_wrapping_a_partial___generates_expected_str():
    partial = functools.partial(has_args_and_kwargs, k=1, z=2)
    action = BaseAction(SimpleChain, partial, 1, u=3)

    assert repr(action) == f"{partial!r}(1, u=3)"


def test_repr___given_action_wrapping_a_function_with_marker___generates_expected_str():
    action = BaseAction(SimpleChain, has_args_and_kwargs, 1, 2, 3, k=1, z=2).tag("abc")

    assert repr(action) == "has_args_and_kwargs(1, 2, 3, k=1, z=2).tag('abc')"


def test_repr___given_a_local_function___incorporates_info():
    def test(x: str, y: str) -> str:
        return x + y

    action = BaseAction(SimpleChain, test, y="_end")

    assert repr(action) == (
        "test_repr___given_a_local_function___incorporates_info.<locals>.test(y='_end')"
    )


def test_repr___attempted_recursive_call___handled_gracefully():
    action = BaseAction(SimpleChain, has_args_and_kwargs, y=1)
    action.function = action  # type: ignore

    assert repr(action) == "...(y=1)"
