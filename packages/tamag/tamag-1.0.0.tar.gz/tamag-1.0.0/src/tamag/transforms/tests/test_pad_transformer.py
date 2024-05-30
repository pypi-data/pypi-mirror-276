# test_padding_transformer.py
import unittest
import numpy as np
from tamag.transforms import PadTransformer

class TestPadTransformer(unittest.TestCase):
    def test_padding_transformer_default(self):
        transformer = PadTransformer()
        input_array = np.ones((512, 512))  # Example input array

        # Ensure the output size is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, (1024, 1024))

        # Ensure padding values are correct
        self.assertEqual(result[0, 0], 0)  # Top-left corner should be padded with 0

    def test_padding_transformer_custom_values(self):
        transformer = PadTransformer(constant_value=255, output_size=2048)
        input_array = np.zeros((256, 256))  # Another example input array

        # Ensure the output size is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, (2048, 2048))

        # Ensure padding values are correct
        self.assertEqual(result[0, 0], 255)  # Top-left corner should be padded with 255

    def test_padding_transformer_use_max_dimension(self):
        transformer = PadTransformer(use_max_dimension=True)
        input_array = np.random.rand(300, 400)  # Yet another example input array

        # Ensure the output size is correct (using the maximum dimension)
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, (1024, 1024))

    def test_padding_transformer_error_handling(self):
        transformer = PadTransformer()
        input_array = "not_a_numpy_array"  # Invalid input (not a NumPy array)

        # Ensure an exception is raised for invalid input
        with self.assertRaises(TypeError):
            transformer.transform(input_array)

if __name__ == '__main__':
    unittest.main()
