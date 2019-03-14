import numpy as np


def normalize_image_zero_one(im):
    im -= np.min(im)
    if np.max(im) > 0:
        im /= np.max(im)
    return im


def normalize_image_center_scale(im):
    im -= np.mean(im)
    im /= np.std(im)
    return im
