from astropy.io import fits
from ..utils.helper import checkoptions
import warnings
from pathlib import Path

def load_magnetogram_from_path(magnetogram_path):
    """
    Load FITS data from specified path for solar flare analysis.

    Args:
    - magnetogram_path (str): absolute file path for magnetogram.

    Returns:
    - tuple: Tuple containing magnetogram data and header data.
    """

    # Read magnetogram
    HMI_fits = fits.open(magnetogram_path, cache=False)
    HMI_fits.verify('fix')
    dataHMI = HMI_fits[1].data
    dataHMI_header = HMI_fits[1].header

    return dataHMI, dataHMI_header


def load_bitmap_from_path(bitmap_path):
    """
    Load FITS data from specified path for solar flare analysis.

    Args:
    - bitmap_path (str): absolute file path for bitmap.

    Returns:
    - array: bitmap data.
    """

    # Read bitmap
    bitmap_hdul = fits.open(bitmap_path, cache=False)
    bitmap_hdul.verify('fix')
    bitmap_data = bitmap_hdul[0].data

    return bitmap_data
