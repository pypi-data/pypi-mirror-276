# tests/test_preprocess_transformer.py

import unittest
import numpy as np
from tamag.transforms import DenoiseTransformer

class TestDenoiseTransformer(unittest.TestCase):

    def assertAllZeroWithinRange(self, array, lower_bound, upper_bound):
        # Helper function to check if all values within the specified range are set to zero
        values_within_range = np.logical_and(array >= lower_bound, array <= upper_bound) 
        self.assertTrue(np.all(array[values_within_range] == 0))

    def test_preprocess_transformer_default(self):
        lower_bound = -50
        upper_bound = 50
        maximum_range = 256
        size = (512, 512)
        transformer = DenoiseTransformer(lower_bound=lower_bound, upper_bound=upper_bound, maximum_range=maximum_range)
        input_array = np.random.randint(-255, 255, size=size)  # Example input array

        # Ensure the output shape is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, size)

        # Check if any value is outside the maximum range
        self.assertFalse(np.any(np.logical_or(result < -maximum_range,result > maximum_range)))

        # Ensure values within the specified range are set to zero
        self.assertAllZeroWithinRange(result, lower_bound, upper_bound)

    def test_preprocess_transformer_custom_values_lower(self):
        lower_bound = -30
        upper_bound = 30
        maximum_range = 128
        size = (256, 256)
        transformer = DenoiseTransformer(lower_bound=lower_bound, upper_bound=upper_bound, maximum_range=maximum_range)
        input_array = np.random.randint(-127, 127, size=size)  # Example input array with all values lower than maximum_range

        # Ensure the output shape is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, size)

        # Check if any value is outside the maximum range
        self.assertFalse(np.any(np.logical_or(result < -maximum_range,result > maximum_range)))

        # Ensure values within the specified range are set to zero
        self.assertAllZeroWithinRange(result, lower_bound, upper_bound)

    def test_preprocess_transformer_custom_values_higher(self):
        lower_bound = -30
        upper_bound = 30
        maximum_range = 128
        size = (256, 256)
        transformer = DenoiseTransformer(lower_bound=lower_bound, upper_bound=upper_bound, maximum_range=maximum_range)
        input_array = np.random.randint(-1024, 1024, size=size)  # Example input array with all values higher than maximum_range

        # Ensure the output shape is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, size)

        # Check if any value is outside the maximum range
        self.assertFalse(np.any(np.logical_or(result < -maximum_range,result > maximum_range)))

        # Ensure values within the specified range are set to zero
        self.assertAllZeroWithinRange(result, lower_bound, upper_bound)

    def test_preprocess_transformer_error_handling(self):
        transformer = DenoiseTransformer(lower_bound=-20, upper_bound=20, maximum_range=64)
        input_array = "not_a_numpy_array"  # Invalid input (not a NumPy array)

        # Ensure a TypeError is raised for invalid input
        with self.assertRaises(TypeError):
            transformer.transform(input_array)

if __name__ == '__main__':
    unittest.main()
