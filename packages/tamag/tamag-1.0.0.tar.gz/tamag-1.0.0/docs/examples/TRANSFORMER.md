## Overview of the `tamag` Module

The `tamag` module is a comprehensive package designed for transforming magnetogram maps using various techniques to reduce information loss and augment magnetograms for predictive modeling. It provides a collection of transformers, each tailored for a specific transformation method. These transformers can be easily integrated into your data preprocessing pipeline.

## Helpers

### Helper Function: `display_magnetogram`
To simplify the process of visualizing original and transformed magnetograms, we provide a helper function named `display_magnetogram`. This function takes the magnetogram, bitmap and transformed maps and displays them side by side for easy comparison.

```python
import matplotlib.pyplot as plt

def display_magnetogram(original, bitmap, transformed):
    """
    Display original and transformed magnetograms side by side.

    Args:
    - original (numpy array): Original magnetogram map.
    - bitmap (numpy array): Bitmap data
    - transformed (numpy array): Transformed magnetogram map.
    """

    # List of data to display
    data_list = [original, bitmap, transformed]
    titles = ['Original Image', 'Bitmap Data', 'Processed Image']

    # Visualize the images
    plt.figure(figsize=(15, 5))
    for i, (data, title) in enumerate(zip(data_list, titles), 1):
        plt.subplot(1, 3, i)
        plt.imshow(data, cmap='gray')
        plt.title(title)

    plt.show()
```

### Helper Function: `save_magnetogram`
To simplify the process of saving transformed magnetograms, we provide a helper function named save_magnetogram`. This function takes the transformed magnetogram and a filename and saves them for further processing.

```python
from PIL import Image

def save_image(img,path):
    """
    Saves magnetograms as image

    Args:
    - img (numpy array): magnetogram.
    - path (str): Path to save Image
    """
    pil_image = Image.fromarray(img)
    dpi = (300, 300) 
    if img.ndim == 2:  # Single-channel (grayscale)
        pil_image = pil_image.convert('L')
    elif img.ndim == 3 and img.shape[2] == 3:  # Three-channel (RGB)
        pil_image = pil_image.convert('RGB')
        path=f'{path.split(".")[0]}_rgb.{path.split(".")[1]}'
    pil_image.save(path) 
    return True
```

### Helper Function: `broilerplate`

For brevity reasons, we have included a broilerplate code that can be used throughout the guide. Replace `<TRANSFORMATION_TYPE>` with the transformer of choice.

```python 
# Boilerplate: Replace TRANSFORMATION_TYPE with the desired transformer type (e.g., HistogramEqualization)
from tamag.transforms import `<TRANSFORMATION_TYPE>`
import matplotlib.pyplot as plt
from tamag.datasets import load_fits_data

magnetogram, magnetogram_header, bitmap_data = load_fits_data()

transformer = `<TRANSFORMER_TYPE()>`

# Apply the transform 
transformed = transformer.transform(magnetogram)

# OR

# Apply the transform with rgb
transformed = transformer.transform(magnetogram, scale=255, rgb=True)

# Visualize
display_magnetogram(magnetogram, bitmap_data, transformed)
```

### Sample Output
![output](https://github.com/Adeyeha/tamag/tree/master/docs/images/transformer_output.png)

## Transformers

### 1. `Denoise`

The `Denoise` enhances the quality of an active region patch by employing denoising techniques. It constrains the values of the active region patch within a defined range and subsequently eliminates values falling below a specified noise threshold.

#### Example Usage:

```python
from tamag.transforms import Denoise

# Instantiate the transformer
transformer = Denoise()

# Replace with transformer in broilerplate code
```

### 2. `Flip`

The `Flip` modifies a magnetogram map by flipping it either horizontally or vertically. It encapsulates the logic for flipping the magnetogram based on a specified direction, which can be either 'horizontal' or 'vertical'.

#### Example Usage:

```python
from tamag.transforms import Flip

# Instantiate the transformer
transformer = Flip(direction='horizontal')

# Replace with transformer in broilerplate code
```

### 3. `GaussianBlur`

The `GaussianBlur` applies Gaussian blurring to a magnetogram map. Utilizing a Gaussian kernel, the extent of blurring is determined by the 'sigma' value. A higher sigma value leads to more pronounced blurring.

#### Example Usage:

```python
from tamag.transforms import GaussianBlur

# Instantiate the transformer
transformer = GaussianBlur(sigma=100)

# Replace with transformer in broilerplate code
```

### 4. `PolarityInversion`

The `PolarityInversion` reverses the polarity of a magnetogram map by multiplying all values in the magnetogram by -1. This transformation effectively flips the direction of the magnetic field lines.

#### Example Usage:

```python
from tamag.transforms import PolarityInversion

# Instantiate the transformer
transformer = PolarityInversion()

# Replace with transformer in broilerplate code
```

### 5. `Pad`

The `Pad` introduces padding to an image array, ensuring it reaches a designated size. The transformation adds the necessary padding to achieve the desired dimensions.

#### Example Usage:

```python
from tamag.transforms import Pad

# Instantiate the transformer
pad_transformer = Pad()

# Replace with transformer in broilerplate code
```

### 6. `FluxGuided`

The `FluxGuided` identifies the optimal patch within an image employing a stride-based approach. This transformer is designed to locate the most informative patch within the input image.

#### Example Usage:

```python
from tamag.transforms import FluxGuided

# Instantiate the transformer
pad_transformer = FluxGuided(stride=10)

# Replace with transformer in broilerplate code
```


### 7. `RandomNoise`

The `RandomNoise` introduces random noise to a magnetogram map by applying noise to each pixel. The noise is generated from a uniform distribution within the specified range of -gauss to gauss.

#### Example Usage:

```python
from tamag.transforms import RandomNoise

# Instantiate the transformer
random_noise_transformer = RandomNoise(gauss=500)

# Replace with transformer in broilerplate code
```

### 8. `ResizeByHalf`

The `ResizeByHalf` modifies a 2D numpy array by reducing its size to half of the original dimensions. The transformation achieves the resizing by employing average pooling on the image.

#### Example Usage:

```python
from tamag.transforms import ResizeByHalf

# Instantiate the transformer
resize_by_half_transformer = ResizeByHalf()

# Replace with transformer in broilerplate code
```

### 9. `Rotate`

The `Rotate` facilitates the rotation of a magnetogram map by a user-specified angle. The transformation is accomplished through the rotation function, enabling rotation at any angle within the range of 0 to 360 degrees.

#### Example Usage:

```python
from tamag.transforms import Rotate

# Instantiate the transformer
rotation_transformer = Rotate(angle=45)

# Replace with transformer in broilerplate code
```

### 10. `ByteScaling`

The `ByteScaling` performs scaling of values in an input array, excluding NaNs, to fit within a specified range.

#### Example Usage:

```python
from tamag.transforms import ByteScaling

# Instantiate the transformer
byte_scaling_transformer = ByteScaling()

# Replace with transformer in broilerplate code
```

### 11. `BitmapCropping`

The `BitmapCropping` performs cropping of an Active Region (AR) Patch based on bitmap data, utilizing the largest connected component in the bitmap data to determine the cropping region.

#### Example Usage:

```python
from tamag.transforms import BitmapCropping

# Instantiate the transformer
bitmap_cropping_transformer = BitmapCropping()

# Replace with transformer in broilerplate code
```

### 12. `HistogramEqualization`

The `HistogramEqualization` enhances the contrast of a magnetogram map by redistributing intensity values. This can be particularly useful for improving visual contrast in the magnetogram.

#### Example Usage:
```python
from tamag.transforms import HistogramEqualization

# Instantiate the transformer
bitmap_cropping_transformer = HistogramEqualization()

# Replace with transformer in broilerplate code
```

## Next Steps

Feel free to explore more transformers within the `tamag` module or integrate them into your magnetogram preprocessing pipeline. For detailed guidance on efficiently organizing and applying these transformers, check out the [pipeline](./PIPELINE.md) documentation.


Happy transforming!
