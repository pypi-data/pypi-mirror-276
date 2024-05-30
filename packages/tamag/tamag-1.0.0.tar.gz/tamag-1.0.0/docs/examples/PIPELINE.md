## Overview of the `tamag` Pipeline Module

The `tamag` module provides a flexible and customizable pipeline for applying a sequence of transformations to magnetogram maps. The pipeline is designed to be modular, allowing users to easily experiment with different combinations of transformers.

### Pipeline Initialization

To create a pipeline, you need to instantiate a `Pipeline` object with a list of transformer instances. Each transformer will be applied sequentially in the order specified in the list.

#### Example Initialization:

```python
from tamag.transforms import Rotate, Pad, ByteScaling, Flip
from tamag.pipeline import Pipeline

# Instantiate the pipeline with a list of transformers
transformation_pipeline = Pipeline([
    Rotate(angle=5),
    Flip(direction='vertical', loss_threshold=1),
    ByteScaling(),
], on_error="ignore", on_null_output="ignore")
```

### Applying the Pipeline
Once the pipeline is initialized, you can apply it to a magnetogram map by calling the `transform` method.

#### Example Application:
```python
from tamag.datasets import load_fits_data

# Load magnetogram data (replace with your own data loading code)
magnetogram, magnetogram_header, bitmap_data = load_fits_data(sample_no=2)

# Apply the transformation pipeline to the magnetogram
transformed_magnetogram = transformation_pipeline.transform(magnetogram)
```

### Pipeline Options
The pipeline supports optional parameters such as on_error and on_null_output, allowing users to control the behavior in case of errors or null outputs during the transformation process.

### Experimenting with Transformation modules
Feel free to experiment with different modules and their configurations within the pipeline to achieve desired results. You can customize the list of transformers based on your specific use case.

Refer to the [documentation](./TRANSFORMER.md) for detailed information on each transformer and the pipeline.

Happy experimenting with magnetogram transformations!