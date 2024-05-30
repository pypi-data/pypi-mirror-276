"""
Module: bitmap_cropping_transformer
Description: Contains the BitmapCropping class for cropping an AR Patch based on bitmap data.
"""

import numpy as np
from scipy.ndimage import label

from ..utils.exceptions import NoBitmapError, NoHeaderError
from ..utils.logger import VerboseLogger
from ..utils.helper import checktype, to_rgb, checkoptions, background, apply_mask
from ._byte_scaling_transformer import ByteScaling

class BitmapCropping:

    def __init__(self, fits_type='patch', verbose=False,**kwargs):
        """
        Bitmap Cropping Module

        BitmapCropping performs cropping of an Active Region (AR) Patch based on bitmap data, 
        utilizing the largest connected component in the bitmap data to determine the cropping region.
        
        Parameters:
        - fits_type (str): Type of FITS data to load. Either `patch` or `fulldisk`. Default is `patch`.
        - verbose (bool, optional): If True, enable verbose logging. Default is False.
        - **kwargs: Additional keyword arguments.

        Basic Example:
        
        # Create an instance of the transformer
        transformer = BitmapCropping()
        # Load a sample magnetogram
        magnetogram, magnetogram_header, bitmap = load_fits_data()
        # Transform the magnetogram
        transformed_magnetogram = transformer.transform(magnetogram, bitmap, scale=255, rgb=True)
        
        """
        self.verbose = verbose
        self.logger = VerboseLogger(verbose=self.verbose)
        self.requires_bitmap = True
        self.orient_changing = False
        self.fits_type = fits_type if checkoptions(fits_type, ["patch", "fulldisk"], 'fits_type') else None
        self.requires_header= True if self.fits_type == 'fulldisk' else False
        self.mask = None
        self.kwargs = kwargs

    def _bitmap_cropping(self, AR_patch, bitmap_data):
        """
        Crop the AR Patch based on the largest connected component in the bitmap data.

        The function thresholds the bitmap data to identify regions of interest,
        handles NaN values, finds the largest connected component, and crops the AR Patch accordingly.

        Parameters:
        - AR_Patch (numpy array): The input Active Region patch to be cropped.
        - bitmap_data (numpy array): The bitmap data used to identify the cropping region.

        Returns:
        - numpy array: The cropped region of the AR Patch.
        """
        # Check if input AR_patch and bitmap_data are NumPy arrays
        checktype(AR_patch, np.ndarray)
        checktype(bitmap_data, np.ndarray)

        # Check for NaN values in the bitmap data and create a mask
        nan_mask = np.isnan(bitmap_data)

        # Threshold the bitmap data to binary values (0s and 1s)
        bitmap_data = (bitmap_data > 2).astype(np.uint8)

        # Exclude regions with NaN values from the binary bitmap
        bitmap_data[nan_mask] = 0

        # Label the connected components in the updated bitmap
        labels, num_features = label(bitmap_data)

        # Calculate the sizes of each connected component
        component_sizes = np.bincount(labels.ravel())

        # Find the label of the largest component (excluding the background component)
        largest_component_label = np.argmax(component_sizes[1:]) + 1

        # Find the coordinates of the largest component
        largest_component_coords = np.argwhere(labels == largest_component_label)

        # Get the minimum and maximum coordinates of the largest component
        min_x, min_y = largest_component_coords.min(axis=0)
        max_x, max_y = largest_component_coords.max(axis=0)

        # Crop the AR Patch to the region defined by the largest component
        cropped_magnetogram = AR_patch[min_x:max_x + 1, min_y:max_y + 1]

        return cropped_magnetogram

    def transform(self, magnetogram, header=None, bitmap=None, rgb=False, scale=None):
        """
        Transform the input AR Patch by cropping based on bitmap data.

        Parameters:
        - magnetogram (numpy array): The input magnetogram to be transfromed.
        - header: fits header data if fulldisk.
        - bitmap (numpy array): The bitmap data used to identify the cropping region.
        - rgb (bool, optional): If True, generate RGB array. Default is False.
        - scale (float, optional): Scaling factor applied to the output array.


        Returns:
        - numpy array: The transformed (cropped) region of the AR Patch.
        """
        if self.fits_type == "fulldisk":
            if not header:
                raise NoHeaderError("Header data must be provided for fulldisk fits.")

            magnetogram,mask = background(magnetogram, header)
            self.mask = mask

        if bitmap is None:
            raise NoBitmapError("Bitmap data must be provided for transformations that require bitmap data.")

        output_array = self._bitmap_cropping(magnetogram, bitmap)

        if scale is not None:
            output_array = ByteScaling(scaler=scale).transform(output_array)

        if rgb:
            output_array = to_rgb(output_array)

        if self.fits_type == "fulldisk":
            output_array = apply_mask(output_array,self.mask)

        return output_array
