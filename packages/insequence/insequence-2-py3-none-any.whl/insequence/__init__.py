# SPDX-FileCopyrightText: Christian Heinze
#
# SPDX-License-Identifier: Apache-2.0
"""insequence package.

Python package to compose transformations and manage the execution of the composition.
"""

from .api import (
    Action,
    action,
    controller,
    modifiers,
)
from .chain import Chain, Transformation, Yields

__version__ = "2"

__all__ = [
    "action",
    "controller",
    "modifiers",
    "Yields",
    "Chain",
    "Action",
    "Transformation",
]
