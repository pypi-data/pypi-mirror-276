import numpy as np
import scipy.ndimage
import time
from timelined_array import TimelinedArray
from logging import getLogger


def downsample(data, factor=4, axes=(2, 3)):
    """Downsample the input data using averaging.

    Args:
        data (np.ndarray): The input data to be downsampled.
        factor (int, optional): The downsampling factor. Defaults to 4.
        axes (tuple, optional): The axes along which to perform downsampling. Defaults to (2, 3).

    Returns:
        np.ndarray: The downsampled data.
    """

    # Downsample function using averaging
    logger = getLogger("downsampling")

    pad_width = [(0, 0)] * data.ndim
    for axis in axes:
        pad_size = (factor - data.shape[axis] % factor) % factor
        pad_width[axis] = (0, pad_size)
    _data = np.pad(data, pad_width, mode="constant", constant_values=0)

    reshaping_parameters = []
    mean_axes = []
    current_dim = 0
    for dim, dimsize in enumerate(_data.shape):
        if dim in axes:
            reshaping_parameters.append(_data.shape[dim] // factor)
            current_dim += 1
            reshaping_parameters.append(factor)
            mean_axes.append(current_dim)
            current_dim += 1
        else:
            reshaping_parameters.append(_data.shape[dim])
            current_dim += 1
    start_time = time.time()
    _data = _data.reshape(*reshaping_parameters)
    _data = _data.mean(axis=tuple(mean_axes))
    end_time = time.time()
    logger.info(f"Finished downsampling (factor-{factor}) in {end_time - start_time:.2f} seconds")
    if isinstance(data, TimelinedArray) and data.time_dimension not in axes:
        _data = TimelinedArray(_data, time_dimension=data.time_dimension, timeline=data.timeline)

    return _data  # , pad_width


def upsample(data, original_shape, factor=4, axes=(2, 3), order=1):
    """Upsample function using interpolation.

    Args:
        data (ndarray): Input data to upsample.
        original_shape (tuple): Original shape of the data before upsampling.
        factor (int, optional): Upsampling factor. Defaults to 4.
        axes (tuple, optional): Axes along which to upsample. Defaults to (2, 3).
        order (int, optional): Order of interpolation. Defaults to 1 for linear interpolation.

    Returns:
        ndarray: Upsampled data.

    Raises:
        None
    """

    # Upsample function using interpolation
    # order=3 for cubic interpolation (Lanczos)

    logger = getLogger("upsampling")

    zoom_factors = []
    for dim, dimsize in enumerate(data.shape):
        if dim in axes:
            zoom_factors.append(factor)
        else:
            zoom_factors.append(1)

    try:
        from cupyx.scipy.ndimage import zoom as cp_zoom
        import cupy as cp
    except Exception:
        pass

    start_time = time.time()
    upsampled_data = scipy.ndimage.zoom(data, zoom=tuple(zoom_factors), order=order)
    end_time = time.time()
    logger.info(f"Finished upsampling (factor-{factor}) in {end_time - start_time:.2f} seconds")

    slices = tuple(slice(0, original_shape[dim]) for dim in range(len(original_shape)))
    _data = upsampled_data[slices]
    if isinstance(data, TimelinedArray) and data.time_dimension not in axes:
        _data = TimelinedArray(_data, time_dimension=data.time_dimension, timeline=data.timeline)
    return _data
