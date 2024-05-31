from copy import deepcopy
from typing import Optional

import numpy as np

from .help_types import ArrayLike, RealNumber
from . import default_methods as default_methods


class Axis:
    def __init__(
        self,
        size: int,
        sample: RealNumber = 1,
        start: RealNumber = 0,
        end: Optional[RealNumber] = None,
    ) -> None:
        """The representation of some array axis.

        This is the axis description. The axis describes the size, sample
        spacing between elements, start and end.

        Raises:
            TypeError: Raise this exception if type of size is not int.
            ValueError: Raise this exception if size less then 1.

        Args:
            size (int): is size of axis
            sample (RealNumber): is sample of axis.
            start (RealNumber): is start of axis.
            end (RealNumber): is end of axis.
        """
        _check_size(size)
        self._size = size
        self._sample = sample
        self._start = start
        self._end = end
        self._array: Optional[np.ndarray] = None

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, value: int) -> None:
        _check_size(value)
        self._size = value
        self._reset_property()

    @property
    def sample(self) -> RealNumber:
        return self._sample

    @sample.setter
    def sample(self, value: RealNumber) -> None:
        self._sample = value
        self._reset_property()

    @property
    def start(self) -> RealNumber:
        return self._start

    @start.setter
    def start(self, value: RealNumber) -> None:
        self._start = value
        self._reset_property()

    @property
    def end(self) -> RealNumber:
        if self._end is None:
            self._end = self.start + self.sample * (self.size - 1)
        return self._end

    @end.setter
    def end(self, value: RealNumber) -> None:
        self._end = value

    @property
    def array(self) -> np.ndarray:
        """Representation of array axis into numpy.ndarray

        Returns:
            numpy.ndarray: numpy array of axis
        """
        return self.get_array()

    def get_array(self) -> np.ndarray:
        """Create array of numpy from Axis, using, start, end and sample of Axis.

        Args:
            self (Axis): instance of Axis

        Returns:
            numpy.ndarray: numpy array of axis.
        """
        result = np.linspace(self.start, self.end, self.size)
        return result

    def copy(self) -> 'Axis':
        """Copy of axis.

        Returns:
            Axis: copy of axis
        """
        return deepcopy(self)

    @staticmethod
    def get_common_axis(
        axis1: 'Axis', axis2: 'Axis', is_correct_end=False
    ) -> 'Axis':
        """Specifies the overall axis.

        Finds the general sample rate and beginning and end of sequence.
        A method by which to find the common sequence of numbers along
        the axis, obtained from two other sequences along the axis.

        Args:
            axis1 (Axis): first axis.
            axis2 (Axis): second axis.

        Returns:
            Axis: return common Axis.
        """

        return default_methods.get_common_axis(axis1, axis2, is_correct_end)

    @staticmethod
    def get_using_end(
        start: RealNumber,
        end: RealNumber,
        sample: RealNumber = 1.0,
        is_correct_end: bool = True,
    ) -> 'Axis':
        """Create instance of Axis using start, end and sample params of axis.

        Args:
            start (RealNumber): start position of axis.
            end (RealNumber): end position of axis.
            sample (RealNumber): sample of axis.
            is_correct_end (bool): Default to True. Checking the correctness of
                the end of the axis. If value is False, no end will be set
                for the instance.

        Returns:
            Axis: new instance of Axis.
        """
        return default_methods.get_using_end(
            start, end, sample, is_correct_end
        )

    @staticmethod
    def get_from_array(
        x: ArrayLike, sample: Optional[RealNumber] = None
    ) -> 'Axis':
        """Create instance of Axis from some array of numbers.

        Args:
            x (ArrayLike): input array of numbers.
            sample (RealNumber, optional): sample of axis for array.
                Default is None.

        Returns:
            Axis: new instance of Axis.
        """

        return default_methods.get_axis_from_array(x, sample)

    def _reset_property(self) -> None:
        self._end = None
        self._array = None

    def __str__(self):
        result = (
            f'size: {self.size}\n'
            f'sample: {self._sample}\n'
            f'start: {self._start}\n'
            f'end: {self._end}\n'
        )

        return result
    
    def __eq__(self, other: 'Axis'):
        return ( 
            self.start == other.start 
            and self.size == self.size 
            and self.sample == self.sample
        )
    
    def __ne__(self, other: 'Axis'):
        return not self.__eq__(other)

def _check_size(size: int) -> None:
    if not isinstance(size, int):
        raise TypeError(
            f'The wrong type os size parameters. Type of size is {type(size)}'
        )

    if size < 1:
        raise ValueError(
            f'The size of axis should be positive value. Size is equal to {size}'
        )
