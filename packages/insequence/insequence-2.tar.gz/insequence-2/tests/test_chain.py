# SPDX-FileCopyrightText: Christian Heinze
#
# SPDX-License-Identifier: Apache-2.0
"""Test chain."""

import contextlib
import functools
import io
import itertools
import pickle
import string
import warnings
from collections.abc import Generator, Iterable
from typing import Any, TypeVar

import pytest
from base import TransformationFactory
from insequence import Chain, Transformation, Yields


def test_format_n_max___when_env_variable_set___return_its_value(monkeypatch: Any):
    monkeypatch.setenv("INSEQUENCE_CHAIN_TERMS", "10")
    assert Chain._format_n_max() == 10


def test_format_n_max___when_env_variable_not_set___return_default(monkeypatch: Any):
    with contextlib.suppress(KeyError):
        monkeypatch.delenv("INSEQUENCE_CHAIN_TERMS")
    assert Chain._format_n_max() == 5


@pytest.fixture
def controller(
    transformations: TransformationFactory,
) -> Transformation[Yields[Transformation[int]]]:
    def controller_(
        functions: Iterable[Transformation[int]],
    ) -> Generator[Transformation[int], None, None]:
        for function in functions:
            transformations.log.append("|")
            yield function

    return controller_


def test_init___given_a_mix_of_functions_and_none___keeps_only_functions(
    transformations: TransformationFactory,
):
    functions = (
        transformations.create(range(3)),
        transformations.create(range(3, 6)),
        transformations.create(range(6, 9)),
    )

    chain = Chain(*functions[0], None, *functions[1], None, *functions[2], None)

    assert all(
        f == g
        for f, g in zip(chain.functions, itertools.chain.from_iterable(functions))
    )


@pytest.mark.parametrize("controller", [None, lambda fs: tuple(fs)[:1]])
def test_repr___short_chain_without_and_with_controller___yields_expected_string(
    transformations: TransformationFactory,
    controller: Transformation[Yields[Transformation[int]]] | None,
    monkeypatch: Any,
):
    monkeypatch.setenv("INSEQUENCE_CHAIN_TERMS", "4")
    limit = Chain._format_n_max()

    chain_indexes = "abc"
    if controller is not None:
        controller_: Chain[Yields[Transformation[int]]] | None = Chain(
            controller, controller
        )
    else:
        controller_ = None
    chain = Chain(*transformations.create(chain_indexes), controller=controller_)
    chain_inner = ", ".join(f"[[{i}]]" for i in chain_indexes[:limit])

    if controller is None:
        assert repr(chain) == f"Chain({chain_inner})"
    else:
        assert repr(chain) == f"Chain({chain_inner}, controller={controller_!r})"


@pytest.mark.parametrize(
    ("controller", "cycle_limit"),
    [(None, 2), (lambda fs: tuple(fs)[:1], -1), (lambda x: x, 1), (None, None)],
)
def test_repr___short_chain_without_and_with_extras___yields_expected_string(
    transformations: TransformationFactory,
    controller: Transformation[Yields[Transformation[int]]] | None,
    cycle_limit: int | None,
    monkeypatch: Any,
):
    monkeypatch.setenv("INSEQUENCE_CHAIN_TERMS", "4")
    limit = Chain._format_n_max()

    chain_indexes = "abc"
    chain = Chain(
        *transformations.create(chain_indexes),
        controller=controller,
        cycle_limit=cycle_limit,
    )
    chain_inner = ", ".join(f"[[{i}]]" for i in chain_indexes[:limit])

    assert chain.cycle_limit == cycle_limit
    match (controller, cycle_limit):
        case (None, 1):
            assert repr(chain) == f"Chain({chain_inner})"
        case (None, cycle_limit):
            assert repr(chain) == f"Chain({chain_inner}, cycle_limit={cycle_limit!r})"
        case (controller, 1):
            assert repr(chain) == f"Chain({chain_inner}, controller={controller!r})"
        case _:
            assert repr(chain) == (
                f"Chain({chain_inner}, controller={controller!r},"
                f" cycle_limit={cycle_limit!r})"
            )


@pytest.mark.parametrize(
    ("controller", "cycle_limit"),
    [(None, None), (lambda fs: tuple(fs)[:1], 0), (None, 2)],
)
def test_repr___long_chain_without_and_with_extras___yields_expected_string(
    transformations: TransformationFactory,
    controller: Transformation[Yields[Transformation[int]]] | None,
    cycle_limit: int | None,
    monkeypatch: Any,
):
    monkeypatch.setenv("INSEQUENCE_CHAIN_TERMS", "4")
    limit = Chain._format_n_max()

    chain_indexes = "abcdef"
    chain = Chain(
        *transformations.create(chain_indexes),
        controller=controller,
        cycle_limit=cycle_limit,
    )
    chain_inner = ", ".join(f"[[{i}]]" for i in chain_indexes[:limit]) + ", ..."

    assert chain.cycle_limit == cycle_limit
    match (controller, cycle_limit):
        case (None, 1):
            assert repr(chain) == f"Chain({chain_inner})"
        case (None, cycle_limit):
            assert repr(chain) == f"Chain({chain_inner}, cycle_limit={cycle_limit!r})"
        case (controller, 1):
            assert repr(chain) == f"Chain({chain_inner}, controller={controller!r})"
        case _:
            assert repr(chain) == (
                f"Chain({chain_inner}, controller={controller!r},"
                f" cycle_limit={cycle_limit!r})"
            )


def test_eq___given_identical_copy___finds_equality(
    transformations: TransformationFactory,
):
    chain = Chain(*transformations.create("abc"))

    assert chain == Chain(*chain)


def test_eq___given_copy_with_different_controller___finds_inequality(
    transformations: TransformationFactory,
):
    chain = Chain(*transformations.create("abc"))
    new_chain = Chain(
        *chain.functions, controller=lambda fs: (f for i, f in enumerate(fs) if i < 1)
    )

    assert chain != new_chain


def test_eq___given_copy_with_different_cycle_limit___finds_inequality(
    transformations: TransformationFactory,
):
    chain = Chain(*transformations.create("abc"))
    new_chain = Chain(*chain.functions, cycle_limit=None)

    assert chain != new_chain


def test_eq___given_different_type_but_identical_content___finds_inequality(
    transformations: TransformationFactory,
):
    chain = Chain(*transformations.create("abc"))

    assert chain != list(chain)


def test_eq___if_equality_cannot_be_decided___forward_decisionmaking(
    transformations: TransformationFactory,
):
    chain = Chain(*transformations.create("abc"))

    class EqualsEverything:
        def __eq__(self, _: Any) -> bool:
            return True

    assert chain == EqualsEverything()


@pytest.mark.parametrize(
    ("cycle_limit", "summary"),
    [(-2, ""), (0, ""), (1, "abc"), (3, "abcabcabc"), (None, 33 * "abc")],
)
def test_yield_functions___given_various_cycle_limits___yields_as_expected(
    transformations: TransformationFactory, cycle_limit: int | None, summary: str
):
    chain = Chain(*transformations.create("abc"), cycle_limit=cycle_limit)

    x = 1
    for f in chain._yield_functions():
        x = f(x)
        if len(transformations.summary) == 99:
            return

    assert transformations.summary == summary


def test_iter___when_controller_is_present___adapts_output(
    transformations: TransformationFactory,
    controller: Transformation[Yields[Transformation[int]]] | None,
):
    chain = Chain[int](*transformations.create("abc"))
    chain_with_controller = Chain[int](
        *transformations.create("abc"), controller=controller
    )
    new_chain = Chain[int](*chain, *chain_with_controller)

    assert len(list(chain)) == 3
    assert len(list(chain.copy(controlled_by=controller))) == 1
    assert len(list(new_chain)) == len(new_chain.functions) == 4


def test_controller___when_combined_with_cycle_limit___behaves_as_expected():
    T = TypeVar("T")

    def skip_second(g: Yields[T]) -> Yields[T]:
        for i, f in enumerate(g):
            if i == 1:
                continue
            yield f

    chain = Chain(
        lambda x: x + "b", lambda x: x + "c", controller=skip_second, cycle_limit=3
    )

    assert chain("a") == "abbcbc"


def test_call___when_called___runs_all_functions(
    transformations: TransformationFactory,
):
    chain = Chain[int](*transformations.create(range(10)))

    chain(0)

    assert transformations.summary == "0123456789"


@pytest.mark.parametrize(
    ("cycle_limit", "summary"), [(1, "|a|b|c"), (2, 2 * "|a|b|c"), (-1, "")]
)
def test_call___when_provided_with_controller___uses_controller(
    transformations: TransformationFactory,
    controller: Transformation[Yields[Transformation[int]]],
    cycle_limit: int | None,
    summary: str,
):
    chain = Chain[int](
        *transformations.create("abc"), controller=controller, cycle_limit=cycle_limit
    )

    chain(0)

    assert transformations.summary == summary


@pytest.fixture
def factory_and_stoppable_chain(
    transformations: TransformationFactory,
) -> tuple[TransformationFactory, Chain[int]]:
    def stops_pipeline_if_positive(x: int) -> int:
        if x > 0:
            raise StopIteration
        return x + 1

    chain = Chain(
        *transformations.create("abc"),
        stops_pipeline_if_positive,
        *transformations.create("def"),
    )
    return transformations, chain


def test_call___if_function_raises_stop_iteration___execution_terminates(
    factory_and_stoppable_chain: tuple[TransformationFactory, Chain[int]],
):
    transformations, stoppable_chain = factory_and_stoppable_chain

    result = stoppable_chain(1)

    assert result == 1
    assert transformations.summary == "abc"


def test_call___if_function_does_not_raise_stop_iteration___execution_carries_on(
    factory_and_stoppable_chain: tuple[TransformationFactory, Chain[int]],
):
    transformations, stoppable_chain = factory_and_stoppable_chain

    result = stoppable_chain(0)

    assert result == 1
    assert transformations.summary == "abcdef"


def test_call___if_function_raises_exception___exception_is_propagated(
    transformations: TransformationFactory,
):
    def raises_value_error_if_positive(x: int) -> int:
        if x > 0:
            raise ValueError("positive")
        return x + 1

    chain = Chain(
        *transformations.create(range(3)),
        raises_value_error_if_positive,
        *transformations.create(range(3, 6)),
    )

    with pytest.raises(ValueError, match="raises_value_error_if_positive.*: positive"):
        chain(1)


@pytest.mark.parametrize("cycle_limit", [0, 1, 5])
def test_call___when_a_context_manager_is_injected___the_context_is_active(
    transformations: TransformationFactory, capsys: Any, cycle_limit: int
):
    def capture_warnings(
        functions: Iterable[Transformation[int]],
    ) -> Generator[Transformation[int], None, None]:
        for function in functions:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=Warning)
                yield function

    def issues_a_warning(x: int) -> int:
        warnings.warn(message="this is a warning", category=Warning, stacklevel=1)
        return x + 1

    chain = Chain(
        *transformations.create("abc"),
        issues_a_warning,
        *transformations.create("def"),
        controller=capture_warnings,
        cycle_limit=cycle_limit,
    )

    result = chain(1)

    assert all(b == "" for b in capsys.readouterr())
    assert result == 1 + cycle_limit


def test_copy___when_called___does_not_copy_function_tuple(
    transformations: TransformationFactory,
):
    chain = Chain(*transformations.create(string.ascii_letters[:10]))

    chain_copy = chain.copy(controlled_by=None)

    assert id(chain.functions) == id(chain_copy.functions)


def test_copy___when_called_without_argument___produces_an_exact_copy(
    transformations: TransformationFactory,
):
    chain = Chain(*transformations.create(string.ascii_letters[:10]))

    chain_copy = chain.copy()

    assert chain == chain_copy


@pytest.mark.parametrize(
    ("old_cl", "new_cl"), [(1, 2), (None, 1), (4, None), (-1, 7), (1, 1), (None, None)]
)
def test_copy___when_called_with_cycle_limit___copies_as_expected(
    transformations: TransformationFactory, old_cl: int | None, new_cl: int | None
):
    chain = Chain(*transformations.create("abcd"), cycle_limit=old_cl)
    chain_copy = chain.copy(with_cycle_limit=new_cl)

    assert chain.cycle_limit == old_cl
    assert chain_copy.cycle_limit == new_cl
    assert (chain == chain_copy) == (old_cl == new_cl)


@pytest.mark.parametrize(
    ("controller", "new_controller"),
    list(
        (x, y)
        for x, y in zip(
            (None, lambda fs: tuple(fs)[:1]), (lambda fs: tuple(fs)[:1], None)
        )
    ),
)
def test_copy___when_called_with_controller___copies_accordingly(
    transformations: TransformationFactory,
    controller: Transformation[Yields[Transformation[int]]] | None,
    new_controller: Transformation[Yields[Transformation[int]]] | None,
):
    chain = Chain[int](*transformations.create("abc"))
    chain.controller = controller

    chain_copy = chain.copy(controlled_by=new_controller)

    assert chain is not chain_copy
    assert chain.functions is chain_copy.functions
    assert chain.controller is controller
    assert chain_copy.controller is new_controller


def test_copy___modifiying_all_extras___has_expected_effect(
    transformations: TransformationFactory,
):
    chain = Chain[int](*transformations.create("abc"))
    chain_copy = chain.copy(controlled_by=lambda x: x, with_cycle_limit=7)

    assert chain.controller is None
    assert chain.cycle_limit == 1
    assert chain_copy.controller is not None
    assert chain_copy.cycle_limit == 7


def test_add___given_none___returns_a_copy_of_the_chain(
    transformations: TransformationFactory,
):
    chain = Chain(*transformations.create("abc"))

    new_chain = chain + None

    assert new_chain is not chain
    assert new_chain == chain


def test_add___given_another_callable___concatenates(
    transformations: TransformationFactory,
):
    chain = Chain(*transformations.create("abc"))

    def add(x: int, y: int, transformations: TransformationFactory) -> int:
        transformations.log.append("d")
        return x + y

    add_2 = functools.partial(add, y=2, transformations=transformations)

    new_chain = chain + add_2

    assert new_chain is not chain
    assert new_chain != chain
    assert new_chain(1) == chain(1) + 2
    assert transformations.summary == "abcdabc"


def test_add___given_another_iterable___concatenates(
    transformations: TransformationFactory,
):
    chain = Chain[int](*transformations.create(string.ascii_letters[:4]))
    other = transformations.create(string.ascii_letters[4:10])

    (chain + other)(0)

    assert transformations.summary == "".join(string.ascii_letters[:10])


def test_radd___given_none___returns_a_copy_of_the_chain(
    transformations: TransformationFactory,
):
    chain = Chain(*transformations.create("abc"))

    new_chain = None + chain

    assert new_chain is not chain
    assert new_chain == chain


def test_radd___given_another_callable___concatenates(
    transformations: TransformationFactory,
):
    chain = Chain(*transformations.create("abc"))

    def add(x: int, y: int, transformations: TransformationFactory) -> int:
        transformations.log.append("d")
        return x + y

    add_2 = functools.partial(add, y=2, transformations=transformations)

    new_chain = add_2 + chain

    assert new_chain is not chain
    assert new_chain != chain
    assert new_chain(1) == chain(1) + 2
    assert transformations.summary == "dabcabc"


def test_radd___given_another_iterable___concatenates(
    transformations: TransformationFactory,
):
    chain = Chain[int](*transformations.create(string.ascii_letters[4:10]))
    other: list[Transformation[int]] = transformations.create(string.ascii_letters[:4])

    (other + chain)(0)

    assert transformations.summary == "".join(string.ascii_letters[:10])


def add_1(x: int) -> int:
    return x + 1


def test_chain___when_components_can_be_pickled___chain_can_be_pickled():
    chain = Chain(add_1, add_1, add_1)

    pickled_chain = pickle.dumps(chain)
    recovered_chain = pickle.loads(pickled_chain)

    assert recovered_chain == chain
    assert recovered_chain(1) == chain(1) == 4


_BUFFER = io.StringIO()


def control(generator: Yields[Transformation[int]]) -> Yields[Transformation[int]]:
    for function in generator:
        _BUFFER.write(f"{function}\n")
        yield function


def test_chain___when_components_and_controller_can_be_pickled___chain_can():
    chain = Chain(
        add_1,
        add_1,
        add_1,
        cycle_limit=2,
        controller=Chain(control, control, cycle_limit=2),
    )

    assert chain(1) == 7
    assert _BUFFER.getvalue().strip().split("\n") == 24 * [str(add_1)]

    pickled_chain = pickle.dumps(chain)
    recovered_chain = pickle.loads(pickled_chain)

    assert recovered_chain == chain
