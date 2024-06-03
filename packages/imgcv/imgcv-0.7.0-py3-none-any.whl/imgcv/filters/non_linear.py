import numpy as np
from imgcv.common import check_image


def min_filter(img, filter_size):
    """Apply min filter to the image.It takes the minimum value of the pixels in the window.

    Args:
        img (np.ndarray): Input Image array
        filter_size (Tuple[int, int]): Size of the filter

    Raises:
        ValueError: If filter_size is not a tuple.

    Returns:
        np.ndarray: Filtered image array.
    """

    check_image(img)
    if not isinstance(filter_size, tuple):
        raise ValueError("filter_size should be a tuple")

    if len(img.shape) == 2:
        final_img = np.zeros(img.shape)

        for row in range(img.shape[0]):
            for col in range(img.shape[1]):
                window = img[row : row + filter_size[0], col : col + filter_size[1]]
                result = np.min(window)
                final_img[row, col] = result

        return final_img.astype(np.uint8)

    else:
        final_img = np.zeros(img.shape)
        for i in range(img.shape[2]):
            final_img[:, :, i] = min_filter(img[:, :, i], filter_size)

        return final_img.astype(np.uint8)


def max_filter(img, filter_size):
    """Apply max filter to the image.It takes the maximum value of the pixels in the window.

    Args:
        img (np.ndarray): Input Image array
        filter_size (Tuple[int,int]): Size of the filter

    Raises:
        ValueError: If filter_size is not a tuple.

    Returns:
        np.ndarray: Filtered image array.
    """

    check_image(img)
    if not isinstance(filter_size, tuple):
        raise ValueError("filter_size should be a tuple")

    if len(img.shape) == 2:
        final_img = np.zeros(img.shape)

        for row in range(img.shape[0]):
            for col in range(img.shape[1]):
                window = img[row : row + filter_size[0], col : col + filter_size[1]]
                result = np.max(window)
                final_img[row, col] = result

        return final_img.astype(np.uint8)

    else:
        final_img = np.zeros(img.shape)
        for i in range(img.shape[2]):
            final_img[:, :, i] = max_filter(img[:, :, i], filter_size)

        return final_img.astype(np.uint8)


def median_filter(img, filter_size):
    """Apply median filter to the image.It takes the median value of the pixels in the window.

    Args:
        img (np.ndarray): Input Image array
        filter_size (Tuple[int,int]): Size of the filter

    Raises:
        ValueError: If filter_size is not a tuple.

    Returns:
        np.ndarray: Filtered image array.
    """
    check_image(img)
    if not isinstance(filter_size, tuple):
        raise ValueError("filter_size should be a tuple")

    if len(img.shape) == 2:
        final_img = np.zeros(img.shape)

        for row in range(img.shape[0]):
            for col in range(img.shape[1]):
                window = img[row : row + filter_size[0], col : col + filter_size[1]]
                result = np.median(window)
                final_img[row, col] = result
        return final_img.astype(np.uint8)

    else:
        final_img = np.zeros(img.shape)
        for i in range(img.shape[2]):
            final_img[:, :, i] = median_filter(img[:, :, i], filter_size)

        return final_img.astype(np.uint8)
