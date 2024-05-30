"""
Module: informative_patch_transformer
Description: Contains the FluxGuided class for finding the best patch in an image using a stride-based approach.
"""

import numpy as np
from . import Pad
from ..utils.logger import VerboseLogger
from ..utils.helper import checktype,to_rgb,checkoptions,background,apply_mask
from ._byte_scaling_transformer import ByteScaling
from ..utils.exceptions import NullOutputError,NullOutputWarning,NoHeaderError

class FluxGuided:

    def __init__(self, fits_type='patch', patch_size=512, stride=10, constant_value=0, output_size=1024, infer_output_size=False, on_null_output="ignore", verbose=False, **kwargs):
        """
       Flux Guided Module

        FluxGuided Module identifies the optimal patch within an image employing a stride-based approach. 
        This module is designed to locate the most informative patch within the input image.
        
        Parameters:
        - fits_type (str): Type of FITS data to load. Either `patch` or `fulldisk`. Default is `patch`.
        - patch_size (int, optional): The size of the patch. Default is 512.
        - stride (int, optional): The stride for computing patches. Default is 10.
        - constant_value (float, optional): The constant value for padding. Default is 0.
        - output_size (int, optional): The output size after padding. Default is 1024.
        - infer_output_size (bool, optional): If True, the output size is automatically inferred based on the maximum dimension of the original array. Default is False.
        - on_null_output (str, optional): Define the behavior when a transformer returns None.
            - "ignore": return input data and log a warning (default).
            - "raise": Raise an error if a transformer returns None.
        - verbose (bool, optional): If True, enable verbose logging. Default is False.

        Basic Example:
        
        # Create an instance of the transformer
        transformer = FluxGuided()
        # Load a sample magnetogram
        magnetogram, magnetogram_header, bitmap = load_fits_data()
        # Transform the magnetogram
        transformed_magnetogram = transformer.transform(magnetogram, scale=255, rgb=True)

        """
        self.patch_size = patch_size
        self.stride = stride
        self.validoptions = ["ignore", "raise"]
        self.on_null_output = on_null_output if checkoptions(on_null_output, self.validoptions, "on_null_output") else None
        self.verbose = verbose
        self.logger = VerboseLogger(verbose=self.verbose)
        self.requires_bitmap = False
        self.orient_changing = False
        self.fits_type = fits_type if checkoptions(fits_type, ["patch", "fulldisk"], 'fits_type') else None
        self.requires_header= True if self.fits_type == 'fulldisk' else False
        self.mask = None
        self.kwargs = kwargs
        self.padding = Pad(constant_value=constant_value, output_size=output_size, infer_output_size=infer_output_size)
  
    def _find_best_patch(self, original_array):
        """
        Find the best patch in the image using a stride-based approach.

        Args:
        - original_array (numpy array): The input image array.

        Returns:
        - numpy array: The best patch.
        """
        
        # Check if input is a NumPy array
        checktype(original_array, np.ndarray)

        original_height, original_width = original_array.shape
        best_ratio = 0
        best_patch = None

        # Check if the original array is smaller than patch_size in both dimensions
        if original_height < self.patch_size and original_width < self.patch_size:
            # If smaller, use padding to handle the case
            best_patch = self.padding.transform(original_array)

        # Check which dimension needs stride-based computation
        elif original_height < self.patch_size:
            best_patch, best_ratio = self._compute_stride(original_array, dimension='width')

        elif original_width < self.patch_size:
            best_patch, best_ratio = self._compute_stride(original_array, dimension='height')

        else:
            best_patch, best_ratio = self._compute_stride(original_array, dimension='both')

        return best_patch

    def _compute_stride(self, original_array, dimension):
        """
        Compute the best patch using a stride-based approach.

        Args:
        - original_array (numpy array): The input image array.
        - dimension (str): The dimension for stride-based computation ('width', 'height', or 'both').

        Returns:
        - numpy array: The best patch.
        - float: The best ratio.
        """
        original_height, original_width = original_array.shape
        best_ratio = 0
        best_patch = None

        if dimension == 'width':
            loop_range = range(0, original_width - self.patch_size + 1, self.stride)
            for x in loop_range:
                cropped_patch = self._crop_and_pad_patch(original_array, x=x)
                best_patch, best_ratio = self._update_best_patch(original_array, cropped_patch, best_patch, best_ratio, x=x)

        elif dimension == 'height':
            loop_range = range(0, original_height - self.patch_size + 1, self.stride)
            for y in loop_range:
                cropped_patch = self._crop_and_pad_patch(original_array, y=y)
                best_patch, best_ratio = self._update_best_patch(original_array, cropped_patch, best_patch, best_ratio, y=y)

        elif dimension == 'both':
            for y in range(0, original_height - self.patch_size + 1, self.stride):
                for x in range(0, original_width - self.patch_size + 1, self.stride):
                    cropped_patch = self._crop_and_pad_patch(original_array, x=x, y=y)
                    best_patch, best_ratio = self._update_best_patch(original_array, cropped_patch, best_patch, best_ratio, x=x, y=y)

        return best_patch, best_ratio

    def _update_best_patch(self, original_array, cropped_patch, best_patch, best_ratio, x=None, y=None):
        """
        Update the best patch based on the ratio.

        Args:
        - original_array (numpy array): The input image array.
        - cropped_patch (numpy array): The cropped patch.
        - best_patch (numpy array): The current best patch.
        - best_ratio (float): The current best ratio.
        - x (int, optional): The x-coordinate. Default is None.
        - y (int, optional): The y-coordinate. Default is None.

        Returns:
        - numpy array: The updated best patch.
        - float: The updated best ratio.
        """
        patch_sum = np.nansum(np.abs(cropped_patch))
        original_sum = np.nansum(np.abs(original_array))

        # Compute ratio while handling potential division by zero
        ratio = patch_sum / original_sum if original_sum != 0 else 0

        # Update best_patch and best_ratio if the current ratio is greater
        if (ratio - best_ratio) > 0.0:
            best_ratio = ratio
            best_patch = cropped_patch
            if x is not None and y is not None:
                self.logger.info(f"Selected patch with ratio: {best_ratio} at x={x}, y={y}")
            elif x is not None:
                self.logger.info(f"Selected patch with ratio: {best_ratio} at x={x}")
            elif y is not None:
                self.logger.info(f"Selected patch with ratio: {best_ratio} at y={y}")

        return best_patch, best_ratio

    def _crop_and_pad_patch(self, original_array, x=None, y=None):
        """
        Crop and pad the patch based on the specified coordinates.

        Args:
        - original_array (numpy array): The input image array.
        - x (int, optional): The x-coordinate. Default is None.
        - y (int, optional): The y-coordinate. Default is None.

        Returns:
        - numpy array: The cropped and padded patch.
        """
        if x is not None:
            x_start = max(0, x)
            x_end = min(original_array.shape[1], x + self.patch_size)
        else:
            x_start = 0
            x_end = original_array.shape[1]

        if y is not None:
            y_start = max(0, y)
            y_end = min(original_array.shape[0], y + self.patch_size)
        else:
            y_start = 0
            y_end = original_array.shape[0]

        # Crop the patch
        cropped_patch = original_array[y_start:y_end, x_start:x_end]

        # Calculate padding amounts
        pad_height = self.patch_size - cropped_patch.shape[0]
        pad_top = pad_height // 2
        pad_bottom = pad_height - pad_top

        pad_width = self.patch_size - cropped_patch.shape[1]
        pad_left = pad_width // 2
        pad_right = pad_width - pad_left

        # Pad the cropped_patch
        cropped_patch = np.pad(cropped_patch, ((pad_top, pad_bottom), (pad_left, pad_right)), mode='constant', constant_values=0)

        return cropped_patch

    def transform(self, magnetogram, header=None, rgb=False, scale=None):
        """
        Transform the input magnetogram by finding the best patch.

        Args:
        - magnetogram (numpy array): The input magnetogram to be transfromed.
        - header: fits header data if fulldisk.
        - rgb (bool, optional): If True, generate RGB array. Default is False.
        - scale (float, optional): Scaling factor applied to the output array.


        Returns:
        - numpy array: The transformed (best patch) magnetogram.
        """
        if self.fits_type == "fulldisk":
            raise NotImplementedError("Method not Implemented for fulldisk fits")
            if not header:
                raise NoHeaderError("Header data must be provided for fulldisk fits.")

            magnetogram,mask = background(magnetogram, header)
            self.mask = mask

        output_array = self._find_best_patch(magnetogram)

        if output_array is None:
            # Skip Transformation if on_null_output is ignore
            if self.on_null_output == "ignore":
                self.logger.warn(f"Skipping FluxGuided Transformation due to None output ", NullOutputWarning)
                output_array = magnetogram
            # Raise Exception if on_null_output is raise
            elif self.on_null_output == "raise":
                error_message = f"FluxGuided returned None. Check input data and parameters"
                raise NullOutputError(error_message)

        if scale is not None:
            output_array = ByteScaling(scaler=scale).transform(output_array)

        if rgb:
            output_array = to_rgb(output_array)

        if self.fits_type == "fulldisk":
            output_array = apply_mask(output_array,self.mask)

        return output_array 
