import unittest
import numpy as np
from tamag.transforms import ByteScalingTransformer

class TestByteScalingTransformer(unittest.TestCase):
    def test_byte_scaling_transformer_default(self):
        transformer = ByteScalingTransformer()
        input_array = np.random.rand(512, 512) * 255  # Example input array

        # Ensure the output shape is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, (512, 512))

        # Ensure values are byte-scaled correctly
        self.assertTrue(np.all(result >= 0))
        self.assertTrue(np.all(result <= 255))

    def test_byte_scaling_transformer_custom_values(self):
        transformer = ByteScalingTransformer(min_value=50, max_value=200, scaler=100)
        input_array = np.random.rand(256, 256) * 150 + 50  # Another example input array

        # Ensure the output shape is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, (256, 256))

        # Ensure values are byte-scaled correctly
        self.assertTrue(np.all(result >= 0))
        self.assertTrue(np.all(result <= 100))

    def test_byte_scaling_transformer_nan_values(self):
        transformer = ByteScalingTransformer()
        input_array = np.random.rand(512, 512)  # Example input array with NaN values
        input_array[100:200, 100:200] = np.nan  # Introduce NaN values

        # Ensure the output shape is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, (512, 512))

        # Ensure NaN values are not preserved in the output
        nan_indices = np.isnan(input_array)
        self.assertFalse(np.any(np.isnan(result[nan_indices])))

    def test_byte_scaling_transformer_error_handling(self):
        transformer = ByteScalingTransformer()
        input_array = "not_a_numpy_array"  # Invalid input (not a NumPy array)

        # Ensure a TypeError is raised for invalid input
        with self.assertRaises(TypeError):
            transformer.transform(input_array)

if __name__ == '__main__':
    unittest.main()
