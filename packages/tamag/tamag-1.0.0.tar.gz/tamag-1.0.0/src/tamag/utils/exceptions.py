"""
Module: exceptions
Description: Contains custom exceptions for this package.
"""

class NoBitmapError(Exception):
    """
    Exception raised when there is no bitmap available for a transformation that requires bitmap data.
    """
    pass

class NoHeaderError(Exception):
    """
    Exception raised when there is no header available for a transformation that requires header.
    """
    pass

class PipelineExecutionError(Exception):
    """
    Exception raised when there is an error while executing a transformer within a pipeline.
    """
    pass

class NullOutputError(Exception):
    """
    Exception raised when there is a transformer return None.
    """
    pass

class InvalidOutputSizeError(Exception):
    """
    Custom exception for handling cases where the `output_size` parameter is invalid.
    """
    pass

class RGBScaleError(Exception):
    """
    Custom exception for RGB scale exceeding.
    """
    pass

class InformationLossWarning(UserWarning):
    """
    Warning raised when there is potential information loss during a transformation.
    """
    pass

class NullOutputWarning(UserWarning):
    """
    Warning raised when there is a transformer return None.
    """
    pass

class PipelineExecutionWarning(UserWarning):
    """
    Warning raised when there is an error while executing a transformer within a pipeline.
    """
    pass

class MixedFitsTypeError(Exception):
    """
    Exception raised when transformers in pipeline have mixed fitstype.
    """
    pass