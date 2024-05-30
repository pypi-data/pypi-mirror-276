"""
Module: invert_polarity_transformer
Description: Contains the PolarityInversion module for inverting the polarity of a magnetogram map.
"""

import numpy as np
from ..utils.helper import checktype,to_rgb,checkoptions,background,apply_mask
from ..utils.logger import VerboseLogger
from ..utils.exceptions import NoHeaderError
from ._byte_scaling_transformer import ByteScaling

class PolarityInversion:

    def __init__(self, fits_type='patch', verbose=False, **kwargs):
        """
        PolarityInversion Module

        PolarityInversion reverses the polarity of a magnetogram map by multiplying all values in the magnetogram by -1.
        This transformation effectively flips the direction of the magnetic field lines.
        
        Parameters:
        - fits_type (str): Type of FITS data to load. Either `patch` or `fulldisk`. Default is `patch`.
        - verbose (bool, optional): If True, enable verbose logging. Default is False.
        - **kwargs: Additional keyword arguments.

        Basic Example:
        
        # Create an instance of the transformer
        transformer = PolarityInversion()
        # Load a sample magnetogram
        magnetogram, magnetogram_header, bitmap = load_fits_data()
        # Transform the magnetogram
        transformed_magnetogram = transformer.transform(magnetogram, scale=255, rgb=True)
        """
        self.verbose = verbose
        self.logger = VerboseLogger(verbose=self.verbose)
        self.requires_bitmap = False
        self.orient_changing = False
        self.fits_type = fits_type if checkoptions(fits_type, ["patch", "fulldisk"], 'fits_type') else None
        self.requires_header= True if self.fits_type == 'fulldisk' else False
        self.mask = None
        self.kwargs = kwargs

    def _invert_polarity(self, magnetogram):
        """
        Invert the polarity of a magnetogram map.

        This function multiplies all the values in the magnetogram map by -1,
        effectively reversing the direction of the magnetic field lines.

        Parameters:
        - magnetogram (numpy array): The magnetogram map whose polarity is to be inverted.

        Returns:
        - numpy array: The polarity-inverted magnetogram map.
        """
        # Check if input is a NumPy array
        checktype(magnetogram, np.ndarray)

        # Invert the polarity by multiplying by -1
        inverted_magnetogram = magnetogram * -1

        return inverted_magnetogram

    def transform(self, magnetogram, header=None, rgb=False, scale=None):
        """
        Transform the input magnetogram by inverting its polarity.

        Parameters:
        - magnetogram (numpy array): The input magnetogram to be transfromed.
        - header: fits header data if fulldisk.
        - rgb (bool, optional): If True, generate RGB array. Default is False.
        - scale (float, optional): Scaling factor applied to the output array.

        Returns:
        - numpy array: The polarity-inverted magnetogram map.
        """

        if self.fits_type == "fulldisk":
            if not header:
                raise NoHeaderError("Header data must be provided for fulldisk fits.")

            magnetogram,mask = background(magnetogram, header)
            self.mask = mask

        output_array = self._invert_polarity(magnetogram)

        if scale is not None:
            output_array = ByteScaling(scaler=scale).transform(output_array)

        if rgb:
            output_array = to_rgb(output_array)

        if self.fits_type == "fulldisk":
            output_array = apply_mask(output_array,self.mask)

        return output_array

