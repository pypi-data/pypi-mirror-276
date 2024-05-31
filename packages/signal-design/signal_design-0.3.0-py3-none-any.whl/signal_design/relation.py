import logging
from copy import deepcopy
from typing import Tuple, Type, TypeVar, Union

import numpy as np

from signal_design import axis

from .core import MathOperation, RelationProtocol
from .exc import BadInputError, NotEqualError, TypeFuncError
from .help_types import ArrayLike, Number, RealNumber
from . import default_methods as default_methods

R = TypeVar('R', bound='Relation')
"""Description first `Relation`."""

R2 = TypeVar('R2', bound='Relation')
"""Description second `Relation`."""


class Relation(RelationProtocol):
    """A representation of dependency y from x (y = f(x)).

    The class describe the dependency between x, y. x is `Axis` instance showing
    the start of sequence, size of sequence and the sample space between elements.
    They consist of real. The size of :class:`Axis` must be equal length of
    `y` sequence.

    For the instance of `Relation` class, define the basic mathematical operations:
    addition (+), subtraction(-), multiplication(\\*), division(/),
    exponentiation (\\*\\*) and their unary representation (+=, -=, \\*=, /=).
    The result of the operation is a new instance of the `Relation` class.

    Determined correlation and convolution between two instances
    (methods: correlate and convolve).

    WARNING!!! When inheriting the `Relation` class, it is important to write correctly
    constructor. It must match the constructor of the `Relation` class.
    Because some methods return a type(self)(...). For example,
    addition method (def __add__(self: R, other: Union['Relation', Num]) -> R).
    Or predefine these methods in the inherited class.

    Raises:
        TypeError: Raise this exception if wrong parameters setting to Axis.
        ValueError: Raise this exception if wrong parameters setting to Axis.
        BadInputError: Raise this exception if we don't have enough data.
        NotEqualError: Raise this exception if we try create instance use
            different length of sequence numbers for x and y.
        TypeFuncError: Raise an exception, when execute some function with
            unexpected type of value.

    Returns:
        _type_: Type of Relation.
    """

    def __init__(
        self,
        x: Union[RelationProtocol, 'axis.Axis', ArrayLike],
        y: Union[ArrayLike, None] = None,
    ) -> None:
        """Initialization of instance of `Relation`.

        Args:
            x (Union[RelationProtocol, ArrayLike, Axis]):
                The `Relation` class, or a class derived from the `Relation`
                class, or instance of `Axis` or an `ArrayLike` object
                containing numbers(real or complex). if x is `ArrayLike` then
                it will be converted to `Axis` instance use method
                *get_array_axis_from_array_method* from config.Config.class

            y (ArrayLike, optional):
                None or array_like object containing real or complex numbers.
                If it is not None then it will be converted to numpy.ndarray.
                Defaults to None.

        Raises:
            TypeError: Raise this exception if wrong parameters setting to Axis.
            ValueError: Raise this exception if wrong parameters setting to Axis.
            BadInputError: Raise this exception if we don't have enough data.
            NotEqualError: Raise this exception if we try create instance use
        """

        if isinstance(x, RelationProtocol):
            self._x = x.x.copy()
            self._y = x.y.copy()
            if y is not None:
                logging.warning(f'x is instance of {type(x)}, "y" was ignored')
            return None

        if y is None:
            raise BadInputError('y is absent. Not enough data!')

        y = np.array(y)

        if not isinstance(x, axis.Axis):
            x = axis.Axis.get_from_array(x)

        if x.size != y.size:
            raise NotEqualError(x.size, y.size)

        self._x, self._y = x, y

    @property
    def x(self) -> 'axis.Axis':
        """Axis of relation.

        Returns:
            Axis: array axis of relation.
        """
        return self._x

    @property
    def y(self) -> np.ndarray:
        """Result of relation of y(x)

        Returns:
            numpy.ndarray: array of numbers represent relation of y(x)
        """
        return self._y

    @property
    def start(self) -> RealNumber:
        """Start of array axis x.

        Returns:
            RealNumber: start number of array axis x.
        """
        return self._x.start

    @start.setter
    def start(self, value: RealNumber) -> None:
        """Setter for start.

        Args:
            value (RealNumber): set start for array axis x.
        """
        self._x.start = value

    @property
    def sample(self) -> RealNumber:
        """Sample for array axis x.

        Returns:
            RealNumber: sample of array axis x.
        """
        return self._x.sample

    @sample.setter
    def sample(self, value: RealNumber) -> None:
        """Setter for sample.

        Args:
            value (RealNumber): set sample for array axis x.
        """
        self._x.sample = value

    @property
    def size(self) -> int:
        """size of array axis x.

        Returns:
            int: integer number of array size x.
        """

        return self._x.size

    @size.setter
    def size(self, value: int) -> None:

        self._x.size = value

    @property
    def end(self) -> RealNumber:
        """End of array axis x.

        Returns:
            RealNumber: end number of array axis x.
        """
        return self._x.end

    @end.setter
    def end(self, value: RealNumber):
        """Setter for start.

        Args:
            value (RealNumber): set end for array axis x.
        """
        self._x.end = value

    @property
    def array(self) -> np.ndarray:
        """Get array representation of array axis x.

        Returns:
            numpy.ndarray: array of numpy.
        """
        return self._x.array

    def get_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Return the data of the object.

        Raises:
            NotEqualError: After manipulating on x Axis, the size of the
                extracted arrays is checked. If they are different then raise
                that error.

        Returns:
            Tuple[numpy.ndarray, numpy.ndarray]: tuple of two number sequence
        """

        if self._x.size != self._y.size:
            raise NotEqualError(self._x.size, self._y.size)

        return self.array.copy(), self.y.copy()

    def max(self) -> Number:
        """Get maximum of Relation.

        Returns:
            Number: maximum of y array.
        """
        return self._y.max()

    def min(self) -> Number:
        """Get minimum of Relation.

        Returns:
            Number: minimum of y array.
        """
        return self._y.min()

    def get_norm(self) -> RealNumber:
        """Get signal rate.

        Calculated in terms of signal energy.

        Returns:
            Number: signal rate
        """

        square_self = self**2
        return default_methods.one_integrate(square_self) / (self.sample)

    def select_data(
        self: R,
        start: Union[Number, None] = None,
        end: Union[Number, None] = None,
    ) -> R:
        """Select data using x-axis

        Args:
            self (R): instance of Relation
            start (Number, optional): new start of relation x. Defaults to None.
            end (Number, optional): new end of relation x. Defaults to None.

        Returns:
            R: new instance of Relation.
        """

        if start is None:
            start = self.start

        if end is None:
            end = self.end

        array = self.array

        is_selected = np.logical_and(
            np.greater_equal(array, start), np.less_equal(array, end)
        )
        selected_x = array[is_selected]

        new_x_array = axis.Axis(
            start=selected_x[0], sample=self.sample, size=selected_x.size
        )

        return type(self)(new_x_array, self.y[is_selected])

    def exp(self: R) -> R:
        """Get exponent of Relation.

        Args:
            self (R): instance of Relation

        Returns:
            R: Relation where new y is exponent of old y.
        """
        return type(self)(self.x.copy(), np.exp(self.y))

    def diff(self: R) -> R:
        """Differentiation of 'Relation'.

        Args:
            self (R): instance of Relation

        Returns:
            R: result of differentiation.
        """
        result = default_methods.differentiate(self)
        return type(self)(result)

    def integrate(self: R) -> R:
        """Integration of `Relation`.

        Args:
            self (R): instance of Relation

        Returns:
            R: result of cumulative integration.
        """
        result = default_methods.integrate(self)
        return type(self)(result)

    def interpolate_extrapolate(
        self: R, new_x: Union[R, 'axis.Axis', ArrayLike]
    ) -> R:
        """Interpolates and extrapolates an existing relation using new array
        x of the represented Axis instance.

        Args:
            self (R): instance of Relation
            new_x (Axis): new x array axis

        Returns:
            R: new instance of Relation
        """
        if isinstance(new_x, Relation):
            new_x = new_x.x.copy()
        elif isinstance(new_x, axis.Axis):
            new_x = new_x.copy()
        else:
            new_x = axis.Axis.get_from_array(new_x)

        new_y = default_methods.interpolate_extrapolate(
            self.x.array.copy(), self.y.copy()
        )(new_x)
        return type(self)(new_x, new_y)

    def shift(self: R, x_shift: RealNumber = 0) -> R:
        """Shifting of relation on the x-axis.

        Args:
            self (R): instance of Relation
            x_shift (Number, optional): Number of displacement on the x-axis.
            Defaults to 0.

        Returns:
            R: new instance of Relation
        """
        new_x = self.x.copy()
        new_x.start = new_x.start + x_shift
        return type(self)(new_x, self.y)

    @staticmethod
    def equalize(r1: R, r2: R2) -> Tuple[R, R2]:
        """Bringing two Relation objects with different x-axes to one common one.

        When converting, interpolation and extrapolation are used.

        Args:
            r1 (R): first instance of Relation
            r2 (R2): second instance of Relation

        Returns:
            Tuple[R, R2]: tuple of new Relation instances with common axis.
        """
        if r1.x == r2.x:
            return deepcopy(r1), deepcopy(r2)

        new_x = axis.Axis.get_common_axis(r1.x, r2.x)
        r1 = r1.interpolate_extrapolate(new_x)
        r2 = r2.interpolate_extrapolate(new_x)

        return r1, r2

    @classmethod
    def correlate(cls: Type[R], r1: 'Relation', r2: 'Relation') -> R:
        """Correlation of two Relations.

        Args:
            cls (Type[R]): class of Relation
            r1 (Relation): first Relation.
            r2 (Relation): second Relation.

        Raises:
            TypeFuncError: raise exception
                if we try correlate with unexpected types.

        Returns:
            R: new instance of Relation
        """

        if isinstance(r1, Relation) and isinstance(r2, Relation):
            result = default_methods.correlate(cls, r1, r2)
            return cls(result)
        else:
            raise TypeFuncError('Correlation', type(r1), type(r2))

    @classmethod
    def convolve(cls: Type[R], r1: 'Relation', r2: 'Relation') -> R:
        """Convolution of two Relations.

        Args:
            cls (Type[R]): class of Relation
            r1 (Relation): first Relation.
            r2 (Relation): second Relation.

        Raises:
            TypeFuncError: raise exception
                if we try correlate with unexpected types.

        Returns:
            R: new instance of Relation
        """
        if isinstance(r1, Relation) and isinstance(r2, Relation):
            result = default_methods.convolve(cls, r1, r2)
            return cls(result)
        else:
            raise TypeFuncError('Convolution', type(r1), type(r2))

    @staticmethod
    def math_operation(
        a: 'Relation',
        b: Union['Relation', Number],
        name_operation: MathOperation,
    ) -> Tuple['axis.Axis', np.ndarray]:
        logging.debug(f'Type of a: {type(a)}')
        logging.debug(f'Type of b: {type(b)}')

        if isinstance(b, RelationProtocol):
            r1, r2 = Relation.equalize(a, b)
            return r1.x.copy(), default_methods.math_operation(
                r1.y.copy(), r2.y.copy(), name_operation
            )
        else:
            return a.x.copy(), default_methods.math_operation(
                a.y.copy(), b, name_operation
            )

    def __add__(self: R, other: Union['Relation', Number]) -> R:
        return type(self)(*self.math_operation(self, other, MathOperation.ADD))

    def __radd__(self: R, other: Union['Relation', Number]) -> R:
        return type(self)(
            *self.math_operation(self, other, MathOperation.RADD)
        )

    def __sub__(self: R, other: Union['Relation', Number]) -> R:
        return type(self)(*self.math_operation(self, other, MathOperation.SUB))

    def __rsub__(self: R, other: Union['Relation', Number]) -> R:
        return type(self)(
            *self.math_operation(self, other, MathOperation.RSUB)
        )

    def __mul__(self: R, other: Union['Relation', Number]) -> R:
        return type(self)(*self.math_operation(self, other, MathOperation.MUL))

    def __rmul__(self: R, other: Union['Relation', Number]) -> R:
        return type(self)(
            *self.math_operation(self, other, MathOperation.RMUL)
        )

    def __truediv__(self: R, other: Union['Relation', Number]) -> R:
        return type(self)(
            *self.math_operation(self, other, MathOperation.TRUEDIV)
        )

    def __rtruediv__(self: R, other: Union['Relation', Number]) -> R:
        return type(self)(
            *self.math_operation(self, other, MathOperation.RTRUEDIV)
        )

    def __pow__(self: R, other: Union['Relation', Number]) -> R:
        return type(self)(*self.math_operation(self, other, MathOperation.POW))

    def __rpow__(self: R, other: Union['Relation', Number]) -> R:
        return type(self)(
            *self.math_operation(self, other, MathOperation.RPOW)
        )

    def __iadd__(self: R, other: Union['Relation', Number]) -> R:
        return self.__add__(other)

    def __isub__(self: R, other: Union['Relation', Number]) -> R:
        return self.__sub__(other)

    def __imul__(self: R, other: Union['Relation', Number]) -> R:
        return self.__mul__(other)

    def __idiv__(self: R, other: Union['Relation', Number]) -> R:
        return self.__truediv__(other)

    def __ipow__(self: R, other: Union['Relation', Number]) -> R:
        return self.__pow__(other)

    def __len__(self) -> int:
        return self._x.size

    def __getitem__(
        self: R, select_data: Union[Number, slice]
    ) -> Union[Tuple[Number, Number], R]:
        """Select data from Relation

        if item is Number then function return tuple of two numbers.
        The first number is number near to select data.
        Second number is number represent of relation to selected data.

        if select data is slice then function return Relation that
        equal Relation if we call select_data function of instance.

        Args:
            self (R): instance of Relation
            item (Union[float, slice]): selected data is number or slice

        Returns:
            Union[Tuple[Num, Num], R]: two number or instance of relation.
        """

        if isinstance(select_data, (float, int, complex)):
            array = self.array
            idx = (np.abs(array - select_data)).argmin()
            return array[idx], self.y[idx]

        if isinstance(select_data, slice):
            return self.select_data(select_data.start, select_data.stop)

    def __str__(self) -> str:
        return f'y: {self.y}\nx: {str(self.x)}'
