from typing import Callable, Optional, Type, TypeVar, Union

import numpy as np

from . import spectrum
from .axis import Axis

from .core import RelationProtocol
from .exc import ConvertingError
from .relation import Relation
from .help_types import ArrayLike, Number, RealNumber
from . import default_functions as default_functions

S = TypeVar('S', bound='Signal')
"""Instance of `Signal`."""

SSPR = Union['spectrum.Spectrum', 'Signal', Relation]
"""Instance of `Signal` or `Spectrum` or :class:`signal_design.relation.Relation`."""

SRN = Union['Signal', Relation, Number]
"""Instance of `Signal` or :class:`signal_design.relation.Relation` or `Number`."""

SSPRN = Union['spectrum.Spectrum', 'Signal', Relation, Number]
"""Instance of `Signal` or `Spectrum` or :class:`signal_design.relation.Relation` or `Number`."""


def input2signal_operation(
    func: Callable[[S, SRN], S]
) -> Callable[[S, SSPRN], S]:
    def wrapper(_, input: SSPRN) -> S:
        conversion = _input2signal_operation(input)
        return func(_, conversion)

    return wrapper


def _input2signal_operation(input: SSPRN) -> SRN:
    return (
        input.get_signal() if isinstance(input, spectrum.Spectrum) else input
    )


def input2signal(
    func: Callable[[Type[S], 'Signal', 'Signal'], S]
) -> Callable[[Type[S], SSPR, SSPR], 'Signal']:
    def wrapper(_, input1: SSPR, input2: SSPR) -> 'Signal':
        converted_input1 = _input2signal(input1)
        converted_input2 = _input2signal(input2)
        return func(_, converted_input1, converted_input2)

    return wrapper


def _input2signal(input: SSPR) -> 'Signal':
    if isinstance(input, spectrum.Spectrum):
        return input.get_signal()
    elif isinstance(input, Signal):
        return input
    elif isinstance(input, Relation):
        return Signal(input)
    else:
        raise ConvertingError(type(input), Signal)


class Signal(Relation):
    """Class describing some kind of signal.

    The `Signal` class inherits the :class:`signal_design.relation.Relation` class.

    Each signal can be converted into a :class:`signal_design.spectrum.Spectrum` using method `get_spectrum`.
    To convert the signal into a spectrum, the method defined in the default_functions module
    is used (default_functions.signal2spectrum). Current method can be
    overridden by own.

    When performing arithmetic operations on instances of the spectrum.Spectrum class,
    an instance of the `Signal` class will be extracted from
    the :class:`signal_design.spectrum.Spectrum` instance, and arithmetic operations will be performed
    on this instance. An instance of :class:`signal_design.relation.Relation` class will be converted into
    the instance of `Signal` class.
    """

    def __init__(
        self,
        time: Union[RelationProtocol, Axis, ArrayLike],
        amplitude: Optional[ArrayLike] = None,
        spectrum: Optional['spectrum.Spectrum'] = None,
    ) -> None:
        """Initialization of instance of `Signal`.

        Args:
            time (Union[RelationProtocol, Axis, ArrayLike]): An instance
                of Relation class or inherited from it, or ArrayLike, or array_like
                object containing numbers real.

            amplitude (ArrayLike, optional): None or array_like object
                containing numbers (real or complex). Defaults to None.
        """

        super().__init__(time, amplitude)
        self._spectrum = spectrum

    @property
    def time(self) -> Axis:
        """Time array axis.

        Equal to property `x`.

        Returns:
            Axis: time array axis.
        """
        return self.x

    @property
    def amplitude(self) -> np.ndarray:
        """Amplitude array.

        Equal to property 'y'

        Returns:
            np.ndarray: amplitude array.
        """
        return self.y

    def get_spectrum(
        self,
        frequency: Optional[Union[Axis, int]] = None,
        is_start_zero=False,
        is_real_value_transform=True,
    ) -> 'spectrum.Spectrum':
        """Get spectrum from signal.

        Args:
            frequency (Axis, int, optional): Define frequency to calculate
            spectrum. Defaults to None.

            is_start_zero (bool, optional): If True then the signal will be
                shifted to zero. Defaults to `False`.

        Returns:
            spectrum.Spectrum: instance of :class:`signal_design.spectrum.Spectrum` described this `Signal`.
        """

        if self._spectrum is None or frequency:

            spectrum_result = default_functions.signal2spectrum(
                self, frequency, is_start_zero, is_real_value_transform
            )
            self._spectrum = spectrum.Spectrum(spectrum_result, signal=self)

        return self._spectrum

    def get_amplitude_spectrum(
        self, frequency: Optional[Union[Axis, int]] = None, is_start_zero=False
    ) -> Relation:
        """Extract amplitude spectrum from :class:`signal_design.spectrum.Spectrum`.

        Method `get_spectrum` is used to get instance of :class:`signal_design.spectrum.Spectrum`.
        The amplitude spectrum is calculated from it using `get_amp_spectrum`
        method.

        Args:
            frequency (Axis, int, optional): Define frequency to calculate
                spectrum. Defaults to None.

            is_start_zero (bool, optional): If True then the signal will be
                shifted to zero. Defaults to `False`.

        Returns:
            Relation: amplitude spectrum expected Relation instance.
        """
        return self.get_spectrum(
            frequency, is_start_zero
        ).get_amplitude_spectrum()

    def get_phase_spectrum(
        self, frequency: Optional[Union[Axis, int]] = None, is_start_zero=False
    ) -> Relation:
        """Extract amplitude spectrum from :class:`signal_design.spectrum.Spectrum`.

        Method `get_spectrum` is used to get instance of :class:`signal_design.spectrum.Spectrum`.
        The amplitude spectrum is calculated from it using `get_amp_spectrum`
        method.

        Args:
            frequency (Axis, int, optional): Define frequency to calculate
            spectrum. Defaults to None.

            is_start_zero (bool, optional): If True then the signal will be
                shifted to zero. Defaults to `False`.

        Returns:
            Relation: amplitude spectrum expected Relation instance.
        """
        return self.get_spectrum(frequency, is_start_zero).get_phase_spectrum()

    def shift(self: S, x_shift: RealNumber = 0) -> S:
        """Shifting of signal.

        Shift signal using Fourier transform.

        Args:
            x_shift: shift distance.

        Returns:
            Signal: shifted signal.
        """
        return type(self)(default_functions.signal_shift(self, x_shift))

    def get_reverse_signal(
        self: S,
        percent: Union[float, int] = 5.0,
        subtract_phase: bool = True,
        frequency_start: Optional[float] = None,
        frequency_end: Optional[float] = None,
    ) -> S:
        """Calculate reversed signal.

        Args:
            self (S): instance of Signal.

            percent (Union[float, int], optional): level of added white
                noise in percent. Defaults to 5.0.

            subtract_phase (bool, optional): If True performs phase subtraction,
                If False succeeds, add the phase. Defaults to True.

            frequency_start (float, optional): The start frequency.
                Defaults to None.

            frequency_end (float, optional): The end frequency.
                Defaults to None.

        Returns:
            S: instance of Signal.
        """

        signal = (
            self.get_spectrum()
            .get_reverse_filter(
                percent, subtract_phase, frequency_start, frequency_end
            )
            .get_signal(self.time)
        )

        return type(self)(signal)

    def add_phase(self: S, other: SSPR) -> S:
        """Add phase to signal.

        Args:
            self (S): instance of `Signal`.

            other (SSPR): Extracting the :class:`signal_design.spectrum.Spectrum` from the object and adding
                the phase :class:`signal_design.spectrum.Spectrum` to the `Signal`.

        Returns:
            S: new instance of `Signal`.
        """
        return type(self)(
            self.get_spectrum().add_phase(other).get_signal(self.time)
        )

    def sub_phase(self: S, other: SSPR) -> S:
        """Subtract phase from signal.

        Args:
            self (S): instance of Signal

            other (SSPR): Extracting the spectrum from the object and subtract
                the phase spectrum from the signal.

        Returns:
            S: new instance of Signal.
        """
        return type(self)(
            self.get_spectrum().sub_phase(other).get_signal(self.time)
        )

    @staticmethod
    def get_time_from_frequency(
        frequency: Axis, 
        size: Optional[int] = None, 
        time_start: Optional[float] = None
    ) -> Axis:
        """Get time axis from frequency axis and desired size of time axis.

        Method for getting a time axis using frequency axis and desired size.
        Also setting with desired time start.

        Args:

            frequency (Axis): frequency axis. 
        
            size (int, optional): desired size of time axis. Defaults to None.
            
            time_start (float, optional): default fft convert to 0. time. Maybe 
                you want another start of time. Defaults to None.
            
        Return:
            Axis: time axis.
        
        """

        return default_functions.get_time_axis(frequency, size, time_start)

    @classmethod
    @input2signal
    def convolve(cls: Type[S], s1: S, s2: S) -> S:
        """Convolution of two instances of :class:`signal_design.relation.Relation` and return new instance of
        `Signal`. Instances of :class:`signal_design.spectrum.Spectrum` will be converted to `Signal`

        Args:
            cls (Type[S]): `Signal` class.
            r1 (SSPR): instance of :class:`signal_design.relation.Relation` or subclass of `Relation`
            r2 (SSPR): instance of :class:`signal_design.relation.Relation` or subclass of `Relation`

        Returns:
            S: new instance of Signal.
        """
        return cls(super().convolve(s1, s2))

    @classmethod
    @input2signal
    def correlate(cls: Type[S], r1: S, r2: S) -> S:
        """Correlation of two instances of :class:`signal_design.relation.Relation` and return new instance of
        `Signal`. Instance of :class:`signal_design.spectrum.Spectrum` will be converted to `Signal`

        Args:
            cls (Type[S]): `Signal` class.
            r1 (SSPR): instance of :class:`signal_design.relation.Relation` or subclass of `Relation`
            r2 (SSPR): instance of :class:`signal_design.relation.Relation` or subclass of `Relation`

        Returns:
            S: new instance of Signal.
        """
        return cls(super().correlate(r1, r2))

    @input2signal_operation
    def __add__(self: S, a: SRN) -> S:
        return super().__add__(a)

    @input2signal_operation
    def __sub__(self: S, a: SRN) -> S:
        return super().__sub__(a)

    @input2signal_operation
    def __mul__(self: S, a: SRN) -> S:
        return super().__mul__(a)

    @input2signal_operation
    def __truediv__(self: S, a: SRN) -> S:
        return super().__truediv__(a)

    @input2signal_operation
    def __pow__(self: S, a: SRN) -> S:
        return super().__pow__(a)
