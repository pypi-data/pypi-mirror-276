"""A collection of miscellaneous helper functions

This module contains the following functions:

* :func:`FreqResp2RealImag`: Calculate real and imaginary parts from frequency
  response
* :func:`is_2d_matrix`: Check if a np.ndarray is a matrix
* :func:`is_2d_square_matrix`: Check if a np.ndarray is a two-dimensional square matrix
* :func:`is_vector`: Check if a np.ndarray is a vector
* :func:`make_semiposdef`: Make quadratic matrix positive semi-definite
* :func:`normalize_vector_or_matrix`: Scale an array of numbers to the interval between
  zero and one
* :func:`number_of_rows_equals_vector_dim`: Check if a matrix and a vector match in size
* :func:`plot_vectors_and_covariances_comparison`: Plot two vectors and their
  covariances side-by-side for visual comparison
* :func:`print_mat`: Print matrix (2D array) to the console or return as formatted
  string
* :func:`print_vec`: Print vector (1D array) to the console or return as formatted
  string
* :func:`progress_bar`: A simple and reusable progress-bar
* :func:`shift_uncertainty`: Shift the elements in the vector x and associated
  uncertainties ux
* :func:`trimOrPad`: Trim or pad (with zeros) a vector/array to the desired length(s)
* :func:`complex_2_real_imag`: Take a np.ndarray with dtype complex and return
  real and imaginary parts
* :func:`real_imag_2_complex`: Take a np.ndarray with real and imaginary parts
  and return dtype complex ndarray
* :func:`separate_real_imag_of_mc_samples`: Split a np.ndarray containing MonteCarlo
  samples' real and imaginary parts
* :func:`separate_real_imag_of_vector`: Split a np.ndarray containing real and
  imaginary parts into half
"""

__all__ = [
    "print_mat",
    "print_vec",
    "make_semiposdef",
    "FreqResp2RealImag",
    "make_equidistant",
    "trimOrPad",
    "progress_bar",
    "shift_uncertainty",
    "is_vector",
    "is_2d_matrix",
    "number_of_rows_equals_vector_dim",
    "plot_vectors_and_covariances_comparison",
    "is_2d_square_matrix",
    "normalize_vector_or_matrix",
    "complex_2_real_imag",
    "real_imag_2_complex",
    "separate_real_imag_of_mc_samples",
    "separate_real_imag_of_vector",
]

from typing import Any, List, Optional, Union

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from scipy.sparse import eye, issparse
from scipy.sparse.linalg import eigs


def shift_uncertainty(x: np.ndarray, ux: np.ndarray, shift: int):
    """Shift the elements in the vector x and associated uncertainties ux

    This function uses :func:`numpy.roll` to shift the elements in x
    and ux. See the linked official documentation for details.

    Parameters
    ----------
    x : np.ndarray of shape (N,)
        vector of estimates
    ux : float, np.ndarray of shape (N,) or of shape (N,N)
        uncertainty associated with the vector of estimates
    shift : int
        amount of shift

    Returns
    -------
    shifted_x : (N,) np.ndarray
        shifted vector of estimates
    shifted_ux : float, np.ndarray of shape (N,) or of shape (N,N)
        uncertainty associated with the shifted vector of estimates

    Raises
    ------
    ValueError
        If shift, x or ux are of unexpected type, dimensions of x and ux do not fit
        or ux is of unexpected shape
    """

    shifted_x = _shift_vector(vector=x, shift=shift)

    if isinstance(ux, float):
        return shifted_x, ux

    if isinstance(ux, np.ndarray):
        if is_vector(ux):
            return shifted_x, _shift_vector(vector=ux, shift=shift)
        elif is_2d_square_matrix(ux):
            shifted_ux = _shift_2d_matrix(ux, shift)
            return shifted_x, shifted_ux
        raise ValueError(
            "shift_uncertainty: input uncertainty ux is expected to be a vector or "
            f"two-dimensional, square matrix but is of shape {ux.shape}."
        )

    raise ValueError(
        "shift_uncertainty: input uncertainty ux is expected to be a float or a "
        f"numpy.ndarray but is of type {type(ux)}."
    )


def _cast_shift_to_int(shift: Any) -> int:
    try:
        return int(shift)
    except ValueError:
        raise ValueError(
            "shift_uncertainty: shift is expected to be type int or at least "
            f"cast-able to int, but is {shift} of type {type(shift)}. Please provide "
            "a valid value."
        )


def _shift_vector(vector: np.ndarray, shift: int) -> np.ndarray:
    return np.roll(vector, shift)


def _shift_2d_matrix(matrix: np.ndarray, shift: int) -> np.ndarray:
    return np.roll(matrix, (shift, shift), axis=(0, 1))


def trimOrPad(
    array: Union[List, np.ndarray],
    length: Union[int, tuple],
    mode: str = "constant",
    real_imag_type: bool = False,
):
    """Trim or pad (with zeros) a vector/array to the desired length(s)

    Either trim or zero-pad each axis of an array to achieve a specified `length`.
    The trimming/padding is applied at the end of (each axis of) the array.
    The implementation allows for some axis to be trimmed, while others can be padded
    at the same time.

    Parameters
    ----------
    array : list, ND np.ndarray
        original data
    length : int, tuple of int
        length or shape of output
    mode : str, optional
        handed over to np.pad, default "constant"
    real_imag_type : bool, optional
        if array is to be interpreted as PyDynamic real-imag-type, defaults to False
        only works for 1D and square-2D arrays (of even length)

    Returns
    -------
    array_modified : np.ndarray of shape similar to length
        An either trimmed or zero-padded array
    """

    # force numpy array
    array = np.array(array)

    # split and reassemble if vector/covariance is in real-imag representation
    # (only works for 1D and 2D-square arrays of even length)
    if real_imag_type:
        N = array.shape[0] // 2
        kwargs = {
            "length": length,
            "mode": "constant",
            "real_imag_type": False,
        }

        if len(array.shape) == 1:
            REAL = trimOrPad(array[:N], **kwargs)
            IMAG = trimOrPad(array[N:], **kwargs)
            return np.r_[REAL, IMAG]

        elif is_2d_square_matrix(array):
            RR = trimOrPad(array[:N, :N], **kwargs)
            RI = trimOrPad(array[:N, N:], **kwargs)
            IR = trimOrPad(array[N:, :N], **kwargs)
            II = trimOrPad(array[N:, N:], **kwargs)

            return np.block([[RR, RI], [IR, II]])

        else:
            raise ValueError(
                f"Array of shape {array.shape} cannot "
                "be interpreted as real/imag representation. "
                "Only 1D arrays of even length or 2D square arrays "
                "of even length can be interpreted as real/imag."
            )

    # just trim/pad at the end otherwise
    else:
        # convert uniform length on all axis into internal tuple representation
        if isinstance(length, int):
            length = [length] * len(array.shape)

        # prepare padding and trimming arguments
        pad_lengths = []
        trim_slices = []
        for axis_length, axis_new_length in zip(array.shape, length):
            diff = axis_new_length - axis_length

            # prepare padding
            if diff > 0:
                pad_lengths.append((0, diff))
            else:
                pad_lengths.append((0, 0))

            # prepare trimming
            trim_slices.append(slice(0, axis_new_length))

        # first pad, what needs to be padded
        # then trim (does nothing, if all axis have been padded)
        return np.pad(array, pad_lengths, mode=mode)[tuple(trim_slices)]


def print_vec(vector, prec=5, retS=False, vertical=False):
    """Print vector (1D array) to the console or return as formatted string

    Parameters
    ----------
    vector : (M,) array_like
    prec : int
        the precision of the output
    vertical : bool
        print out vertical or not
    retS : bool
        print or return string

    Returns
    -------
    s : str
        if retS is True

    """

    if vertical:
        t = "\n"
    else:
        t = "\t"
    s = "".join(["%1.*g %s" % (int(prec), s, t) for s in vector])
    if retS:
        return s
    else:
        print(s)


def print_mat(matrix, prec=5, vertical=False, retS=False):
    """Print matrix (2D array) to the console or return as formatted string

    Parameters
    ----------
    matrix : (M,N) array_like
    prec : int
        the precision of the output
    vertical : bool
        print out vertical or not
    retS : bool
        print or return string

    Returns
    -------
    s : str
        if retS is True

    """

    if vertical:
        matrix = matrix.T

    s = "".join(
        [
            print_vec(matrix[k, :], prec=prec, vertical=False, retS=True) + "\n"
            for k in range(matrix.shape[0])
        ]
    )

    if retS:
        return s

    print(s)


def make_semiposdef(
    matrix: np.ndarray,
    maxiter: Optional[int] = 10,
    tol: Optional[float] = 1e-12,
    verbose: Optional[bool] = False,
) -> np.ndarray:
    """Make quadratic matrix positive semi-definite by increasing its eigenvalues

    Parameters
    ----------
    matrix : array_like of shape (N,N)
        the matrix to process
    maxiter : int, optional
        the maximum number of iterations for increasing the eigenvalues, defaults to 10
    tol : float, optional
        tolerance for deciding if pos. semi-def., defaults to 1e-12
    verbose : bool, optional
        If True print smallest eigenvalue of the resulting matrix, if False (default)
        be quiet

    Returns
    -------
    (N,N) array_like
        quadratic positive semi-definite matrix

    Raises
    ------
    ValueError
        If matrix is not square.
    """
    n, m = matrix.shape
    if n != m:
        raise ValueError("Matrix has to be quadratic")
    # use specialised functions for sparse matrices
    if issparse(matrix):
        # enforce symmetric matrix
        matrix = 0.5 * (matrix + matrix.T)
        # calculate smallest eigenvalue
        e = np.min(np.real(eigs(matrix, which="SR", return_eigenvectors=False)))
        count = 0
        # increase the eigenvalues until matrix is positive semi-definite
        while e < tol and count < maxiter:
            matrix += (np.absolute(e) + tol) * eye(n, format=matrix.format)
            e = np.min(np.real(eigs(matrix, which="SR", return_eigenvectors=False)))
            count += 1
        e = np.min(np.real(eigs(matrix, which="SR", return_eigenvectors=False)))
    # same procedure for non-sparse matrices
    else:
        matrix = 0.5 * (matrix + matrix.T)
        count = 0
        e = np.min(np.real(np.linalg.eigvals(matrix)))
        while e < tol and count < maxiter:
            e = np.min(np.real(np.linalg.eigvals(matrix)))
            matrix += (np.absolute(e) + tol) * np.eye(n)
        e = np.min(np.real(np.linalg.eigvals(matrix)))
    if verbose:
        print("Final result of make_semiposdef: smallest eigenvalue is %e" % e)
    return matrix


def FreqResp2RealImag(
    Abs: np.ndarray, Phase: np.ndarray, Unc: np.ndarray, MCruns: Optional[int] = 1000
):
    """Calculate real and imaginary parts from frequency response

    Calculate real and imaginary parts from amplitude and phase with
    associated uncertainties.

    Parameters
    ----------
    Abs : (N,) array_like
        amplitude values
    Phase : (N,) array_like
        phase values in rad
    Unc : (2N, 2N) or (2N,) array_like
        uncertainties either as full covariance matrix or as its main diagonal
    MCruns : int, optional
        number of iterations for Monte Carlo simulation, defaults to 1000

    Returns
    -------
    Re, Im : (N,) array_like
        best estimate of real and imaginary parts
    URI : (2N, 2N) array_like
        uncertainties assoc. with Re and Im
    """

    if len(Abs) != len(Phase) or 2 * len(Abs) != len(Unc):
        raise ValueError("\nLength of inputs are inconsistent.")

    if len(Unc.shape) == 1:
        Unc = np.diag(Unc)

    Nf = len(Abs)

    AbsPhas = np.random.multivariate_normal(
        np.hstack((Abs, Phase)), Unc, int(MCruns)
    )  # draw MC inputs

    H = AbsPhas[:, :Nf] * np.exp(
        1j * AbsPhas[:, Nf:]
    )  # calculate complex frequency response values
    RI = np.hstack((np.real(H), np.imag(H)))  # transform to real, imag

    Re = np.mean(RI[:, :Nf])
    Im = np.mean(RI[:, Nf:])
    URI = np.cov(RI, rowvar=False)

    return Re, Im, URI


def make_equidistant(*args, **kwargs):
    """
    .. deprecated:: 2.0.0
        Please use :func:`PyDynamic.uncertainty.interpolate.make_equidistant`
    """
    raise DeprecationWarning(
        "The method `PyDynamic.misc.tools.make_equidistant` is moved "
        "to :mod:`PyDynamic.uncertainty.interpolate.make_equidistant` since the last "
        "major release 2.0.0. Please switch to the current module immediately and use "
        "the current function "
        ":func:`PyDynamic.uncertainty.interpolate.make_equidistant`. Please change "
        "'from PyDynamic.misc.tools import make_equidistant' to 'from "
        "PyDynamic.uncertainty.interpolate import make_equidistant'."
    )


def progress_bar(
    count,
    count_max,
    width: Optional[int] = 30,
    prefix: Optional[str] = "",
    done_indicator: Optional[str] = "#",
    todo_indicator: Optional[str] = ".",
    fout: Optional[bytes] = None,
):
    """A simple and reusable progress-bar

    Parameters
    ----------
    count : int
        current status of iterations, assumed to be zero-based
    count_max : int
        total number of iterations
    width : int, optional
        width of the actual progressbar (actual printed line will be wider), default to
        30
    prefix : str, optional
        some text that will be printed in front of the bar (i.e.
        "Progress of ABC:"), if not given only progressbar itself will be printed
    done_indicator : str, optional
        what character is used as "already-done"-indicator, defaults to "#"
    todo_indicator : str, optional
        what character is used as "not-done-yet"-indicator, defaults to "."
    fout : file-object, optional
        where the progress-bar should be written/printed to, defaults to direct print
        to stdout
    """
    x = int(width * (count + 1) / count_max)
    progressString = "{PREFIX}[{DONE}{NOTDONE}] {COUNT}/{COUNTMAX}\r".format(
        PREFIX=prefix,
        DONE=x * done_indicator,
        NOTDONE=(width - x) * todo_indicator,
        COUNT=count + 1,
        COUNTMAX=count_max,
    )
    if fout is not None:
        fout.write(progressString)
    else:
        print(progressString)


def is_vector(ndarray: np.ndarray) -> bool:
    """Check if a np.ndarray is a vector, i.e. is of shape (n,)

    Parameters
    ----------
    ndarray : np.ndarray
        the array to check

    Returns
    -------
    bool
        True, if the array expands over one dimension only, False otherwise
    """
    return len(ndarray.shape) == 1


def is_2d_matrix(ndarray: np.ndarray) -> bool:
    """Check if a np.ndarray is a matrix, i.e. is of shape (n,m)

    Parameters
    ----------
    ndarray : np.ndarray
        the array to check

    Returns
    -------
    bool
        True, if the array expands over exactly two dimensions, False otherwise
    """
    return len(ndarray.shape) == 2


def number_of_rows_equals_vector_dim(matrix: np.ndarray, vector: np.ndarray) -> bool:
    """Check if a matrix has the same number of rows as a vector

    Parameters
    ----------
    matrix : np.ndarray
        the matrix, that is supposed to have the same number of rows
    vector : np.ndarray
        the vector, that is supposed to have the same number of elements

    Returns
    -------
    bool
        True, if the number of rows coincide, False otherwise
    """
    return len(vector) == matrix.shape[0]


def plot_vectors_and_covariances_comparison(
    vector_1: np.ndarray,
    vector_2: np.ndarray,
    covariance_1: np.ndarray,
    covariance_2: np.ndarray,
    title: Optional[str] = "Comparison between two vectors and corresponding "
    "uncertainties",
    label_1: Optional[str] = "vector_1",
    label_2: Optional[str] = "vector_2",
):
    """Plot two vectors and their covariances side-by-side for visual comparison

    Parameters
    ----------
    vector_1 : np.ndarray
        the first vector to compare
    vector_2 : np.ndarray
        the second vector to compare
    covariance_1 : np.ndarray
        the first covariance matrix to compare
    covariance_2 : np.ndarray
        the second covariance matrix to compare
    title : str, optional
        the title for the comparison plot, defaults to `"Comparison between two vectors
        and corresponding uncertainties"`
    label_1 : str, optional
        the label for the first vector in the legend and title for the first
        covariance plot, defaults to "vector_1"
    label_2 : str, optional
        the label for the second vector in the legend and title for the second
        covariance plot, defaults to "vector_2"
    """
    fig, ax = plt.subplots(nrows=2, ncols=2)
    fig.suptitle(title)
    ax[0][0].imshow(covariance_1)
    ax[0][0].set_title(label_1 + " uncertainties")
    ax[0][1].imshow(covariance_2)
    ax[0][1].set_title(label_2 + " uncertainties")
    ax[1][0].plot(vector_1, label=label_1)
    ax[1][0].plot(vector_2, label=label_2)
    ax[1][0].legend()
    ax[1][0].set_title(label_1 + " and " + label_2)
    ax[1][1].imshow(covariance_2 - covariance_1, norm=Normalize())
    ax[1][1].set_title("Relative difference of uncertainties")
    plt.show()


def is_2d_square_matrix(ndarray: np.ndarray) -> bool:
    """Check if a np.ndarray is a two-dimensional square matrix, i.e. is of shape (n,n)

    Parameters
    ----------
    ndarray : np.ndarray
        the array to check

    Returns
    -------
    bool
        True, if the array expands over exactly two dimensions of similar size,
        False otherwise
    """
    return is_2d_matrix(ndarray) and ndarray.shape[0] == ndarray.shape[1]


def normalize_vector_or_matrix(numbers: np.ndarray) -> np.ndarray:
    """Scale an array of numbers to the interval between zero and one

    If all values in the array are the same, the output array will be constant zero.

    Parameters
    ----------
    numbers : np.ndarray
        the :class:`numpy.ndarray` to normalize

    Returns
    -------
    np.ndarray
        the normalized array
    """
    minimum = translator = np.min(numbers)
    array_span = np.max(numbers) - minimum
    normalizer = array_span or 1.0
    return (numbers - translator) / normalizer


def complex_2_real_imag(array: np.ndarray) -> np.ndarray:
    r"""Take an array of any non-flexible scalar dtype to return real and imaginary part

    The input array :math:`x \in \mathbb R^m` is reassembled to the form
    of the expected input of some of the functions in the modules
    :mod:`propagate_DFT <PyDynamic.uncertainty.propagate_DFT>` and
    :mod:`fit_filter <PyDynamic.model_estimation.fit_filter>`: :math:`y = \left(
    \operatorname{Re}(x), \operatorname{Im}(x) \right)`.

    Parameters
    ----------
    array : np.ndarray of shape (M,)
        the array to assemble the version with real and imaginary parts from

    Returns
    -------
    np.ndarray of shape (2M,)
        the array of real and imaginary parts
    """
    return np.hstack((np.real(array), np.imag(array)))


def real_imag_2_complex(array: np.ndarray) -> np.ndarray:
    r"""Take a np.ndarray with real and imaginary parts and return dtype complex ndarray

    The input array :math:`x \in \mathbb R^{2m}` representing a complex vector
    :math:`y \in \mathbb C^m` has the form of the expected input of
    some of the functions in the modules
    :mod:`propagate_DFT <PyDynamic.uncertainty.propagate_DFT>` and
    :mod:`fit_filter <PyDynamic.model_estimation.fit_filter>`: :math:`x = \left(
    \operatorname{Re}(y), \operatorname{Im}(y) \right)` or a np.ndarray containing
    several of these.

    Parameters
    ----------
    array : np.ndarray of shape (N,2M) or of shape (2M,)
        the array of any integer or floating dtype to assemble the complex version of

    Returns
    -------
    np.ndarray of shape (N,M) or of shape (M,)
        the complex array
    """
    if is_2d_matrix(array):
        real, imag = separate_real_imag_of_mc_samples(array)
    else:
        real, imag = separate_real_imag_of_vector(array)
    return real + 1j * imag


def separate_real_imag_of_mc_samples(array: np.ndarray) -> List[np.ndarray]:
    r"""Split a np.ndarray containing MonteCarlo samples real and imaginary parts

    The input array :math:`x \in \mathbb R^{n \times 2m}` representing an
    n-elemental array of complex vectors :math:`y_i \in \mathbb C^m` has the form of
    the expected input of some of the functions in the modules
    :mod:`propagate_DFT <PyDynamic.uncertainty.propagate_DFT>` and
    :mod:`fit_filter <PyDynamic.model_estimation.fit_filter>`: :math:`x = \left(
    \operatorname{Re}(y_i), \operatorname{Im}(y_i) \right)_{i=1,\ldots,n}`.

    Parameters
    ----------
    array : np.ndarray of shape (N,2M)
        the array of any integer or floating dtype to assemble the complex version of

    Returns
    -------
    list of two np.ndarrays of shape (N,M)
        two-element list of the two arrays containing the real and imaginary parts
    """
    if _vector_has_odd_length(array[0]):
        raise ValueError(
            "separate_real_imag_of_mc_samples: vectors of real and imaginary "
            "parts are expected to contain exactly as many real as "
            f"imaginary parts but the first one is of odd length={len(array[0])}."
        )
    return np.split(ary=array, indices_or_sections=2, axis=1)


def separate_real_imag_of_vector(vector: np.ndarray) -> List[np.ndarray]:
    r"""Split a np.ndarray containing real and imaginary parts into half

    The input array :math:`x \in \mathbb R^{2m}` representing a complex vector
    :math:`y \in \mathbb C^m` has the form of
    the expected input of some of the functions in the modules
    :mod:`propagate_DFT <PyDynamic.uncertainty.propagate_DFT>` and
    :mod:`fit_filter <PyDynamic.model_estimation.fit_filter>`:
    :math:`x = \left( \operatorname{Re}(y), \operatorname{Im}(y) \right)`.

    Parameters
    ----------
    vector : np.ndarray of shape (2M,)
        the array of any integer or floating dtype to assemble the complex version of

    Returns
    -------
    list of two np.ndarrays of shape (M,)
        two-element list of the two arrays containing the real and imaginary parts
    """
    if _vector_has_odd_length(vector):
        raise ValueError(
            "separate_real_imag_of_vector: vector of real and imaginary "
            "parts is expected to contain exactly as many real as "
            f"imaginary parts but is of odd length={len(vector)}."
        )
    return np.split(ary=vector, indices_or_sections=2)


def _vector_has_odd_length(vector: np.ndarray) -> bool:
    return len(vector) % 2 == 1
