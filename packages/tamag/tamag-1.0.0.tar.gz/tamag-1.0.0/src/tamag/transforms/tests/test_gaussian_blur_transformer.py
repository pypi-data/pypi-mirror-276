import unittest
import numpy as np
from tamag.transforms import GaussianBlurTransformer

class TestGaussianBlurTransformer(unittest.TestCase):
    def test_gaussian_blur_transformer_default(self):
        transformer = GaussianBlurTransformer()
        input_array = np.random.rand(512, 512)  # Example input array

        # Ensure the output shape is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, (512, 512))

    def test_gaussian_blur_transformer_custom_sigma(self):
        transformer = GaussianBlurTransformer(sigma=5)
        input_array = np.random.rand(256, 256)  # Another example input array

        # Ensure the output shape is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, (256, 256))

    def test_gaussian_blur_transformer_error_handling(self):
        transformer = GaussianBlurTransformer()
        input_array = "not_a_numpy_array"  # Invalid input (not a NumPy array)

        # Ensure a TypeError is raised for invalid input
        with self.assertRaises(TypeError):
            transformer.transform(input_array)

if __name__ == '__main__':
    unittest.main()
