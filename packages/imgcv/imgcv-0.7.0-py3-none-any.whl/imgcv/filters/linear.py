import numpy as np
from imgcv.common import check_image


def box_filter(img, filter_size):
    """Apply box filter to the image. This is a simple averaging filter.

    Args:
        img (np.ndarray): Input Image array
        filter_size (Tuple[int, int]): Size of the filter.

    Raises:
        ValueError: If filter_size is not a tuple.

    Returns:
        np.ndarray: Filtered image array.
    """
    check_image(img)
    if not isinstance(filter_size, tuple):
        raise ValueError("filter_size should be a tuple")

    if len(img.shape) == 2:

        pad_height = filter_size[0] // 2
        pad_width = filter_size[1] // 2

        padded_img = np.pad(
            img, ((pad_height, pad_height), (pad_width, pad_width)), mode="constant"
        )

        kernel = np.ones(filter_size)

        # convolve
        final_img = np.zeros(img.shape)
        for row in range(img.shape[0]):
            for col in range(img.shape[1]):
                window = padded_img[
                    row : row + filter_size[0], col : col + filter_size[1]
                ]
                result = np.mean(window * kernel)
                result = np.clip(result, 0, 255)
                final_img[row, col] = np.round(result)

        return final_img.astype(np.uint8)

    else:
        # apply filter to each channel
        final_img = np.zeros(img.shape)
        for i in range(img.shape[2]):
            final_img[:, :, i] = box_filter(img[:, :, i], filter_size)
        return final_img.astype(np.uint8)
