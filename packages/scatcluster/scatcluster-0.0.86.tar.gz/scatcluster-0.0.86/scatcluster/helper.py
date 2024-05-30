"""
ScatCluster Helper
"""
import importlib
import itertools
from string import ascii_uppercase

import numpy as np
from scipy.stats import median_abs_deviation


def is_gpu_available():
    """Check if the GPU is available."""
    cupy_spec = importlib.util.find_spec('cupy')
    return cupy_spec is not None


def round_nearest(x, a):
    """
    Rounds a number `x` to the nearest multiple of `a`.

    Parameters:
        x (float): The number to be rounded.
        a (float): The multiple to round to.

    Returns:
        float: The rounded number.
    """
    return round(x / a) * a


def is_notebook() -> bool:
    """
    A function to check if the code is running in a Jupyter notebook or IPython terminal.

    Returns:
        bool: True if running in a Jupyter notebook or qtconsole, False otherwise.
    """
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False


def tqdm_importer():
    """
    A function that imports the tqdm module based on the current environment.
    """
    if is_notebook():
        pass
    else:
        pass


def demad(x, factor=10.0):
    """Normalize signal with median absolute deviation.

    Parameters
    ----------
    x : np.ndarray
        The input signal.
    factor : float, optional
        An additional normalization factor.

    Returns
    -------
    The data normalized with median absolute deviation.
    """
    mad = median_abs_deviation(x)
    return x / np.mean(mad) / factor


COLORS = [
    '0.8',
    '#222222',
    '#F3C300',
    '#875692',
    '#F38400',
    '#A1CAF1',
    '#BE0032',
    '#C2B280',
    '#848482',
    '#008856',
    '#E68FAC',
    '#0067A5',
    '#F99379',
    '#604E97',
    '#F6A600',
    '#B3446C',
    '#DCD300',
    '#882D17',
    '#8DB600',
    '#654522',
    '#E25822',
    '#2B3D26',
    '0.8',
    '#222222',
    '#F3C300',
    '#875692',
    '#F38400',
    '#A1CAF1',
    '#BE0032',
    '#C2B280',
    '#848482',
    '#008856',
    '#E68FAC',
    '#0067A5',
    '#F99379',
    '#604E97',
    '#F6A600',
    '#B3446C',
    '#DCD300',
    '#882D17',
    '#8DB600',
    '#654522',
    '#E25822',
    '#2B3D26',
    '0.8',
    '#222222',
    '#F3C300',
    '#875692',
    '#F38400',
    '#A1CAF1',
    '#BE0032',
    '#C2B280',
    '#848482',
    '#008856',
    '#E68FAC',
    '#0067A5',
    '#F99379',
    '#604E97',
    '#F6A600',
    '#B3446C',
    '#DCD300',
    '#882D17',
    '#8DB600',
    '#654522',
    '#E25822',
    '#2B3D26',
]


def iter_all_strings():
    """
    Generates all possible strings of uppercase letters of increasing length.

    Returns:
        A generator that yields all possible strings.
    """
    for size in itertools.count(1):
        for s in itertools.product(ascii_uppercase, repeat=size):
            yield ''.join(s)


def list_of_strings(number_letters):
    """
    Generates a list of strings of length 'number_letters' using itertools.islice and iter_all_strings.

    Parameters:
        number_letters (int): The number of strings to generate.

    Returns:
        list: A list of strings of length 'number_letters'.
    """
    return list(itertools.islice(iter_all_strings(), number_letters))
