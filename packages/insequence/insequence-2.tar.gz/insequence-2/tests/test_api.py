# SPDX-FileCopyrightText: Christian Heinze
#
# SPDX-License-Identifier: Apache-2.0
"""Test API."""

import concurrent.futures
import contextlib
import dataclasses
import functools
import pickle
from collections.abc import Generator
from typing import Any, TypeVar

import pytest
from base import TransformationFactory
from insequence import (
    Action,
    Chain,
    Yields,
    action,
    controller,
)
from insequence.api import _attributes, modifiers


def test_action_class___initialization___assigns_arguments_to_attributes():
    def func(x: int, y: int, z: int) -> int:
        return x * y + z

    action = Action(func, 1, z=2)

    assert action.function == func
    assert action.args == (1,)
    assert action.kwargs == {"z": 2}
    assert action.chaintype is Chain
    assert action(5) == 7


def test_attributes___providing_attributes___modifies_existing_attributes():
    @_attributes(__name__="abc", uuu=3)
    def test(x: int) -> int:
        return x

    assert test.__name__ == "abc"
    with pytest.raises(AttributeError):
        test.uuu  # noqa: B018


@action
def act(x: int, y: int, z: int) -> int:
    """test."""
    return x * y + z


def test_action___given_a_function___creates_action_builder():
    action_ = act(1, z=2)

    assert act.__module__ == __name__
    assert act.__doc__ == """test."""
    assert act.__name__ == "act"

    assert action_.args == (1,)
    assert action_.kwargs == {"z": 2}
    assert action_(3) == 5


def test_action___given_a_function___yields_a_picklable_result():
    action_ = act(1, z=2)

    pickled_action = pickle.dumps(action_)
    recovered_action = pickle.loads(pickled_action)

    assert recovered_action == action_


def test_action___lambdas___cannot_be_pickled():
    action_ = action(lambda x: x)

    with pytest.raises(AttributeError, match="pickle"):
        pickle.dumps(action_)


def test_action___when_removing_all_function_refs_first___unpickling_fails():
    def test_func(x: int) -> int:
        return x

    action_ = action(test_func)()

    pickled_action = pickle.dumps(action_)
    del test_func
    del action_
    with pytest.raises(pickle.UnpicklingError, match="failed to recover"):
        pickle.loads(pickled_action)


def test_action___when_called_with_parenthesis___creates_action_builder():
    @action()
    def func(x: int, y: int, z: int) -> int:
        """test."""
        return x * y + z

    action_ = func(1, z=2)

    assert func.__module__ == __name__
    assert func.__doc__ == """test."""
    assert func.__name__ == "func"

    assert action_.args == (1,)
    assert action_.kwargs == {"z": 2}
    assert action_(3) == 5


T = TypeVar("T")


def test_controller___given_a_function___copies_metadata_to_new_object():
    def control_(generator: Yields[T], message: str) -> Yields[T]:
        """Print a message before yielding."""
        for object_ in generator:
            print(message)
            yield object_

    control = controller(control_)

    assert control.__module__ == control_.__module__
    assert control.__name__ == f"{control_.__name__}_wrapper"
    assert control.__qualname__ == f"{control_.__qualname__}_wrapper"
    assert control.__doc__ == control_.__doc__


def test_controller___used_as_decorator_with_parenthesis___generates_factory():
    @controller()
    def test(x: Yields[T]) -> Yields[T]:
        """abc."""
        yield from x

    assert isinstance(test(), Action)
    assert test.__doc__ == "abc."


def test_controller___when_called___stores_functions_in_correct_module():
    @controller()
    def _(x: Yields[T]) -> Yields[T]:
        """abc."""
        yield from x

    from insequence import api

    api_store = getattr(api, Action.function_store_name())
    for module, _ in api_store:
        assert module == f"{api.__package__}.api"

    local_store = globals()[Action.function_store_name()]
    for module, _ in local_store:
        assert module == __name__


def test_controller___when_pickled___can_unpickled():
    @controller()
    def test(x: Yields[T]) -> Yields[T]:
        """abc."""
        yield from x

    chain = test() + test() + test()
    pickled_chain = pickle.dumps(chain)

    assert pickle.loads(pickled_chain) == chain


def test_repeat___given_nonpositive_count__complains():
    with pytest.raises(ValueError, match="nonpositive"):
        modifiers[int].repeat(0)(Chain())


@pytest.mark.parametrize("times", [2, 5, None])
def test_repeat___given_a_limit___repeats_accordingly(
    transformations: TransformationFactory, times: int | None
):
    @action
    def add(x: int, y: int) -> int:
        return x + y

    @action
    def stop_if_number_exceeds(x: int, limit: int) -> int:
        if x <= limit:
            return x
        raise StopIteration()

    chain = add(2) + stop_if_number_exceeds(20) + transformations.create("abcd")
    result = modifiers[int].repeat(times)(chain)(1)

    if times is not None:
        assert result == 1 + 2 * times
        assert transformations.summary == times * "abcd"
    else:
        assert result == 21
        assert transformations.summary == 9 * "abcd"


def test_repeat___when_applied_to_a_pickleable_chain___retains_pickleability():
    @action
    def add_prefix(suffix: str, prefix: str) -> str:
        return prefix + suffix

    prepend_underscore = add_prefix("_")
    prepend_pre = add_prefix("pre")

    chain = prepend_underscore + prepend_pre
    new_chain = modifiers[str].repeat(2)(chain)

    chain_pickle = pickle.dumps(chain)
    new_chain_pickle = pickle.dumps(new_chain)

    assert pickle.loads(chain_pickle) == chain
    assert pickle.loads(new_chain_pickle) == new_chain


def test_repeat___given_chain_with_non_one_shot_controller___completely_repeats(
    transformations: TransformationFactory,
):
    @contextlib.contextmanager
    def manager(factory: TransformationFactory) -> Generator[None, None, None]:
        factory.log.append("{")
        yield None
        factory.log.append("}")

    chain = modifiers[int].use_context(
        functools.partial(manager, factory=transformations)
    )(Chain(*transformations.create("abc")))

    result = modifiers[int].repeat(3)(chain)(0)

    assert result == 0
    assert transformations.summary == 3 * "{a}{b}{c}"


def test_use_context___when_given_a_context_manager__applies_functions_in_context(
    transformations: TransformationFactory,
):
    @dataclasses.dataclass
    class Manager:
        factory: TransformationFactory

        def __enter__(self) -> None:
            self.factory.log.append("[")

        def __exit__(self, *_: Any) -> bool:
            self.factory.log.append("]")
            return False

    chain = Chain(*transformations.create("abc"))

    result = modifiers[int].use_context(Manager(transformations))(chain)(0)

    assert result == 0
    assert transformations.summary == "[a][b][c]"


def test_use_context___when_given_a_callable_generating_a_one_shot_manager___works(
    transformations: TransformationFactory,
):
    @contextlib.contextmanager
    def manager(factory: TransformationFactory) -> Generator[None, None, None]:
        factory.log.append("{")
        yield None
        factory.log.append("}")

    chain = Chain(*transformations.create("abc"))

    result = modifiers[int].use_context(
        functools.partial(manager, factory=transformations)
    )(chain)(0)

    assert result == 0
    assert transformations.summary == "{a}{b}{c}"


@pytest.mark.parametrize(
    ("skip_values", "expectation"),
    [
        (
            (
                0,
                "b",
            ),
            "c",
        ),
        (
            (
                1,
                "a",
            ),
            "c",
        ),
        ((2,), "ab"),
        (("c",), "ab"),
    ],
)
def test_skip___when_given_indexes_and_markers___skip_mentioned_operations(
    skip_values: tuple[str | int, ...], expectation: str
):
    @action
    def add(x: str, y: str) -> str:
        return x + y

    chain = add("a").tag("a") + add("b").tag("b") + add("c").tag("c")

    result = modifiers[str].skip(*skip_values)(chain)("")

    assert result == expectation


def test_skip___when_combined_with_repeat___order_matters():
    @action
    def add(x: str, y: str) -> str:
        return x + y

    chain = add("b") + add("c")

    # this skips the first cycle through the entire tuple
    b = modifiers[str]
    assert (b.repeat(3) + b.skip(1))(chain)("a") == "abcbc"
    assert (b.skip(1) + b.repeat(2))(chain)("a") == "abb"


@pytest.mark.parametrize(
    ("start", "end", "expectation"),
    [
        (0, 1, "a"),
        (0, 3, "abc"),
        (1, 4, "bcd"),
        (3, 1, ""),
        (-1, 1000, "abcde"),
        (2, 4, "cd"),
    ],
)
def test_window___when_give_numeric_endpoints___extracts_the_expected_subchain(
    start: int, end: int, expectation: str
):
    @action
    def add(x: str, y: str) -> str:
        return x + y

    chain = add("a") + add("b") + add("c") + add("d") + add("e")

    result = modifiers[str].window(start, end)(chain)("")

    assert result == expectation


@pytest.mark.parametrize(
    ("start", "end", "expectation"),
    [
        (0, "3", "abc"),
        (0, "1", ""),
        ("1", "1", ""),
        ("1", "3", "abc"),
        (2, "1", ""),
        (3, "1", ""),
        ("a", "b", ""),
        ("a", 3, ""),
        ("1", "j", "abcde"),
    ],
)
def test_window___when_give_arbitrary_endpoints___extracts_the_expected_subchain(
    start: int | str, end: int | str, expectation: str
):
    @action
    def add(x: str, y: str) -> str:
        return x + y

    chain = (
        add("a").tag("1")
        + add("b").tag("2")
        + add("c").tag("1")
        + add("d").tag("3")
        + add("e").tag("4")
    )

    result = modifiers[str].window(start, end)(chain)("")

    assert result == expectation


@pytest.mark.parametrize(
    ("start", "end", "start_inclusive", "end_inclusive", "expectation"),
    [
        (0, "3", True, False, "abc"),
        (0, "3", True, True, "abcd"),
        (0, "3", False, True, "bcd"),
        (0, "3", False, False, "bc"),
        ("2", "j", True, False, "bcde"),
        (None, "2", False, False, "a"),
        (None, "2", False, True, "ab"),
        (2, "4", False, True, "de"),
        (2, "3", False, False, ""),
        (3, 10, True, True, "de"),
    ],
)
def test_window___when_modifying_endpoint_inclusivity___extracts_the_expected_subchain(
    start: int, end: int, start_inclusive: bool, end_inclusive: bool, expectation: str
):
    @action
    def add(x: str, y: str) -> str:
        return x + y

    chain = (
        add("a").tag("1")
        + add("b").tag("2")
        + add("c").tag("1")
        + add("d").tag("3")
        + add("e").tag("4")
    )

    result = modifiers[str].window(
        start, end, start_inclusive=start_inclusive, end_inclusive=end_inclusive
    )(chain)("")

    assert result == expectation


@action
def scale_and_move(x: float, move: float, scale: float) -> float:
    return move + x * scale


def test_action___when_applied_concurrenlty___works_as_expected():
    move_by_one = scale_and_move(move=1.0, scale=1.0)
    scale_by_two = scale_and_move(move=0.0, scale=2.0)
    chain = modifiers[float].repeat(2)(move_by_one + scale_by_two)

    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
        results = executor.map(chain, [2.0, 5.0, 7.0])

    assert list(results) == [14.0, 26.0, 34.0]


@pytest.mark.parametrize(("in_", "expected_out"), [(1.0, 5.0), (2.0, 6.0), (0.0, 4.0)])
def test_append___when_applied_to_a_chain___appends_specified_action(
    in_: float, expected_out: float
):
    chain = (
        scale_and_move(move=2.0, scale=1.0)
        + scale_and_move(move=1.0, scale=2.0)
        + scale_and_move(move=2.0, scale=4.0)
    )

    out = modifiers[float].append(lambda x: x / 2.0)(chain)(in_)

    assert out == expected_out


@pytest.mark.parametrize(("in_", "expected_out"), [(1.0, 9.0), (2.0, 10.0), (0.0, 8.0)])
def test_prepend___when_applied_to_a_chain___prepends_specified_action(
    in_: float, expected_out: float
):
    chain = (
        scale_and_move(move=2.0, scale=1.0)
        + scale_and_move(move=1.0, scale=2.0)
        + scale_and_move(move=2.0, scale=4.0)
    )

    out = modifiers[float].prepend(lambda x: x / 2.0)(chain)(in_)

    assert out == expected_out


def stop_if_exceeds_fifty(x: float) -> float:
    if x > 50.0:
        raise StopIteration()
    return x


def test_pickle___when_given_complex_object___can_be_unpickled():
    b = modifiers[float]
    chain = b.append(stop_if_exceeds_fifty)(
        b.repeat()(
            scale_and_move(move=2.0, scale=2.0) + scale_and_move(move=2.0, scale=2.0)
        )
    )

    pickled = pickle.dumps(chain)

    assert pickle.loads(pickled) == chain


def test_chain_modifier_namespace___when_attempting_instantiation___complains():
    with pytest.raises(NotImplementedError, match="does not support instantiation"):
        modifiers[int]()
