import typing
from typing import Any, NewType, Union

import numpy as np
from packaging import version

RealNumber = Union[float, int]
"""A real number."""

Number = Union[float, int, complex]
"""A real or complex number"""

Frequency = np.ndarray
"""The frequency expected by numpy array."""

Time = np.ndarray
"""The time expected by numpy array."""

X = np.ndarray
"""x array"""
Y = np.ndarray
"""y array"""

if hasattr(typing, 'Literal'):
    from typing import Literal
else:
    from typing_extensions import Literal

# from numpy.typing import ArrayLike

if version.parse(np.__version__) <= version.parse('1.19'):
    ArrayLike = NewType('ArrayLike', Any)
else:
    from numpy.typing import ArrayLike
