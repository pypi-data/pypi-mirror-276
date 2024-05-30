"""
Module: flip_transformer
Description: Contains the Flip Module class for flipping a magnetogram map either horizontally or vertically.
"""

import numpy as np
from ..utils.logger import VerboseLogger
from ..utils.exceptions import InformationLossWarning, NoHeaderError
from ..utils.helper import checktype,calculate_information_loss,to_rgb, checkoptions, background, apply_mask
from ._byte_scaling_transformer import ByteScaling

class Flip:

    def __init__(self, fits_type='patch', direction='horizontal', loss_threshold=1.0, verbose=False, **kwargs):
        """
        Flip Module

        Flip modifies a magnetogram map by flipping it either horizontally or vertically. 
        It encapsulates the logic for flipping the magnetogram based on a specified direction, 
        which can be either 'horizontal' or 'vertical'.
        
        Parameters:
        - fits_type (str): Type of FITS data to load. Either `patch` or `fulldisk`. Default is `patch`.
        - direction (str, optional): The direction of the flip. Should be either 'horizontal' or 'vertical'. Default is 'horizontal'.
        - loss_threshold (float, optional): The threshold for information loss. If the information loss exceeds this threshold, the input array will be returned. Default is 1.0.
        - verbose (bool, optional): If True, enable verbose logging. Default is False.
        - **kwargs: Additional keyword arguments.

        Basic Example:
        
        # Create an instance of the transformer
        transformer = Flip()
        # Load a sample magnetogram
        magnetogram, magnetogram_header, bitmap = load_fits_data()
        # Transform the magnetogram
        transformed_magnetogram = transformer.transform(magnetogram, scale=255, rgb=True)

        """

        self.validoptions = ["horizontal", "vertical"]
        self.direction = direction if checkoptions(direction, self.validoptions, "direction") else None
        self.verbose = verbose
        self.loss_threshold = loss_threshold
        self.logger = VerboseLogger(verbose=self.verbose)
        self.requires_bitmap = False
        self.orient_changing = True
        self.fits_type = fits_type if checkoptions(fits_type, ["patch", "fulldisk"], 'fits_type') else None
        self.requires_header= True if self.fits_type == 'fulldisk' else False
        self.mask = None
        self.kwargs = kwargs

    def _flip(self, input, direction):
        """
        Flip an input map either horizontally or vertically.

        Parameters:
        - input (numpy array): The input map to be flipped.
        - direction (str, optional): The direction of the flip. Should be either 'horizontal' or 'vertical'. Default is 'horizontal'.

        Returns:
        - numpy array: The flipped input map.
        """

        # Check if input is a NumPy array
        checktype(input,np.ndarray)

        if direction.lower() == 'horizontal':
            # Flip the magnetogram horizontally
            return np.fliplr(input)
        elif direction.lower() == 'vertical':
            # Flip the magnetogram vertically
            return np.flipud(input)


    def transform(self, magnetogram, header=None, rgb=False, scale=None):
        """
        Transform the magnetogram/bitmap_data.

        Parameters:
        - magnetogram (numpy array): The input magnetogram to be transfromed.
        - header: fits header data if fulldisk.
        - rgb (bool, optional): If True, generate RGB array. Default is False.
        - scale (float, optional): Scaling factor applied to the output array.

        Returns:
        - Tuple[numpy array]: The transformed magnetogram/bitmap_data.
        """
        if self.fits_type == "fulldisk":
            if not header:
                raise NoHeaderError("Header data must be provided for fulldisk fits.")

            magnetogram,mask = background(magnetogram, header)
            self.mask = mask

        output_array = self._flip(magnetogram, self.direction)

        information_loss = calculate_information_loss(magnetogram, output_array)

        if information_loss > self.loss_threshold:
            warning_msg = f"Skipping Flip due to information loss ({information_loss}) exceeding threshold ({self.loss_threshold})."
            self.logger.warn(warning_msg,InformationLossWarning)

            return magnetogram

        if scale is not None:
            output_array = ByteScaling(scaler=scale).transform(output_array)

        if rgb:
            output_array = to_rgb(output_array)

        if self.fits_type == "fulldisk":
            output_array = apply_mask(output_array,self.mask)

        return output_array


