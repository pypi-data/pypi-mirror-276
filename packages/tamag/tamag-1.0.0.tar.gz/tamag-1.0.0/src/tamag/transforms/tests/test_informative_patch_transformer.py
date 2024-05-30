import unittest
import numpy as np
from tamag.transforms import InformativePatchTransformer

class TestInformativePatchTransformer(unittest.TestCase):
    def test_informative_patch_transformer_default(self):
        transformer = InformativePatchTransformer()
        input_array = np.random.rand(512, 512)  # Example input array

        # Ensure the output shape is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, (512, 512))

    def test_informative_patch_transformer_custom_values(self):
        transformer = InformativePatchTransformer(patch_size=256, stride=2)
        input_array = np.random.rand(256, 256)  # Another example input array

        # Ensure the output shape is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, (256, 256))

    def test_informative_patch_transformer_small_input(self):
        transformer = InformativePatchTransformer()
        input_array = np.random.rand(100, 100)  # Example input array smaller than patch_size

        # Ensure the output shape is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, (1024, 1024))

    def test_informative_patch_transformer_error_handling(self):
        transformer = InformativePatchTransformer()
        input_array = "not_a_numpy_array"  # Invalid input (not a NumPy array)

        # Ensure a TypeError is raised for invalid input
        with self.assertRaises(TypeError):
            transformer.transform(input_array)

if __name__ == '__main__':
    unittest.main()
