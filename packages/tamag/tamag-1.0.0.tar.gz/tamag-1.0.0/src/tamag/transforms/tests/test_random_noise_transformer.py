import unittest
import numpy as np
from tamag.transforms import RandomNoiseTransformer

class TestRandomNoiseTransformer(unittest.TestCase):
    def test_random_noise_transformer_default(self):
        transformer = RandomNoiseTransformer()
        input_array = np.random.rand(512, 512)  # Example input array

        # Ensure the output shape is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, (512, 512))

        # Ensure the noisy result is not equal to the original input (simple validation)
        self.assertFalse(np.array_equal(result, input_array))

    def test_random_noise_transformer_custom_gauss(self):
        transformer = RandomNoiseTransformer(gauss=10)
        input_array = np.random.rand(256, 256)  # Another example input array

        # Ensure the output shape is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, (256, 256))

        # Ensure the noisy result is not equal to the original input (simple validation)
        self.assertFalse(np.array_equal(result, input_array))

    def test_random_noise_transformer_error_handling(self):
        transformer = RandomNoiseTransformer()
        input_array = "not_a_numpy_array"  # Invalid input (not a NumPy array)

        # Ensure a TypeError is raised for invalid input
        with self.assertRaises(TypeError):
            transformer.transform(input_array)

if __name__ == '__main__':
    unittest.main()
