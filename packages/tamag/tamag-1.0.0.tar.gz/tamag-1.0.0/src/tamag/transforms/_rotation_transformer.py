"""
Module: rotate_transformer
Description: Contains the Rotate class for rotating a magnetogram map by a specified angle.
"""

import numpy as np
from scipy.ndimage import rotate
from ..utils.exceptions import InformationLossWarning, NoHeaderError
from ..utils.logger import VerboseLogger
from ..utils.helper import calculate_information_loss, checktype, to_rgb, checkoptions, background, apply_mask
from ._byte_scaling_transformer import ByteScaling

class Rotate:

    def __init__(self, fits_type='patch', angle=45, order=3, loss_threshold=1.0, verbose=False, **kwargs):
        """
        Rotate Transformer

        Rotate facilitates the rotation of a magnetogram map by a user-specified angle. 
        The transformation is accomplished through the rotation function, enabling rotation at any angle within the range of 0 to 360 degrees.
        
        Parameters:
        - fits_type (str): Type of FITS data to load. Either `patch` or `fulldisk`. Default is `patch`.
        - angle (float, optional): The angle of rotation in degrees (0 to 360). Default is 45.
        - order (integer, optional): The rotation order. Default is 3.
        - loss_threshold (float, optional): The threshold for information loss. If the information loss exceeds this threshold, the input array will be returned. Default is 1.0.
        - verbose (bool, optional): If True, enable verbose logging. Default is False.
        - **kwargs: Additional keyword arguments.

        Basic Example:
        
        # Create an instance of the transformer
        transformer = Rotate()
        # Load a sample magnetogram
        magnetogram, magnetogram_header, bitmap = load_fits_data()
        # Transform the magnetogram
        transformed_magnetogram = transformer.transform(magnetogram, scale=255, rgb=True)

        """
        self.angle = angle
        self.order = order
        self.loss_threshold = loss_threshold
        self.verbose = verbose
        self.logger = VerboseLogger(verbose=self.verbose)
        self.requires_bitmap = False
        self.orient_changing = True
        self.fits_type = fits_type if checkoptions(fits_type, ["patch", "fulldisk"], 'fits_type') else None
        self.requires_header= True if self.fits_type == 'fulldisk' else False
        self.mask = None
        self.kwargs = kwargs

    def _rotate(self, input, order, angle):
        """
        Rotate the input map by a specified angle.

        Parameters:
        - input (numpy array): The input map to be rotated.
        - order (integer, optional): The rotation order. Default is 3.
        - angle (float, optional): The angle of rotation in degrees (0 to 360). Default is 45.

        Returns:
        - numpy array: The rotated input map.
        """
        # Check if input is a NumPy array
        checktype(input,np.ndarray)

        # Rotate the magnetogram and return the result
        return rotate(input, angle, order=order, reshape=False, mode='nearest')

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

        if np.count_nonzero(np.isnan(magnetogram)):
            self.order = 0

        output_array = self._rotate(magnetogram, self.order, self.angle)

        information_loss = calculate_information_loss(magnetogram, output_array)

        if information_loss > self.loss_threshold:
            warning_msg = f"Skipping Rotate due to information loss ({information_loss}) exceeding threshold ({self.loss_threshold})."
            self.logger.warn(warning_msg,InformationLossWarning)

            return magnetogram

        if scale is not None:
            output_array = ByteScaling(scaler=scale).transform(output_array)

        if rgb:
            output_array = to_rgb(output_array,self.mask)

        if self.fits_type == "fulldisk":
            output_array = apply_mask(output_array,self.mask)

        return output_array

