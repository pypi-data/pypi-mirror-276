import pandas as pd
import numpy as np
from pandas.core.nanops import nanmean as pd_nanmean
from pandas.tseries import offsets
from pandas.tseries.frequencies import to_offset
from scipy import signal
from typing import Union


class PandasWrapper:
    """
    Wrap array_like using the index from the original input, if pandas

    Parameters
    ----------
    pandas_obj : {Series, DataFrame}
        Object to extract the index from for wrapping

    Notes
    -----
    Raises if ``orig`` is a pandas type but obj and and ``orig`` have
    different numbers of elements in axis 0. Also raises if the ndim of obj
    is larger than 2.
    """

    def __init__(self, pandas_obj):
        self._pandas_obj = pandas_obj
        self._is_pandas = isinstance(pandas_obj, (pd.Series, pd.DataFrame))

    def wrap(self, obj, columns=None, append=None, trim_start=0, trim_end=0):
        """
        Parameters
        ----------
        obj : {array_like}
            The value to wrap like to a pandas Series or DataFrame.
        columns : {str, list[str]}
            Column names or series name, if obj is 1d.
        append : str
            String to append to the columns to create a new column name.
        trim_start : int
            The number of observations to drop from the start of the index, so
            that the index applied is index[trim_start:].
        trim_end : int
            The number of observations to drop from the end of the index , so
            that the index applied is index[:nobs - trim_end].

        Returns
        -------
        array_like
            A pandas Series or DataFrame, depending on the shape of obj.
        """
        obj = np.asarray(obj)
        if not self._is_pandas:
            return obj

        if obj.shape[0] + trim_start + trim_end != self._pandas_obj.shape[0]:
            raise ValueError(
                "obj must have the same number of elements in "
                "axis 0 as orig"
            )
        index = self._pandas_obj.index
        index = index[trim_start: index.shape[0] - trim_end]
        if obj.ndim == 1:
            if columns is None:
                name = getattr(self._pandas_obj, "name", None)
            elif isinstance(columns, str):
                name = columns
            else:
                name = columns[0]
            if append is not None:
                name = append if name is None else f"{name}_{append}"

            return pd.Series(obj, name=name, index=index)
        elif obj.ndim == 2:
            if columns is None:
                columns = getattr(self._pandas_obj, "columns", None)
            if append is not None:
                new = []
                for c in columns:
                    new.append(append if c is None else f"{c}_{append}")
                columns = new
            return pd.DataFrame(obj, columns=columns, index=index)
        else:
            raise ValueError("Can only wrap 1 or 2-d array_like")
def _right_squeeze(arr, stop_dim=0):
    """
    Remove trailing singleton dimensions

    Parameters
    ----------
    arr : ndarray
        Input array
    stop_dim : int
        Dimension where checking should stop so that shape[i] is not checked
        for i < stop_dim

    Returns
    -------
    squeezed : ndarray
        Array with all trailing singleton dimensions (0 or 1) removed.
        Singleton dimensions for dimension < stop_dim are retained.
    """
    last = arr.ndim
    for s in reversed(arr.shape):
        if s > 1:
            break
        last -= 1
    last = max(last, stop_dim)

    return arr.reshape(arr.shape[:last])
def array_like(
    obj,
    name,
    dtype=np.double,
    ndim=1,
    maxdim=None,
    shape=None,
    order=None,
    contiguous=False,
    optional=False,
    writeable=True,
):
    """
    Convert array-like to a ndarray and check conditions

    Parameters
    ----------
    obj : array_like
         An array, any object exposing the array interface, an object whose
        __array__ method returns an array, or any (nested) sequence.
    name : str
        Name of the variable to use in exceptions
    dtype : {None, numpy.dtype, str}
        Required dtype. Default is double. If None, does not change the dtype
        of obj (if present) or uses NumPy to automatically detect the dtype
    ndim : {int, None}
        Required number of dimensions of obj. If None, no check is performed.
        If the number of dimensions of obj is less than ndim, additional axes
        are inserted on the right. See examples.
    maxdim : {int, None}
        Maximum allowed dimension.  Use ``maxdim`` instead of ``ndim`` when
        inputs are allowed to have ndim 1, 2, ..., or maxdim.
    shape : {tuple[int], None}
        Required shape obj.  If None, no check is performed. Partially
        restricted shapes can be checked using None. See examples.
    order : {'C', 'F', None}
        Order of the array
    contiguous : bool
        Ensure that the array's data is contiguous with order ``order``
    optional : bool
        Flag indicating whether None is allowed
    writeable : bool
        Whether to ensure the returned array is writeable

    Returns
    -------
    ndarray
        The converted input.
    """
    if optional and obj is None:
        return None
    reqs = ["W"] if writeable else []
    if order == "C" or contiguous:
        reqs += ["C"]
    elif order == "F":
        reqs += ["F"]
    arr = np.require(obj, dtype=dtype, requirements=reqs)
    if maxdim is not None:
        if arr.ndim > maxdim:
            msg = f"{name} must have ndim <= {maxdim}"
            raise ValueError(msg)
    elif ndim is not None:
        if arr.ndim > ndim:
            arr = _right_squeeze(arr, stop_dim=ndim)
        elif arr.ndim < ndim:
            arr = np.reshape(arr, arr.shape + (1,) * (ndim - arr.ndim))
        if arr.ndim != ndim:
            msg = "{0} is required to have ndim {1} but has ndim {2}"
            raise ValueError(msg.format(name, ndim, arr.ndim))
    if shape is not None:
        for actual, req in zip(arr.shape, shape):
            if req is not None and actual != req:
                req_shape = str(shape).replace("None, ", "*, ")
                msg = "{0} is required to have shape {1} but has shape {2}"
                raise ValueError(msg.format(name, req_shape, arr.shape))
    return arr

def freq_to_period(freq: Union[str, offsets.DateOffset]) -> int:
    """
    Convert a pandas frequency to a periodicity

    Parameters
    ----------
    freq : str or offset
        Frequency to convert

    Returns
    -------
    int
        Periodicity of freq

    Notes
    -----
    Annual maps to 1, quarterly maps to 4, monthly to 12, weekly to 52.
    """
    if not isinstance(freq, offsets.DateOffset):
        freq = to_offset(freq)  # go ahead and standardize
    assert isinstance(freq, offsets.DateOffset)
    freq = freq.rule_code.upper()

    yearly_freqs = ("A-", "AS-", "Y-", "YS-", "YE-")
    if freq in ("A", "Y") or freq.startswith(yearly_freqs):
        return 1
    elif freq == "Q" or freq.startswith(("Q-", "QS", "QE")):
        return 4
    elif freq == "M" or freq.startswith(("M-", "MS", "ME")):
        return 12
    elif freq == "W" or freq.startswith("W-"):
        return 52
    elif freq == "D":
        return 7
    elif freq == "B":
        return 5
    elif freq == "H":
        return 24
    else:  # pragma : no cover
        raise ValueError(
            "freq {} not understood. Please report if you "
            "think this is in error.".format(freq)
        )
    
def _pad_nans(x, head=None, tail=None):
    if np.ndim(x) == 1:
        if head is None and tail is None:
            return x
        elif head and tail:
            return np.r_[[np.nan] * head, x, [np.nan] * tail]
        elif tail is None:
            return np.r_[[np.nan] * head, x]
        elif head is None:
            return np.r_[x, [np.nan] * tail]
    elif np.ndim(x) == 2:
        if head is None and tail is None:
            return x
        elif head and tail:
            return np.r_[[[np.nan] * x.shape[1]] * head, x,
                         [[np.nan] * x.shape[1]] * tail]
        elif tail is None:
            return np.r_[[[np.nan] * x.shape[1]] * head, x]
        elif head is None:
            return np.r_[x, [[np.nan] * x.shape[1]] * tail]
    else:
        raise ValueError("Nan-padding for ndim > 2 not implemented")
    
def convolution_filter(x, filt, nsides=2):
    """
    Linear filtering via convolution. Centered and backward displaced moving
    weighted average.

    Parameters
    ----------
    x : array_like
        data array, 1d or 2d, if 2d then observations in rows
    filt : array_like
        Linear filter coefficients in reverse time-order. Should have the
        same number of dimensions as x though if 1d and ``x`` is 2d will be
        coerced to 2d.
    nsides : int, optional
        If 2, a centered moving average is computed using the filter
        coefficients. If 1, the filter coefficients are for past values only.
        Both methods use scipy.signal.convolve.

    Returns
    -------
    y : ndarray, 2d
        Filtered array, number of columns determined by x and filt. If a
        pandas object is given, a pandas object is returned. The index of
        the return is the exact same as the time period in ``x``
    """
    # for nsides shift the index instead of using 0 for 0 lag this
    # allows correct handling of NaNs
    if nsides == 1:
        trim_head = len(filt) - 1
        trim_tail = None
    elif nsides == 2:
        trim_head = int(np.ceil(len(filt)/2.) - 1) or None
        trim_tail = int(np.ceil(len(filt)/2.) - len(filt) % 2) or None
    else:  # pragma : no cover
        raise ValueError("nsides must be 1 or 2")

    pw = PandasWrapper(x)
    x = array_like(x, 'x', maxdim=2)
    filt = array_like(filt, 'filt', ndim=x.ndim)

    if filt.ndim == 1 or min(filt.shape) == 1:
        result = signal.convolve(x, filt, mode='valid')
    else:  # filt.ndim == 2
        nlags = filt.shape[0]
        nvar = x.shape[1]
        result = np.zeros((x.shape[0] - nlags + 1, nvar))
        if nsides == 2:
            for i in range(nvar):
                # could also use np.convolve, but easier for swiching to fft
                result[:, i] = signal.convolve(x[:, i], filt[:, i],
                                               mode='valid')
        elif nsides == 1:
            for i in range(nvar):
                result[:, i] = signal.convolve(x[:, i], np.r_[0, filt[:, i]],
                                               mode='valid')
    result = _pad_nans(result, trim_head, trim_tail)
    return pw.wrap(result)


__all__ = [
    "STL",
    "seasonal_decompose",
    "seasonal_mean",
    "DecomposeResult",
    "MSTL",
]


def _extrapolate_trend(trend, npoints):
    """
    Replace nan values on trend's end-points with least-squares extrapolated
    values with regression considering npoints closest defined points.
    """
    front = next(
        i for i, vals in enumerate(trend) if not np.any(np.isnan(vals))
    )
    back = (
        trend.shape[0]
        - 1
        - next(
            i
            for i, vals in enumerate(trend[::-1])
            if not np.any(np.isnan(vals))
        )
    )
    front_last = min(front + npoints, back)
    back_first = max(front, back - npoints)

    k, n = np.linalg.lstsq(
        np.c_[np.arange(front, front_last), np.ones(front_last - front)],
        trend[front:front_last],
        rcond=-1,
    )[0]
    extra = (np.arange(0, front) * np.c_[k] + np.c_[n]).T
    if trend.ndim == 1:
        extra = extra.squeeze()
    trend[:front] = extra

    k, n = np.linalg.lstsq(
        np.c_[np.arange(back_first, back), np.ones(back - back_first)],
        trend[back_first:back],
        rcond=-1,
    )[0]
    extra = (np.arange(back + 1, trend.shape[0]) * np.c_[k] + np.c_[n]).T
    if trend.ndim == 1:
        extra = extra.squeeze()
    trend[back + 1 :] = extra

    return trend


def seasonal_mean(x, period):
    """
    Return means for each period in x. period is an int that gives the
    number of periods per cycle. E.g., 12 for monthly. NaNs are ignored
    in the mean.
    """
    return np.array([pd_nanmean(x[i::period], axis=0) for i in range(period)])

def _import_mpl():
    """This function is not needed outside this utils module."""
    try:
        import matplotlib.pyplot as plt
    except:
        raise ImportError("Matplotlib is not found.")

    return plt


def seasonal_decompose(
    x,
    model="additive",
    filt=None,
    period=None,
    two_sided=True,
    extrapolate_trend=0,
):
    """
    Seasonal decomposition using moving averages.

    Parameters
    ----------
    x : array_like
        Time series. If 2d, individual series are in columns. x must contain 2
        complete cycles.
    model : {"additive", "multiplicative"}, optional
        Type of seasonal component. Abbreviations are accepted.
    filt : array_like, optional
        The filter coefficients for filtering out the seasonal component.
        The concrete moving average method used in filtering is determined by
        two_sided.
    period : int, optional
        Period of the series (eg, 1 for annual, 4 for quarterly, etc). Must be
        used if x is not a pandas object or if the index of x does not have a
        frequency. Overrides default periodicity of x if x is a pandas object
        with a timeseries index.
    two_sided : bool, optional
        The moving average method used in filtering.
        If True (default), a centered moving average is computed using the
        filt. If False, the filter coefficients are for past values only.
    extrapolate_trend : int or 'freq', optional
        If set to > 0, the trend resulting from the convolution is
        linear least-squares extrapolated on both ends (or the single one
        if two_sided is False) considering this many (+1) closest points.
        If set to 'freq', use `freq` closest points. Setting this parameter
        results in no NaN values in trend or resid components.

    Returns
    -------
    DecomposeResult
        A object with seasonal, trend, and resid attributes.

    See Also
    --------
    statsmodels.tsa.filters.bk_filter.bkfilter
        Baxter-King filter.
    statsmodels.tsa.filters.cf_filter.cffilter
        Christiano-Fitzgerald asymmetric, random walk filter.
    statsmodels.tsa.filters.hp_filter.hpfilter
        Hodrick-Prescott filter.
    statsmodels.tsa.filters.convolution_filter
        Linear filtering via convolution.
    statsmodels.tsa.seasonal.STL
        Season-Trend decomposition using LOESS.

    Notes
    -----
    This is a naive decomposition. More sophisticated methods should
    be preferred.

    The additive model is Y[t] = T[t] + S[t] + e[t]

    The multiplicative model is Y[t] = T[t] * S[t] * e[t]

    The results are obtained by first estimating the trend by applying
    a convolution filter to the data. The trend is then removed from the
    series and the average of this de-trended series for each period is
    the returned seasonal component.
    """
    pfreq = period
    pw = PandasWrapper(x)
    if period is None:
        pfreq = getattr(getattr(x, "index", None), "inferred_freq", None)

    x = array_like(x, "x", maxdim=2)
    nobs = len(x)

    if not np.all(np.isfinite(x)):
        raise ValueError("This function does not handle missing values")
    if model.startswith("m"):
        if np.any(x <= 0):
            raise ValueError(
                "Multiplicative seasonality is not appropriate "
                "for zero and negative values"
            )

    if period is None:
        if pfreq is not None:
            pfreq = freq_to_period(pfreq)
            period = pfreq
        else:
            raise ValueError(
                "You must specify a period or x must be a pandas object with "
                "a PeriodIndex or a DatetimeIndex with a freq not set to None"
            )
    if x.shape[0] < 2 * pfreq:
        raise ValueError(
            f"x must have 2 complete cycles requires {2 * pfreq} "
            f"observations. x only has {x.shape[0]} observation(s)"
        )

    if filt is None:
        if period % 2 == 0:  # split weights at ends
            filt = np.array([0.5] + [1] * (period - 1) + [0.5]) / period
        else:
            filt = np.repeat(1.0 / period, period)

    nsides = int(two_sided) + 1
    trend = convolution_filter(x, filt, nsides)

    if extrapolate_trend == "freq":
        extrapolate_trend = period - 1

    if extrapolate_trend > 0:
        trend = _extrapolate_trend(trend, extrapolate_trend + 1)

    if model.startswith("m"):
        detrended = x / trend
    else:
        detrended = x - trend

    period_averages = seasonal_mean(detrended, period)

    if model.startswith("m"):
        period_averages /= np.mean(period_averages, axis=0)
    else:
        period_averages -= np.mean(period_averages, axis=0)

    seasonal = np.tile(period_averages.T, nobs // period + 1).T[:nobs]

    if model.startswith("m"):
        resid = x / seasonal / trend
    else:
        resid = detrended - seasonal

    results = []
    for s, name in zip(
        (seasonal, trend, resid, x), ("seasonal", "trend", "resid", None)
    ):
        results.append(pw.wrap(s.squeeze(), columns=name))
    return DecomposeResult(
        seasonal=results[0],
        trend=results[1],
        resid=results[2],
        observed=results[3],
    )

class DecomposeResult:
    """
    Results class for seasonal decompositions

    Parameters
    ----------
    observed : array_like
        The data series that has been decomposed.
    seasonal : array_like
        The seasonal component of the data series.
    trend : array_like
        The trend component of the data series.
    resid : array_like
        The residual component of the data series.
    weights : array_like, optional
        The weights used to reduce outlier influence.
    """

    def __init__(self, observed, seasonal, trend, resid, weights=None):
        self._seasonal = seasonal
        self._trend = trend
        if weights is None:
            weights = np.ones_like(observed)
            if isinstance(observed, pd.Series):
                weights = pd.Series(
                    weights, index=observed.index, name="weights"
                )
        self._weights = weights
        self._resid = resid
        self._observed = observed

    @property
    def observed(self):
        """Observed data"""
        return self._observed

    @property
    def seasonal(self):
        """The estimated seasonal component"""
        return self._seasonal

    @property
    def trend(self):
        """The estimated trend component"""
        return self._trend

    @property
    def resid(self):
        """The estimated residuals"""
        return self._resid

    @property
    def weights(self):
        """The weights used in the robust estimation"""
        return self._weights

    @property
    def nobs(self):
        """Number of observations"""
        return self._observed.shape

    def plot(
        self,
        observed=True,
        seasonal=True,
        trend=True,
        resid=True,
        weights=False,
    ):
        """
        Plot estimated components

        Parameters
        ----------
        observed : bool
            Include the observed series in the plot
        seasonal : bool
            Include the seasonal component in the plot
        trend : bool
            Include the trend component in the plot
        resid : bool
            Include the residual in the plot
        weights : bool
            Include the weights in the plot (if any)

        Returns
        -------
        matplotlib.figure.Figure
            The figure instance that containing the plot.
        """
        from pandas.plotting import register_matplotlib_converters

        plt = _import_mpl()
        register_matplotlib_converters()
        series = [(self._observed, "Observed")] if observed else []
        series += [(self.trend, "trend")] if trend else []

        if self.seasonal.ndim == 1:
            series += [(self.seasonal, "seasonal")] if seasonal else []
        elif self.seasonal.ndim > 1:
            if isinstance(self.seasonal, pd.DataFrame):
                for col in self.seasonal.columns:
                    series += (
                        [(self.seasonal[col], "seasonal")] if seasonal else []
                    )
            else:
                for i in range(self.seasonal.shape[1]):
                    series += (
                        [(self.seasonal[:, i], "seasonal")] if seasonal else []
                    )

        series += [(self.resid, "residual")] if resid else []
        series += [(self.weights, "weights")] if weights else []

        if isinstance(self._observed, (pd.DataFrame, pd.Series)):
            nobs = self._observed.shape[0]
            xlim = self._observed.index[0], self._observed.index[nobs - 1]
        else:
            xlim = (0, self._observed.shape[0] - 1)

        fig, axs = plt.subplots(len(series), 1, sharex=True)
        for i, (ax, (series, def_name)) in enumerate(zip(axs, series)):
            if def_name != "residual":
                ax.plot(series)
            else:
                ax.plot(series, marker="o", linestyle="none")
                ax.plot(xlim, (0, 0), color="#000000", zorder=-3)
            name = getattr(series, "name", def_name)
            if def_name != "Observed":
                name = name.capitalize()
            title = ax.set_title if i == 0 and observed else ax.set_ylabel
            title(name)
            ax.set_xlim(xlim)

        fig.tight_layout()
        return fig