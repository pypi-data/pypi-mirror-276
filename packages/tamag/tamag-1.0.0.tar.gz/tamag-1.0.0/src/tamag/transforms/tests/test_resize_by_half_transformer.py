# tests/test_resize_transformer.py

import unittest
import numpy as np
from tamag.transforms import ResizeByHalfTransformer

class TestResizeByHalfTransformer(unittest.TestCase):
    def test_resize_by_half_transformer(self):
        transformer = ResizeByHalfTransformer(verbose=False)
        input_array = np.random.randint(0, 255, size=(512, 512))  # Example input array

        # Ensure the output shape is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, (256, 256))

        # Ensure values are averaged correctly
        self.assertEqual(np.sum(input_array) / 4, np.sum(result))


    def test_resize_by_half_transformer_error_handling(self):
        transformer = ResizeByHalfTransformer(verbose=False)
        input_array = "not_a_numpy_array"  # Invalid input (not a NumPy array)

        # Ensure a TypeError is raised for invalid input
        with self.assertRaises(TypeError):
            transformer.transform(input_array)

if __name__ == '__main__':
    unittest.main()
