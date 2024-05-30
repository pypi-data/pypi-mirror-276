"""
Module: resize_by_half_transformer
Description: Contains the ResizeByHalf module for resizing a 2D numpy array to half of its original size.
"""

import numpy as np
from ..utils.logger import VerboseLogger
from ..utils.helper import checktype, to_rgb, checkoptions, background, apply_mask
from  ..utils.exceptions import NoHeaderError
from ._byte_scaling_transformer import ByteScaling

class ResizeByHalf:

    def __init__(self, fits_type='patch', verbose=False, **kwargs):
        """
        Resize By Half Module

        ResizeByHalf modifies a 2D numpy array by reducing its size to half of the original dimensions. 
        The transformation achieves the resizing by employing average pooling on the image.
        
        Parameters:
        - fits_type (str): Type of FITS data to load. Either `patch` or `fulldisk`. Default is `patch`.
        - verbose (bool, optional): If True, enable verbose logging. Default is False.
        - **kwargs: Additional keyword arguments.

        Basic Example:
        
        # Create an instance of the transformer
        transformer = ResizeByHalf()
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

    def _resize_by_half(self, x):
        """
        Resize a 2D numpy array to half of its original size using average pooling.

        Parameters:
        - x (numpy array): A 2D numpy array representing an image.

        Returns:
        - numpy array: The resized array.
        """
        # Ensure input is a NumPy array
        checktype(x,np.ndarray)

        # Determine the current height and width
        h, w = x.shape

        # Calculate new dimensions, ensuring they are even
        new_h = h // 2
        new_w = w // 2

        # Truncate the array to make sure the size is a multiple of 2
        truncated_x = x[:new_h * 2, :new_w * 2]

        # Perform average pooling to downsample the image
        resized_x = truncated_x.reshape((new_h, 2, new_w, 2)).mean(axis=(1, 3))

        return resized_x

    def transform(self, magnetogram, header=None, rgb=False, scale=None):
        """
        Transform the input 2D numpy array by resizing it to half of its original size.

        Parameters:
        - magnetogram (numpy array): The input magnetogram to be transfromed.
        - header: fits header data if fulldisk.
        - rgb (bool, optional): If True, generate RGB array. Default is False.
        - scale (float, optional): Scaling factor applied to the output array.

        Returns:
        - numpy array: The resized 2D numpy array.
        """
        if self.fits_type == "fulldisk":
            raise NotImplementedError("Method not Implemented for fulldisk fits")
            if not header:
                raise NoHeaderError("Header data must be provided for fulldisk fits.")

            magnetogram,mask = background(magnetogram, header)
            self.mask = mask

        output_array = self._resize_by_half(magnetogram)

        if scale is not None:
            output_array = ByteScaling(scaler=scale).transform(output_array)

        if rgb:
            output_array = to_rgb(output_array)

        if self.fits_type == "fulldisk":
            output_array = apply_mask(output_array,self.mask)
            
        return output_array

