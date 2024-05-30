import unittest
import numpy as np
from tamag.transformers import FlipTransformer
from tamag.utils.exceptions import InformationLossWarning

class TestFlipTransformer(unittest.TestCase):
    def test_flip_transformer_horizontal(self):
        transformer = FlipTransformer(direction='horizontal', loss_threshold=1.0, verbose=True)
        input_array = np.random.rand(512, 512)  # Example input array

        # Ensure the output shape is correct
        result = transformer.transform(input_array)
        self.assertEqual(result.shape, (512, 512))

        # Ensure the array is flipped horizontally
        self.assertTrue(np.all(result[:, ::-1] == input_array))

    def test_flip_transformer_vertical(self):
        transformer = FlipTransformer(direction='vertical', loss_threshold=1.0, verbose=True)
        input_array = np.random.rand(512, 512)  # Example input array

        # Ensure the output shape is correct
        result= transformer.transform(input_array)
        self.assertEqual(result.shape, (512, 512))

        # Ensure the array is flipped vertically
        self.assertTrue(np.all(result[::-1, :] == input_array))

    def test_flip_transformer_information_loss_warning(self):
        transformer = FlipTransformer(direction='horizontal', loss_threshold=-1.0, verbose=True)
        input_array = np.random.rand(512, 512)  # Example input array

        # Ensure an InformationLossWarning is issued when information loss exceeds the threshold
        with self.assertWarns(InformationLossWarning):
            transformer.transform(input_array)

    def test_flip_transformer_invalid_input_type(self):
        transformer = FlipTransformer(direction='horizontal', loss_threshold=1.0, verbose=True)
        input_array = "not_a_numpy_array"  # Invalid input (not a NumPy array)

        # Ensure a TypeError is raised for invalid input type
        with self.assertRaises(TypeError):
            transformer.transform(input_array)

if __name__ == '__main__':
    unittest.main()
