import numpy as np
from functools import partial
from PIL import Image


def normalize_image_zero_one(im):
    """im is a np array"""
    im = im - np.min(im)
    if np.max(im) > 0:
        im = im / np.max(im)
    return im


def normalize_image_center_scale(im):
    """im is a np array"""
    im -= np.mean(im)
    im /= np.std(im)
    return im


def float_to_uint(im, uint_dtype=np.uint8):
    """im is a np array"""
    imax = np.iinfo(uint_dtype).max + 1  # eg imax = 256 for uint8
    im = im * imax
    im[im == imax] = imax - 1
    im = np.asarray(im, uint_dtype)
    return im


def prep_fish(
    image,
    channel=1,
    T=0,
    clip_percentiles=[0, 99.99],
    median_subtract=True,
    math_dtype=np.float64,
    out_dtype=np.uint16,
):
    """image is an AICSImage object"""
    img3d = image.get_image_data("ZYX", T=T, C=channel)
    img3d = img3d.astype(math_dtype)
    img3d = np.clip(
        img3d,
        a_min=np.percentile(img3d, clip_percentiles[0]),
        a_max=np.percentile(img3d, clip_percentiles[1]),
    )
    if median_subtract:
        img3d -= np.median(img3d)
        img3d[img3d < 0] = 0
    img3d = normalize_image_zero_one(img3d)
    if "uint" in str(out_dtype):
        img3d = float_to_uint(img3d, uint_dtype=out_dtype)
    return img3d


def plot_prepped(img3d, reduce_3D_to_2D=partial(np.percentile, q=100, axis=0)):
    """img3d a 3d np array, eg the output of prep_fish"""
    img2d = reduce_3D_to_2D(img3d)
    img2d = float_to_uint(img2d)
    return Image.fromarray(img2d, "L")
