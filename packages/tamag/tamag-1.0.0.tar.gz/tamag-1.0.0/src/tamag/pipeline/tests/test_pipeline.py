import unittest
import numpy as np
from tamag.transforms import *
from tamag.pipeline import Pipeline
from tamag.utils.exceptions import PipelineExecutionError,NoBitmapError,NoHeaderError

class TestPreprocessingPipeline(unittest.TestCase):

    # def test_transform_with_bitmap_data(self):
    #     # Create sample input data
    #     input_array = np.random.rand(512, 512)
    #     # Create sample bitmap data
    #     bitmap_data = np.random.randint(0, 2, size=(512, 512))
    #     # Create an instance of the Pipeline with transformers
    #     pipeline = Pipeline(steps=[BitmapCropping(), FluxGuided()])
    #     # Perform the transformation
    #     transformed_array = pipeline.transform(input_array, bitmap_data=bitmap_data)
    #     # Add your assertions here based on the expected output
    #     self.assertTrue(isinstance(transformed_array, np.ndarray))  # Example assertion

    def test_transform_without_bitmap_data(self):
        # Create sample input data
        input_array = np.random.rand(512, 512)
        # Create an instance of the Pipeline with transformers
        pipeline = Pipeline(steps=[FluxGuided()])
        # Perform the transformation
        transformed_array = pipeline.transform(input_array)
        # Add your assertions here based on the expected output
        self.assertTrue(isinstance(transformed_array, np.ndarray))  # Example assertion

    def test_mulitple_transform_without_bitmap_data(self):
        # Create sample input data
        input_array = np.random.rand(512, 512)
        bitmap_data = np.random.rand(512, 512)
        # Create an instance of the Pipeline with transformers
        pipeline = Pipeline(steps=[
            Denoise(lower_bound=-20, upper_bound=20),
            BitmapCropping(),
            FluxGuided(),
            Pad(),
            Flip(),
            GaussianBlur(),
            PolarityInversion(),
            Rotate(),
            RandomNoise(),
            ResizeByHalf(),
            ByteScaling(),
            HistogramEqualization()
            ])
        # Perform the transformation
        transformed_array = pipeline.transform(input_array,bitmap_data)
        # Add your assertions here based on the expected output
        self.assertTrue(isinstance(transformed_array, np.ndarray))  # Example assertion

    def test_transform_with_invalid_bitmap_data(self):
        # Create sample input data
        input_array = np.random.rand(512, 512)
        # Create invalid bitmap data (not a NumPy array)
        invalid_bitmap_data = "not_a_numpy_array"
        # Create an instance of the Pipeline with transformers
        pipeline = Pipeline(steps=[BitmapCropping(), FluxGuided()], on_error="raise")
        # Ensure a PipelineExecutionError is raised for invalid bitmap data
        with self.assertRaises(PipelineExecutionError):
            transformed_array = pipeline.transform(input_array, bitmap_data=invalid_bitmap_data)

    def test_transform_requires_bitmap_without_bitmap_data(self):
        # Create sample input data
        input_array = np.random.rand(512, 512)
        # Create an instance of the Pipeline with transformers
        pipeline = Pipeline(steps=[BitmapCropping()])
        # Ensure a NoBitmapError is raised for invalid bitmap data
        with self.assertRaises(NoBitmapError):
            transformed_array = pipeline.transform(input_array)

    def test_transform_fulldisk_without_header(self):
        # Create sample input data
        input_array = np.random.rand(512, 512)
        # Create an instance of the Pipeline with transformers
        pipeline = Pipeline(steps=[Pad()])
        # Ensure a NoHeaderError is raised for invalid bitmap data
        with self.assertRaises(NoHeaderError):
            transformed_array = pipeline.transform(input_array,fulldisk=True)

if __name__ == '__main__':
    unittest.main()
