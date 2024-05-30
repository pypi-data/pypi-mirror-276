"""
Module: denoise_transformer
Description: Contains the Denoise module for denoising an active region patch.
"""

import numpy as np
from ..utils.logger import VerboseLogger
from ..utils.exceptions import NoHeaderError
from ..utils.helper import checktype, to_rgb, checkoptions, apply_mask, background
from ._byte_scaling_transformer import ByteScaling

class Denoise:

    def __init__(self, fits_type='patch', lower_bound=-50, upper_bound=50, maximum_range=256, verbose=False, **kwargs):
        """
        Denoise Module

        Denoise enhances the quality of an active region patch by employing denoising techniques. 
        It constrains the values of the active region patch within a defined range and subsequently
        eliminates values falling below a specified noise threshold.
        
        Parameters:
        - fits_type (str): Type of FITS data to load. Either `patch` or `fulldisk`. Default is `patch`.
        - lower_bound (int): The lower bound of the noise threshold. Default is -50.
        - upper_bound (int): The upper bound of the noise threshold. Default is 50.
        - maximum_range (int, optional): The maximum range for clipping values. Default is 256.
        - verbose (bool, optional): If True, enable verbose logging. Default is False.
        
        Basic Example:
        
        # Create an instance of the transformer
        transformer = Denoise()
        # Load a sample magnetogram
        magnetogram, magnetogram_header, bitmap = load_fits_data()
        # Transform the magnetogram
        transformed_magnetogram = transformer.transform(magnetogram, scale=255, rgb=True)

        """
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.maximum_range = maximum_range
        self.verbose = verbose
        self.logger = VerboseLogger(verbose=self.verbose)
        self.requires_bitmap = False
        self.orient_changing = False
        self.fits_type = fits_type if checkoptions(fits_type, ["patch", "fulldisk"], 'fits_type') else None
        self.requires_header= True if self.fits_type == 'fulldisk' else False
        self.mask = None
        self.kwargs = kwargs


    def _denoise(self, input, lower_bound, upper_bound, maximum_range, mask=None):
        """
        Denoise the active region patch.

        This function first limits the values of the active region patch to a default specified range (-256, 256).
        Then, it sets values within the noise threshold (lower_bound, upper_bound) to zero.

        Args:
        - input (numpy array): The input Active Region (AR) patch or fulldisk data.
        - lower_bound (int): The lower bound of the noise threshold.
        - upper_bound (int): The upper bound of the noise threshold.
        - maximum_range (int, optional): The maximum range for clipping values. Default is 256.
        Returns:
        - numpy array: The denoised Active Region patch.
        """

        # Check if input is a NumPy array
        checktype(input,np.ndarray)

        # Clip the active region patch values to the range [-maximum_range, maximum_range]
        clipped_patch = np.clip(input, -1 * maximum_range, maximum_range)

        # Identify values outside the noise threshold range
        outside_noise_threshold = np.logical_or(clipped_patch < lower_bound, clipped_patch > upper_bound)

        # Set the values within the noise threshold to zero
        denoised = np.where(outside_noise_threshold, clipped_patch, float(0))

        return denoised

    def transform(self, magnetogram, header=None, rgb=False, scale=None):
        """
        Transform the input active region patch by denoising.

        Parameters:
        - magnetogram (numpy array): The input magnetogram to be transfromed.
        - header: fits header data if fulldisk.
        - rgb (bool, optional): If True, generate RGB array. Default is False.
        - scale (float, optional): Scaling factor applied to the output array.


        Returns:
        - numpy array: The denoised Active Region patch.
        """

        if self.fits_type == "fulldisk":
            if not header:
                raise NoHeaderError("Header data must be provided for fulldisk fits.")

            magnetogram,mask = background(magnetogram, header)
            self.mask = mask

            output_array =  self._denoise(magnetogram, self.lower_bound, self.upper_bound, self.maximum_range,mask=self.mask)
        
        elif self.fits_type == "patch":
            output_array =  self._denoise(magnetogram, self.lower_bound, self.upper_bound, self.maximum_range)
        
        if scale is not None:
            output_array = ByteScaling(scaler=scale).transform(output_array)
        if rgb:
            output_array = to_rgb(output_array)

        if self.fits_type == "fulldisk":
            output_array = apply_mask(output_array,self.mask)

        return output_array

