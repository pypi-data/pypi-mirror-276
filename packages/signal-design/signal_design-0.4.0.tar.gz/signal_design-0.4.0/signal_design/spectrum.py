from typing import Callable, Optional, Type, TypeVar, Union

import numpy as np

from . import signal
from .axis import Axis

from .core import RelationProtocol
from .exc import ConvertingError
from .relation import Relation
from .help_types import ArrayLike, Number
from . import default_functions as default_functions

SP = TypeVar('SP', bound='Spectrum')
"""Instance of `Spectrum`"""

SSPR = Union['Spectrum', 'signal.Signal', Relation]
"""Instance of Spectrum or Signal or Relation"""

SPRN = Union['Spectrum', Relation, Number]
"""Instance of Spectrum or Signal or Relation or Number"""

SSPRN = Union['Spectrum', 'signal.Signal', Relation, Number]
"""Instance of Spectrum or Signal or Relation or Number"""


def input2spectrum_operation(
    func: Callable[[SP, SPRN], SP]
) -> Callable[[SP, SSPRN], SP]:
    def wrapper(_, input: SSPRN) -> SP:
        conversion = _input2spectrum_operation(input)
        return func(_, conversion)

    return wrapper


def _input2spectrum_operation(input: SSPRN) -> SPRN:
    return input.get_spectrum() if isinstance(input, signal.Signal) else input


def input2spectrum(
    func: Callable[[Type[SP], 'Spectrum', 'Spectrum'], SP]
) -> Callable[[Type[SP], SSPR, SSPR], SP]:
    def wrapper(_, input1: SSPR, input2: SSPR) -> SP:
        converted_input1 = _input2spectrum(input1)
        converted_input2 = _input2spectrum(input2)
        return func(_, converted_input1, converted_input2)

    return wrapper


def _input2spectrum(input: SSPR) -> 'Spectrum':

    if isinstance(input, Spectrum):
        return input
    elif isinstance(input, signal.Signal):
        return input.get_spectrum()

    elif isinstance(input, Relation):
        return Spectrum(input)
    else:
        raise ConvertingError(type(input), Spectrum)


class Spectrum(Relation):
    """A class that describes the spectrum of a signal.

    The `Spectrum` class derived from the :class:`signal_design.relation.Relation` class.

    Each 'Spectrum' can be converted into a :class:`signal_design.signal.Signal` using method `get_spectrum`
    To convert the `Spectrum` into a :class:`signal_design.signal.Signal`, the method defined in the
    default_functions module is used. (:class:`signal_design.default_functions.spectrum2signal`).
    Current method can be overridden by own.

    When performing arithmetic operations on instances of the
    :class:`signal_design.signal.Signal` class,
    an instance of the `Spectrum` class will be extracted from
    the :class:`signal_design.signal.Signal` instance, and arithmetic
    operations will be performed
    on this instance. An instance of :class:`signal_design.relation.Relation`
    class will be converted into
    the instance of `Spectrum` class.

    """

    def __init__(
        self,
        frequency: Union[RelationProtocol, Axis, ArrayLike],
        spectrum_amplitude: Optional[ArrayLike] = None,
        signal: Optional['signal.Signal'] = None,
    ) -> None:
        """Initialization of instance of `Spectrum`.

        Args:
            frequency (Union[RelationProtocol, Axis, ArrayLike]):
                An instance of :class:`signal_design.relation.Relation` class or inherited from it,
                or `Axis` instance, or array_like object containing
                numbers (real).

            spectrum_amplitude (ArrayLike, optional):
                None or array_like object containing numbers (real or complex).
                Defaults to None.

        """
        super().__init__(frequency, spectrum_amplitude)
        self._signal = signal

    @property
    def frequency(self) -> Axis:
        """Frequency array axis.

        Equal to property `x`.
        Returns:
            Axis: frequency array axis.
        """
        return self.x

    @property
    def amplitude(self) -> np.ndarray:
        """Spectrum amplitude array.

        Equal to property `y`.
        Returns:
            numpy.ndarray: spectrum amplitude array.
        """
        return self.y

    def get_signal(
        self,
        time: Optional[Union[Axis, int]] = None,
        start_time: Optional[float] = None,
    ) -> 'signal.Signal':
        """Get signal from spectrum.

        Compute the signal from the spectrum.

        Args:
            time (Axis, int, optional): Define time to calculate
                signal. Defaults to None.

            start_time (float, optional): If True then the signal will be
                shifted to zero. Defaults to `False`.

        Returns:
            signal.Signal: instance of :class:`signal_design.signal.Signal` described this `Spectrum`.
        """

        if self._signal is None or time:

            signal_result = default_functions.spectrum2signal(
                self, time, start_time
            )
            self._signal = signal.Signal(signal_result, spectrum=self)

        return self._signal

    def get_amplitude_spectrum(self: 'Spectrum') -> Relation:
        """Get amplitude spectrum.

        Calculate the relationship between the frequency and the absolute
        value of the spectrum amplitude.

        Args:
            self (SP): instance of Spectrum.

        Returns:
            Relation: new instance of Relation.
        """
        return Relation(self.x.copy(), np.abs(self.y))

    def get_phase_spectrum(self: 'Spectrum') -> Relation:
        """Get phase spectrum.

        Calculate the relationship between frequency and phase of the spectrum.

        Args:
            self (SP): instance of Spectrum.

        Returns:
            Relation: new instance of Relation.
        """

        return Relation(self.x.copy(), np.unwrap(np.angle(self.y)))

    def get_reverse_filter(
        self: SP,
        percent: Union[float, int] = 5.0,
        subtract_phase=True,
        frequency_start: Optional[float] = None,
        frequency_end: Optional[float] = None,
    ) -> SP:
        """Calculate filter of reversed signal.

        Args:
            self (SP): instance of Spectrum.

            percent (Union[float, int], optional): level of added white noise
                in percent. Defaults to 5.0.

            subtract_phase (bool, optional): If True performs phase subtraction.
                If False succeeds, add the phase. Defaults to True.

            frequency_start (float, optional): The start frequency. Defaults to None.
            frequency_end (float, optional): The end frequency. Defaults to None.

        Returns:
            SP: new instance of Spectrum.
        """

        spectrum = self.select_data(frequency_start, frequency_end)
        abs_spectrum = spectrum.get_amplitude_spectrum()
        abs_spectrum = abs_spectrum + abs_spectrum.max() * percent / 100
        reversed_abs_spectrum = 1 / abs_spectrum

        if subtract_phase:
            phase_spectrum = -1 * spectrum.get_phase_spectrum()
        else:
            phase_spectrum = 1 * spectrum.get_phase_spectrum()

        result_spectrum = type(self).get_from_amplitude_phase(
            reversed_abs_spectrum, phase_spectrum
        )
        return result_spectrum

    def add_phase(self: SP, other: SSPR) -> SP:
        """Add phase to spectrum.

        Args:
            self (SP): instance of `Spectrum`

            other (SSPR): Extracting the `Spectrum` from the object and adding
                the phase `Spectrum` to the `Spectrum`.

        Returns:
            `SP`: new instance of `Spectrum`.
        """

        sp_other = _input2spectrum(other)
        return type(self).get_from_amplitude_phase(
            self.get_amplitude_spectrum(),
            self.get_phase_spectrum() + sp_other.get_phase_spectrum(),
        )

    def sub_phase(self: SP, other: SSPR) -> SP:
        """Subtract phase from spectrum.

        Args:
            self (SP): instance of `Spectrum`

            other (SSPR): Extracting the `Spectrum` from the object and subtract
                the phase `Spectrum` from the `Spectrum`.

        Returns:
            `SP`: new instance of `Spectrum`.
        """
        sp_other = _input2spectrum(other)
        return type(self).get_from_amplitude_phase(
            self.get_amplitude_spectrum(),
            self.get_phase_spectrum() - sp_other.get_phase_spectrum(),
        )

    @staticmethod
    def get_frequency_axis_from_time(
        time: Axis, 
        is_complex_data: bool = False
    ) -> Axis:
        """Get frequency axis from axis of time.

        Method for getting a frequency axis using time axis.
        If the data is complex, then the frequency axis will contain negative 
        part.

        Args:
            time (Axis): axis of time.

            is_complex_data (bool): If the data is complex, then the frequency
                axis will contain a negative part. If not, then vice versa.
                Defaults to False.

        Return:
            Axis: frequency axis.
        
        """
        return default_functions.get_frequency_axis(
            time.size,
            time.sample,
            is_complex_data,
        )

    @classmethod
    def get_from_amplitude_phase(
        cls: Type[SP], amplitude_spectrum: Relation, phase_spectrum: Relation
    ) -> SP:
        """Calculate of the spectrum from the amplitude and phase spectrum.

        The spectrum is calculated through the amplitude and phase spectrum
        using the formula abs*exp(1j*phase).

        Args:
            cls (Type[SP]): Spectrum class.
            amplitude_spectrum (Relation): Amplitude spectrum is instance of :class:`signal_design.relation.Relation`.
            phase_spectrum (Relation): Phase spectrum is instance of :class:`signal_design.relation.Relation`.

        Returns:
            SP: new instance of `Spectrum`
        """

        return cls(amplitude_spectrum * ((1.0j * phase_spectrum).exp()))

    @classmethod
    @input2spectrum
    def convolve(cls: Type[SP], sp1: 'Spectrum', sp2: 'Spectrum') -> SP:
        """Convolution of two instances of :class:`signal_design.relation.Relation` and return new instance of
        `Spectrum`. Instances of :class:`signal_design.signal.Signal` will be converted to `Spectrum`

        Args:
            cls (Type[SP]): `Spectrum` class.
            r1 (SSPR): instance of :class:`signal_design.relation.Relation` or subclass of `Relation`
            r2 (SSPR): instance of :class:`signal_design.relation.Relation` or subclass of `Relation`

        Returns:
            S: new instance of `Spectrum`.
        """
        return super().convolve(sp1, sp2)

    @classmethod
    @input2spectrum
    def correlate(cls: Type[SP], sp1: 'Spectrum', sp2: 'Spectrum') -> SP:
        """Correlation of two instances of :class:`signal_design.relation.Relation` and return new instance of
        `Spectrum`. Instances of :class:`signal_design.signal.Signal` will be converted to `Spectrum`

        Args:
            cls (Type[Spectrum]): `Spectrum` class.
            r1 (SSPR): instance of :class:`signal_design.relation.Relation` or subclass of `Relation`
            r2 (SSPR): instance of :class:`signal_design.relation.Relation` or subclass of `Relation`

        Returns:
            S: new instance of `Spectrum`.
        """
        return super().correlate(sp1, sp2)

    @input2spectrum_operation
    def __add__(self: SP, a: SPRN) -> SP:
        return super().__add__(a)

    @input2spectrum_operation
    def __sub__(self: SP, a: SPRN) -> SP:
        return super().__sub__(a)

    @input2spectrum_operation
    def __mul__(self: SP, a: SPRN) -> SP:
        return super().__mul__(a)

    @input2spectrum_operation
    def __truediv__(self: SP, a: SPRN) -> SP:
        return super().__truediv__(a)

    @input2spectrum_operation
    def __pow__(self: SP, a: SPRN) -> SP:
        return super().__pow__(a)
