"""This is where default function are defined."""
from typing import TYPE_CHECKING, Callable, Optional, Type, TypeVar, Union

import numpy as np
import scipy
from packaging import version
from scipy.interpolate import interp1d


from .help_types import X, Y, ArrayLike, RealNumber
from .core import MathOperation
from .help_types import Number
from .exc import TypeFuncError
from signal_design import axis, relation, signal, spectrum

RelationT = TypeVar("RelationT", bound="relation.Relation")

if version.parse(scipy.__version__) < version.parse('1.6.0'):
    from scipy.integrate import cumtrapz, quad, trapz

    integration = trapz
    cumulative_integration = cumtrapz
    quad_integrate_function = quad
else:
    from scipy.integrate import (
        cumulative_trapezoid,
        quad,
        trapezoid,
    )

    integration = trapezoid
    cumulative_integration = cumulative_trapezoid
    quad_integrate_function = quad

if TYPE_CHECKING:
    Axis = axis.Axis
    """Axis of `x`."""

    Time = axis.Axis
    """Axis of time."""

    Frequency = axis.Axis
    """Axis of frequency."""


def get_using_end(
    start: RealNumber,
    end: RealNumber,
    sample: RealNumber,
    is_correct_end: bool = True,
) -> 'Axis':
    """Create instance of Axis using start, end and sample params of axis.

    Args:
        start (RealNumber): start position of axis.
        end (RealNumber): end position of axis.
        sample (RealNumber): sample of axis.
        is_correct_end (bool): Default True. Checking the correctness of
            the end of the axis. If value is False, no end will be set
            for the instance.

    Returns:
        Axis: new instance of Axis.
    """
    size = get_size(start, end, sample)
    if is_correct_end:
        return axis.Axis(size=size, sample=sample, start=start, end=end)
    return axis.Axis(size=size, sample=sample, start=start)


def get_size(start: RealNumber, end: RealNumber, sample: RealNumber) -> int:
    """Calculate size of axis using start, end and sample.

    Args:
        start (RealNumber): start position of axis.
        end (RealNumber): end position of axis.
        sample (RealNumber): sample of axis.

    Returns:
        int: size of axis.
    """

    result = round(abs((end - start) / sample)) + 1

    return result


def get_array(axis_data: 'axis.Axis') -> np.ndarray:
    """Create array of numpy from Axis, using, start, end and size of Axis.

    Args:
        axis_data (Axis): instance of Axis

    Returns:
        numpy.ndarray: numpy array of axis.
    """

    result = np.linspace(axis_data.start, axis_data.end, axis_data.size)

    return result


def get_axis_from_array(
    x: ArrayLike, sample: Optional[RealNumber] = None
) -> 'Axis':
    """Create instance of Axis from some array of numbers.

    Args:
        x (ArrayLike): Input array like of numbers.
        sample (Optional[RealNumber]): Default None. Sample of array.
            If sample is None, it well be calculated by function.

    Returns:
        Axis: new instance of Axis.
    """
    np_x = np.array(x)
    if sample is None:
        sample = get_actual_sample(np_x)

    return axis.Axis(start=np_x[0], sample=sample, size=np_x.size)


def get_actual_sample(x: np.ndarray) -> RealNumber:
    """Calculate actual sample. Use for self-test. Problem with floating point
    in Python (https://docs.python.org/3/tutorial/floatingpoint.html).

    Args:
        x (numpy.ndarray): array of numbers.

    Returns:
        RealNumber: an actual sample
    """
    diff = np.min(np.diff(x))
    values, counts = np.unique(diff, return_counts=True)
    common_sample = values[np.argmax(counts)]
    return common_sample


def get_common_axis(
    axis1: 'Axis', axis2: 'Axis', is_correct_end: bool = False
) -> 'Axis':
    """Specifies the overall axis.

    Finds the general sample rate and beginning and end of sequence.
    A function by which to find the common sequence of numbers along
    the axis, obtained from two other sequences along the axis.

    Args:
        axis1 (Axis): first axis.
        axis2 (Axis): second axis.

    Returns:
        Axis: return common Axis for first and second axes.
    """
    dx1 = axis1.sample
    dx2 = axis2.sample

    dx = dx1 if dx1 <= dx2 else dx2
    x_start = axis1.start if axis1.start <= axis2.start else axis2.start
    x_end = axis1.end if axis1.end >= axis2.end else axis2.end
    return axis.Axis.get_using_end(
        start=x_start, end=x_end, sample=dx, is_correct_end=is_correct_end
    )


# ==============================================================================


def math_operation(
    y1: np.ndarray,
    y2: Union[np.ndarray, Number],
    name_operation: MathOperation,
) -> Y:
    """Math operations.

    Using numpy math operations.

    Args:
        y1 (numpy.ndarray): first sequence y.
        y2 (Union[numpyp.ndarray, Number]): second sequence y or other number
        name_operation (MathOperation): which mathematical operation (+, -,
            \\*, / and etc.)

    Raises:
        TypeFuncError: if operation can not be executed.

    Returns:
        Y: result of math operation.
    """
    try:
        y = y1.__getattribute__(name_operation.value)(y2)

    except Exception as e:
        raise TypeFuncError(
            name_operation.value.strip('_'), type(y1), type(y2)
        ) from e

    return y


def one_integrate(relation: RelationT) -> float:
    """Integration.

    Taking the integral on a segment. Return of the area under the graph.
    using scipy trapezoid integration.

    Args:
        relation (Relation): from will be calculated integral.

    Returns:
        float: result of integration.
    """
    x, y = relation.get_data()
    return integration(y, x)


def integrate(relation_data: RelationT) -> RelationT:
    """Integration.

    Integration across the entire function. Get the expected integrated
    array function.
    Using the :class:`scipy.integrate.cumtrapz` function.

    Args:
        relation (Relation): integrated function.

    Returns:
        Relation: result of integration of function.
    """
    array_axis = relation_data.x.copy()
    dx = array_axis.sample
    array_axis.start = array_axis.start + array_axis.sample
    array_axis.size = array_axis.size - 1
    return relation.Relation(
        array_axis, cumulative_integration(relation_data.y) * (dx)
    )


def differentiate(relation_data: RelationT) -> RelationT:
    """Differentiation.

    The function by which differentiation is performed.
    Using the `numpy.diff` function.

    Args:
        relation (Relation): function which will be differentiated.

    Returns:
        Relation: result of differentiation.
    """
    array_axis = relation_data.x.copy()
    dx = array_axis.sample
    array_axis.start = array_axis.start + array_axis.sample / 2
    array_axis.size = array_axis.size - 1
    return relation.Relation(array_axis, np.diff(relation_data.y) / (dx))


def interpolate_extrapolate(
    x: X, y: Y, bounds_error=False, fill_value=0.0
) -> Callable[['axis.Axis'], Y]:
    """Interpolation and extrapolation

    Using the `scipy.interpolate.interp1d` function.
    Returning function of interpolation.

    Args:
        x (numpy.ndarray): numbers array of axis. Samples can be not equal.

        y (numpy.ndarray): representation interpolated extrapolated functions
            as array.

        bounds_error (bool, optional): if False then do not raise error if new
            array behind of bound old array. Defaults to False.

        fill_value (float, optional): default fill value if other not expected.
            Defaults to 0.0.

    Returns:
        Callable[[X], Y]: Callable that get first new array of x and return
            interpolate-extrapolate result.
    """
    interpolate_extrapolate = interp1d(
        x, y, bounds_error=bounds_error, fill_value=fill_value
    )

    def wrapper(new_x: axis.Axis) -> Y:
        new_y = interpolate_extrapolate(new_x.array)
        return new_y

    return wrapper


def correlate(
    cls: Type[RelationT],
    r1: RelationT,
    r2: RelationT,
) -> RelationT:
    """Correlation.

    The function by which the correlation is performed.
    Using the `numpy.correlate` function.

    Args:
        cls (Type[Relation]): class to use equalization of two relations.
        r1 (Relation): first function y.
        r2 (Relation): second function y.

    Returns:
        Relation: result of correlation.
    """
    r1, r2 = cls.equalize(r1, r2)
    x_axis = axis.Axis(start=2*r1.start, sample=r1.sample,
                       size=r1.size * 2 - 1)
    return cls(x_axis, np.correlate(r1.y, r2.y, 'full'))


def convolve(
    cls: Type[RelationT],
    r1: RelationT,
    r2: RelationT,
) -> RelationT:
    """Convolution.

    The function by which the convolution is performed.
    Using the `numpy.convolve` function.

    Args:
        cls (Type[Relation]): class to use equalization of two arrays.
        r1 (Relation): first function y.
        r2 (Relation): second function y.

    Returns:
        Relation: result of convolution.
    """
    r1, r2 = cls.equalize(r1, r2)
    x_axis = axis.Axis(start=2*r1.start, sample=r1.sample,
                       size=r1.size * 2 - 1)
    return cls(x_axis, np.convolve(r1.y, r2.y, 'full'))


# ==============================================================================


def signal_shift(
    signal: 'signal.Signal', x_shift: RealNumber = 0
) -> 'signal.Signal':
    """Shifting of signal.

    Shift signal using Fourier transform.

    Args:
        signal: input shifting signal.
        x_shift: shift distance.

    Returns:
        Signal: shifted signal.
    """
    sp = signal.get_spectrum()
    shift = spectrum.Spectrum(
        sp.frequency,
        np.exp(-1j * sp.frequency.array * 2 * np.pi * x_shift),
    )
    return sp.add_phase(shift).get_signal(signal.time)


def signal2spectrum(
    relation_data: RelationT,
    frequency: Optional[Union['Frequency', int]]=None,
    is_start_zero=False,
    is_real_value_transform=True,
) -> 'spectrum.Spectrum':
    """Forward Fourier Transform.

    Function for converting a signal into a spectrum.
    Using the `numpy.fft.rfft` function.

    Args:
        relation_data (Relation): signal from which get spectrum.

        frequency (Axis, int, optional): Define frequency to calculate
            spectrum. Defaults to None.

        is_start_zero (bool, optional): Consider array started from zero time.
            Defaults to False.

    Returns:
        Relation: result transformation Signal to Spectrum.
    """
    new_time = relation_data.x.copy()
    amplitude = relation_data.y.copy()

    if is_start_zero:
        return _calculate_spectrum(
            new_time, 
            amplitude, 
            frequency, 
            is_real_value_transform
        )

    if new_time.start > 0.0:
        new_time.start = 0.0
        amplitude = np.append(
            np.zeros(new_time.size - amplitude.size), amplitude
        )

    elif new_time.end < 0.0:

        new_time.end = 0.0
        amplitude = np.append(
            amplitude, np.zeros(new_time.size - amplitude.size)
        )

    return _calculate_spectrum(
        new_time, 
        amplitude, 
        frequency, 
        is_real_value_transform
    )


def _calculate_spectrum(
    time: 'Time',
    amplitude: np.ndarray,
    frequency: Optional[Union[int, 'Frequency']] = None,
    is_real_value_transform: bool = True
) -> 'spectrum.Spectrum':

    if frequency is None:
        size = None
    elif isinstance(frequency, int):
        size = frequency
    else:
        size = frequency.size

    amplitude = np.append(
        amplitude[time.array >= 0.0], amplitude[time.array < 0.0]
    )

    if np.any(np.iscomplex(amplitude)) or not is_real_value_transform:
        spectrum_array = np.fft.fft(amplitude, size)

        if frequency is None or isinstance(frequency, int):
            np_frequency = np.fft.fftfreq(amplitude.size, d=time.sample)
            spectrum_array = spectrum_array[np_frequency.argsort()]
            np_frequency = np.sort(np_frequency)
            frequency = axis.Axis.get_from_array(np_frequency)
    else:
        spectrum_array = np.fft.rfft(amplitude, size)

        if frequency is None or isinstance(frequency, int):
            np_frequency = np.fft.rfftfreq(amplitude.size, d=time.sample)
            frequency = axis.Axis.get_from_array(np_frequency)
    
    return spectrum.Spectrum(frequency, spectrum_array)


def get_frequency_axis(
    time_size: int, 
    time_sample: float, 
    is_complex_data: bool = False
) -> 'Frequency':
    """Get frequency axis from size and sample of time.

    Function for getting a frequency axis using size and sample of time.
    If the data is complex, then the frequency axis will contain negative part.

    Args:
        time_size (int): size of time
        
        time_sample (float): sample of time
        
        is_complex_data (bool): If the data is complex, then the frequency
            axis will contain a negative part. If not, then vice versa.
            Defaults to False.

    Return:
        Axis: frequency axis.
    
    """
    if is_complex_data:
        np_frequency = np.fft.fftfreq(time_size, d=time_sample)
        np_frequency = np.sort(np_frequency)
    else:
        np_frequency = np.fft.rfftfreq(time_size, d=time_sample)

    frequency = axis.Axis.get_from_array(np_frequency)

    return frequency
        

def spectrum2signal(
    relation_data: relation.Relation,
    time: Optional[Union['Time', int]] = None,
    time_start: Union[float, None] = None,
) -> 'signal.Signal':
    """Inverse Fourier Transform.

    Function for converting a spectrum into a signal.
    Using `numpy.ifft` function.

    Args:
        relation (Relation): spectrum of signal.

        time (Axis, int, optional): Define time to calculate
            signal. Defaults to None.

        time_start (float, optional): default fft convert to 0. time. Maybe you
            want another start of time. Defaults to None.

    Returns:
        Signal: result transformation Spectrum to Signal.
    """

    spectrum = relation_data.y.copy()
    frequency = relation_data.x.copy()

    if time is None:
        size = None
    elif isinstance(time, int):
        size = time
    else:
        size = time.size

    if frequency.start < 0.:
        amplitude = np.fft.ifft(spectrum, size)
    else:
        amplitude = np.fft.irfft(spectrum, size)
        

    if time is None or isinstance(time, int):

        if size is None:
            size = amplitude.size

        time = get_time_axis(frequency, size, time_start)

    amplitude = np.append(
        amplitude[time.array >= 0.0], amplitude[time.array < 0.0]
    )

    return signal.Signal(time, amplitude)

def get_time_axis(
    frequency: 'Frequency', 
    size: Optional[int] = None, 
    time_start: Optional[float] = None
) -> 'Time':
    """Get time axis from frequency axis and desired size of time axis.

    Function for getting a time axis using frequency axis and desired size.

    Args:

        frequency (Axis): frequency axis. 
    
        size (int, optional): desired size of time axis. Defaults to None.
        
        time_start (float, optional): default fft convert to 0. time. Maybe you
            want another start of time. Defaults to None.
        
    Return:
        Axis: time axis.
    
    """

    if size is None:
        size = frequency.size

    dt = 1 / (2 * (frequency.end - frequency.start))

    if time_start is None:
        time = axis.Axis(start=0.0, sample=dt, size=size, end= (size-1) * dt)
    else:
        time = axis.Axis(
            start=time_start,
            sample=dt,
            size=size,
            end=time_start + (size - 1) * dt,
        )

    return time    


def integrate_function(
    function: Callable[[X], Y], x: 'Axis'
) -> RelationT:
    """Integration function y(x).

    The function by which the integration function is performed. Integration across
    the entire function. Get the expected integrated array function.
    Integration of function, using `scipy.integrate.quad` function.

    Args:
        function (Callable[[X], Y]): function is describing
            changes frequency from time.

        x (Axis): x axis.

    Returns:
        Relation: result of integration function.
    """
    integrate_function = np.vectorize(
        lambda x: quad_integrate_function(function, x.start, x)
    )
    result = np.append([0.0], integrate_function(x.array[1:]))
    return relation.Relation(x, result)
