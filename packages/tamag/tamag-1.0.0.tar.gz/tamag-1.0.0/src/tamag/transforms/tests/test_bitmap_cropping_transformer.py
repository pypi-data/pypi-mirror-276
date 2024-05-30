import unittest
import numpy as np
from tamag.transforms import BitmapCroppingTransformer

class TestBitmapCroppingTransformer(unittest.TestCase):
    def test_bitmap_cropping_transformer_error_handling(self):
        transformer = BitmapCroppingTransformer()
        AR_patch = "not_a_numpy_array"  # Invalid input (not a NumPy array)
        bitmap_data = np.random.randint(0, 3, (512, 512))  # Example bitmap data

        # Ensure a TypeError is raised for invalid input
        with self.assertRaises(TypeError):
            transformer.transform(AR_patch, bitmap_data)

if __name__ == '__main__':
    unittest.main()
