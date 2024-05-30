"""
Module: byte_scaling_transformer
Description: Contains the ByteScaling Module for applying byte scaling to an input array.
"""

import numpy as np
from ..utils.logger import VerboseLogger
from ..utils.helper import checktype, to_rgb, checkoptions, background, apply_mask
from ..utils.exceptions import NoHeaderError

class ByteScaling:

    def __init__(self,  fits_type='patch', min_value=None, max_value=None, scaler=255, verbose=False, **kwargs):
        """
        Byte Scaling Module

        ByteScaling performs scaling of values in an input array, excluding NaNs,
        to fit within a specified range.

        Parameters:
        - fits_type (str): Type of FITS data to load. Either `patch` or `fulldisk`. Default is `patch`.
        - min_value (float, optional): The minimum value for scaling. If None, computed from the array.
        - max_value (float, optional): The maximum value for scaling. If None, computed from the array.
        - scaler (float, optional): The scaling factor. Default is 255.
        - verbose (bool, optional): If True, enable verbose logging. Default is False.
        - **kwargs: Additional keyword arguments.

        Basic Example:
        
        # Create an instance of the transformer
        transformer = ByteScaling()
        # Load a sample magnetogram
        magnetogram, magnetogram_header, bitmap = load_fits_data()
        # Transform the magnetogram
        transformed_magnetogram = transformer.transform(magnetogram, scale=255, rgb=True)

        """
        self.min_value = min_value
        self.max_value = max_value
        self.scaler = scaler
        self.verbose = verbose
        self.logger = VerboseLogger(verbose=self.verbose)
        self.requires_bitmap = False
        self.orient_changing = False
        self.fits_type = fits_type if checkoptions(fits_type, ["patch", "fulldisk"], 'fits_type') else None
        self.requires_header= True if self.fits_type == 'fulldisk' else False
        self.mask = None
        self.kwargs = kwargs

    def _bytscal_with_nan(self, input_array, min_value, max_value):
        """
        Perform byte scaling on the input array while preserving NaN values.

        The function scales the values in the input array (excluding NaNs) to the specified range.
        If min_value or max_value are not provided, it computes them while ignoring NaNs.

        Parameters:
        - input_array (numpy array): The input array to be scaled.
        - min_value (float, optional): The minimum value for scaling. If None, computed from the array.
        - max_value (float, optional): The maximum value for scaling. If None, computed from the array.

        Returns:
        - numpy array: The byte-scaled array with NaN values preserved.
        """
        # Check if input is a NumPy array
        checktype(input_array, np.ndarray)

        # Compute min_value and max_value if they are not provided, ignoring NaNs
        input_array = np.nan_to_num(input_array)
        if min_value is None:
            min_value = np.nanmin(input_array)
        if max_value is None:
            max_value = np.nanmax(input_array)

        # Perform byte scaling while preserving NaN values
        # Scale non-NaN values to specified range
        scaled_array = np.where(np.isnan(input_array), np.nan,
                                ((input_array - min_value) / (max_value - min_value) * self.scaler).astype(np.uint8))

        return scaled_array

    def transform(self, magnetogram, header=None, rgb=False):
        """
        Transform the input array by applying byte scaling.

        Parameters:
        - magnetogram (numpy array): The input magnetogram to be transfromed.
        - header: fits header data if fulldisk.
        - rgb (bool, optional): If True, generate RGB array. Default is False.

        Returns:
        - numpy array: The transformed (byte-scaled) array.
        """
        if self.fits_type == "fulldisk":
            if not header:
                raise NoHeaderError("Header data must be provided for fulldisk fits.")

            # magnetogram,mask = background(magnetogram, header)
            # self.mask = mask

        output_array = self._bytscal_with_nan(magnetogram, self.min_value, self.max_value)

        if rgb:
            output_array = to_rgb(output_array)

        # if self.fits_type == "fulldisk":
        #     output_array = apply_mask(output_array,self.mask)

        return output_array
