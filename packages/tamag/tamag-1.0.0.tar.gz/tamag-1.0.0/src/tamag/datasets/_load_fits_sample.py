from astropy.io import fits
from ..utils.helper import checkoptions
import warnings
from pathlib import Path

def load_fits_data(fits_type="patch", sample_no=1):
    """
    Load FITS data for solar flare analysis.

    Args:
    - fits_type (str): Type of FITS data to load. Either `patch` or `fulldisk`. Default is `patch`.
    - sample_no (int): Sample number. Default is 1.

    Returns:
    - tuple: Tuple containing magnetogram data, magnetogram header, and bitmap data.
    """

    checkoptions(fits_type, ["patch", "fulldisk"], 'fits_type')

    # Get the root directory of the package
    package_dir = Path(__file__).parent.parent

    if  fits_type == 'patch':
        file_path = f'datasets/patch_samples/hmi.sharp_{fits_type}_sample_{sample_no}_TAI'
    elif fits_type == 'fulldisk':
        file_path = f'datasets/fulldisk_samples/hmi.sharp_{fits_type}_sample_{sample_no}_TAI'
        # file_path =f'datasets/fulldisk_samples/hmi.m_720s.20111217_060000_TAI.1'

    # Read AR_PATCH
    HMI_fits_path = package_dir / f'{file_path}.magnetogram.fits'
    HMI_fits = fits.open(HMI_fits_path, cache=False)
    HMI_fits.verify('fix')
    dataHMI = HMI_fits[1].data
    dataHMI_header = HMI_fits[1].header

    if fits_type == 'patch':
        # Read Bitmap
        bitmap_path = package_dir / f'{file_path}.bitmap.fits'
        bitmap_hdul = fits.open(bitmap_path, cache=False)
        bitmap_hdul.verify('fix')
        bitmap_data = bitmap_hdul[0].data
        return dataHMI, dataHMI_header, bitmap_data

    elif fits_type == 'fulldisk':
        return dataHMI, dataHMI_header, None

