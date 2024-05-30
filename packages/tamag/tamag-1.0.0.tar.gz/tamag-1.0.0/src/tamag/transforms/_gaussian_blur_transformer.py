"""
Module: gaussian_blur_transformer
Description: Contains the GaussianBlur module for applying Gaussian blurring to a magnetogram map.
"""

import numpy as np
from scipy.ndimage import gaussian_filter
from ..utils.helper import checktype, to_rgb, checkoptions, background, apply_mask
from ..utils.logger import VerboseLogger
from ..utils.exceptions import NoHeaderError
from ._byte_scaling_transformer import ByteScaling

class GaussianBlur:

    def __init__(self, fits_type='patch', sigma=10, verbose=False,  **kwargs):
        """
        Gaussian Blur Module

        GaussianBlur applies Gaussian blurring to a magnetogram map. Utilizing a Gaussian kernel, 
        the extent of blurring is determined by the 'sigma' value. A higher sigma value leads to more pronounced blurring.
        
        Parameters:
        - fits_type (str): Type of FITS data to load. Either `patch` or `fulldisk`. Default is `patch`.
        - sigma (float, optional): The standard deviation of the Gaussian kernel. Default is 10.
        - verbose (bool, optional): If True, enable verbose logging. Default is False.
        - **kwargs: Additional keyword arguments.

        Basic Example:
        
        # Create an instance of the transformer
        transformer = GaussianBlur()
        # Load a sample magnetogram
        magnetogram, magnetogram_header, bitmap = load_fits_data()
        # Transform the magnetogram
        transformed_magnetogram = transformer.transform(magnetogram, scale=255, rgb=True)

        """
        self.sigma = sigma
        self.verbose = verbose
        self.logger = VerboseLogger(verbose=self.verbose)
        self.requires_bitmap = False
        self.orient_changing = False
        self.fits_type = fits_type if checkoptions(fits_type, ["patch", "fulldisk"], 'fits_type') else None
        self.requires_header= True if self.fits_type == 'fulldisk' else False
        self.mask = None
        self.kwargs = kwargs

    def _gaussian_blur(self, magnetogram, sigma):
        """
        Apply Gaussian blurring to a magnetogram map.

        This function uses a Gaussian kernel for blurring, where 'sigma' determines the extent of blurring.

        Parameters:
        - magnetogram (numpy array): The magnetogram map to be blurred.
        - sigma (float): The standard deviation of the Gaussian kernel.

        Returns:
        - numpy array: The blurred magnetogram map.
        """
        # Check if input is a NumPy array
        checktype(magnetogram, np.ndarray)

        # Apply Gaussian blurring using the specified sigma value
        blurred_magnetogram = gaussian_filter(magnetogram, sigma=sigma)
        return blurred_magnetogram

    def transform(self, magnetogram, header=None, rgb=False, scale=None):
        """
        Transform the input magnetogram by applying Gaussian blurring.

        Parameters:
        - magnetogram (numpy array): The input magnetogram to be transfromed.
        - header: fits header data if fulldisk.
        - rgb (bool, optional): If True, generate RGB array. Default is False.
        - scale (float, optional): Scaling factor applied to the output array.

        Returns:
        - numpy array: The blurred magnetogram map.
        """
        if self.fits_type == "fulldisk":
            if not header:
                raise NoHeaderError("Header data must be provided for fulldisk fits.")

            magnetogram,mask = background(magnetogram, header)
            self.mask = mask

        output_array = self._gaussian_blur(magnetogram, self.sigma)

        if scale is not None:
            output_array = ByteScaling(scaler=scale).transform(output_array)

        if rgb:
            output_array = to_rgb(output_array)

        if self.fits_type == "fulldisk":
            output_array = apply_mask(output_array,self.mask)

        return output_array 
