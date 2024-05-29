# pytorch-smartcrop

This is a PyTorch implementation of the smartcrop algorithm. The smartcrop algorithm is a content aware image cropping algorithm that is used to crop images to the most interesting part of the image. The algorithm is based on the pyvips smartcrop implementation.

# Prerequisites

- requires libvips shared library to be installed on the system. For further information on how to install libvips, please refer to the [libvips installation guide](https://libvips.github.io/libvips/install.html)

# Usage

```python
from pytorch_smartcrop import SmartCrop
from PIL import Image

# load image
image = Image.open('image.jpg')

# crop image to 256x256
sc = SmartCrop(patch_size=(256, 256))
cropped_image = sc(image)
```
