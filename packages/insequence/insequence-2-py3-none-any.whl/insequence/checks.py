# SPDX-FileCopyrightText: Christian Heinze
#
# SPDX-License-Identifier: Apache-2.0
"""Check functions."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:  # pragma: no cover
    import contextlib
    from collections.abc import Iterable

    if sys.version_info < (3, 13):
        with contextlib.suppress(ImportError):
            from typing_extensions import TypeIs
    else:
        from typing import TypeIs

T = TypeVar("T")


def is_iterable(object_: T | Iterable[T]) -> TypeIs[Iterable[T]]:
    try:
        iter(object_)  # type: ignore [arg-type]
    except TypeError:
        return False
    return True
