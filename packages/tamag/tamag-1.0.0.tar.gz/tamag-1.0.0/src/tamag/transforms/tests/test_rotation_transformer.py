# tests/test_rotation_transformer.py

import unittest
import numpy as np
from tamag.transforms import RotationTransformer
from tamag.utils.exceptions import InformationLossWarning

class TestRotationTransformer(unittest.TestCase):
    def test_rotation_transformer_default(self):
        transformer = RotationTransformer(angle=30, order=3, loss_threshold=1.0)
        input_array = np.random.rand(512, 512)  # Example input array

        # Ensure the output shape is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, (512, 512))

        # Ensure the rotation angle is applied correctly
        self.assertNotAlmostEqual(np.sum(input_array), np.sum(result))

    def test_rotation_transformer_custom_values(self):
        transformer = RotationTransformer(angle=45, order=0, loss_threshold=0.5)
        input_array = np.random.rand(256, 256)  # Another example input array

        # Ensure the output shape is correct
        result= transformer.transform(input_array)
        self.assertEqual(result.shape, (256, 256))

        # Ensure the rotation angle is applied correctly
        self.assertNotAlmostEqual(np.sum(input_array), np.sum(result))

    def test_rotation_transformer_information_loss(self):
        transformer = RotationTransformer(angle=60, order=3, loss_threshold=-1.0)
        input_array = np.random.rand(128, 128)  # Example input array

        # Ensure the information loss warning is raised
        with self.assertWarns(InformationLossWarning):
            result = transformer.transform(input_array)

    def test_rotation_transformer_with_bitmap_data(self):
        transformer = RotationTransformer(angle=179, order=1, loss_threshold=1.0)
        input_array = np.random.rand(512, 512)  # Example input array
        bitmap_data = np.random.randint(0, 2, size=(512, 512))  # Example bitmap data

        # Ensure the output shape is correct
        result  = transformer.transform(input_array,)
        bitmap_result = transformer.transform(bitmap_data)

        self.assertEqual(result.shape, (512, 512))
        self.assertEqual(bitmap_result.shape, (512, 512))

        # Ensure the rotation angle is applied correctly to both arrays
        self.assertNotAlmostEqual(np.sum(input_array), np.sum(result))
        self.assertNotAlmostEqual(np.sum(bitmap_data), np.sum(bitmap_result))

    def test_rotation_transformer_invalid_input(self):
        transformer = RotationTransformer(angle=45, order=3, loss_threshold=1.0)
        invalid_input = "not_a_numpy_array"  # Invalid input (not a NumPy array)

        # Ensure a TypeError is raised for invalid input
        with self.assertRaises(TypeError):
            transformer.transform(invalid_input)

if __name__ == '__main__':
    unittest.main()
