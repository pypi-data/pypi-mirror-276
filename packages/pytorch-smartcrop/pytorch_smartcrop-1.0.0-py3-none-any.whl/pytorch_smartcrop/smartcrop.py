from typing import Tuple

import PIL.Image
import pyvips
import torch
from pyvips.enums import Interesting


class SmartCrop(torch.nn.Module):
    """
    A PyTorch module that wraps the smartcrop function from the libvips library.
    This module is used to intelligently crop images based on the specified patch size and interestingness measure.

    Parameters
    ----------
    torch : torch.nn.Module
        The base class for all neural network modules in PyTorch.
    """

    def __init__(
        self, patch_size: Tuple[int, int], interesting: Interesting = "entropy"
    ):
        """
        Initializes the SmartCrop module with the given patch size and interestingness measure.

        Parameters
        ----------
        patch_size : tuple
            The size of the patch to crop from the image. It is a tuple of two integers representing the width and height of the patch.
        interesting : str, optional
            The measure of interestingness to use when deciding where to crop the image. It can be for example "entropy" or "attention". By default, it is set to "entropy".
        """
        super().__init__()
        self.patch_size = patch_size
        self.interesting = interesting

    def forward(self, pil_image: PIL.Image) -> PIL.Image:
        """
        Performs the forward pass of the module, which involves cropping the given PIL image.

        Parameters
        ----------
        pil_image : PIL.Image
            The image to crop. It should be a PIL Image object.

        Returns
        -------
        PIL.Image
            The cropped image as a PIL Image object.
        """
        image = pyvips.Image.new_from_array(pil_image)
        pil_image = image.smartcrop(
            self.patch_size[0],
            self.patch_size[1],
            interesting=self.interesting,
        )
        return PIL.Image.fromarray(pil_image.numpy())
