import unittest
import numpy as np
from tamag.transforms import InvertPolarityTransformer

class TestInvertPolarityTransformer(unittest.TestCase):
    def test_invert_polarity_transformer_default(self):
        transformer = InvertPolarityTransformer()
        input_array = np.random.rand(512, 512) * 100  # Example input array

        # Ensure the output shape is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, (512, 512))

        # Ensure values are inverted correctly
        self.assertTrue(np.all(result == -input_array))

    def test_invert_polarity_transformer_custom_values(self):
        transformer = InvertPolarityTransformer()
        input_array = np.random.randint(-100, 100, size=(256, 256))  # Another example input array

        # Ensure the output shape is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, (256, 256))

        # Ensure values are inverted correctly
        self.assertTrue(np.all(result == -input_array))

    def test_invert_polarity_transformer_error_handling(self):
        transformer = InvertPolarityTransformer()
        input_array = "not_a_numpy_array"  # Invalid input (not a NumPy array)

        # Ensure a TypeError is raised for invalid input
        with self.assertRaises(TypeError):
            transformer.transform(input_array)

if __name__ == '__main__':
    unittest.main()
