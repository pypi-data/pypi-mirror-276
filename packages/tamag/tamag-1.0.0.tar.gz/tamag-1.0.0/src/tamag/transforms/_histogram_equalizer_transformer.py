"""
Module Name: histogram_equalization_transformer.py
Description: This module contains the HistogramEqualization module, which is a transformer for applying histogram equalization to a magnetogram map.
"""

import numpy as np
from ..utils.logger import VerboseLogger
from ..utils.helper import checktype,to_rgb,checkoptions,background, apply_mask
from ..utils.exceptions import NoHeaderError
from ._byte_scaling_transformer import ByteScaling

class HistogramEqualization:

    def __init__(self, fits_type='patch', bins=256, range=[0, 256], verbose=False, **kwargs):
        """
        Histogram Equalization Module

        HistogramEqualization enhances the contrast of a magnetogram map through the application of histogram equalization. 
        The module redistributes intensity values, promoting improved visual contrast in the magnetogram.

        Args:
        - fits_type (str): Type of FITS data to load. Either `patch` or `fulldisk`. Default is `patch`.
        - bins (int): Number of bins in the histogram. Default is 256.
        - range (list): Range of intensity values for the histogram. Default is [0, 256].
        - verbose (bool): If True, display verbose output during transformation. Default is False.
        - **kwargs: Additional keyword arguments for future expansion.

        Basic Example:
        
        # Create an instance of the transformer
        transformer = HistogramEqualization()
        # Load a sample magnetogram
        magnetogram, magnetogram_header, bitmap = load_fits_data()
        # Transform the magnetogram
        transformed_magnetogram = transformer.transform(magnetogram, scale=255, rgb=True)

        """
        self.bins = bins
        self.range = range
        self.verbose = verbose
        self.logger = VerboseLogger(verbose=self.verbose)
        self.requires_bitmap = False
        self.orient_changing = False
        self.fits_type = fits_type if checkoptions(fits_type, ["patch", "fulldisk"], 'fits_type') else None
        self.requires_header= True if self.fits_type == 'fulldisk' else False
        self.mask = None
        self.kwargs = kwargs

    def _histogram_equalization(self, magnetogram, bins, range):
        """
        Apply histogram equalization to a magnetogram map using NumPy.

        Args:
        - magnetogram (numpy array): The magnetogram map to be enhanced.

        Returns:
        - numpy array: The contrast-enhanced magnetogram map.
        """

        # Check if input is a NumPy array
        checktype(magnetogram, np.ndarray)

        # Flatten the image to 1D array for histogram computation
        flat_magnetogram = magnetogram.flatten()

        # Calculate the histogram
        histogram, bins = np.histogram(flat_magnetogram, bins, range, density=True)

        # Compute the cumulative distribution function (CDF)
        cdf = histogram.cumsum()
        cdf_normalized = cdf * 255 / cdf[-1]  # Normalize the CDF

        # Use linear interpolation of CDF to find new pixel values
        equalized_magnetogram = np.interp(flat_magnetogram, bins[:-1], cdf_normalized)

        return equalized_magnetogram.reshape(magnetogram.shape)

    def transform(self, magnetogram, header=None, rgb=False, scale=None):
        """
        Apply histogram equalization transformation to a magnetogram.

        Args:
        - magnetogram (numpy array): The input magnetogram to be transfromed.
        - header: fits header data if fulldisk.
        - rgb (bool, optional): If True, generate RGB array. Default is False.
        - scale (float, optional): Scaling factor applied to the output array.

        Returns:
        - numpy array: The transformed magnetogram map with enhanced contrast.
        """
        if self.fits_type == "fulldisk":
            if not header:
                raise NoHeaderError("Header data must be provided for fulldisk fits.")

            magnetogram,mask = background(magnetogram, header)
            self.mask = mask

        output_array = self._histogram_equalization(magnetogram, self.bins, self.range)

        if scale is not None:
            output_array = ByteScaling(scaler=scale).transform(output_array)

        if rgb:
            output_array = to_rgb(output_array)

        if self.fits_type == "fulldisk":
            output_array = apply_mask(output_array,self.mask)

        return output_array 