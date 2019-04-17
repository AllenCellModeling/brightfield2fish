import numpy as np

from brightfield2fish.data.utils import (
    normalize_image_zero_one,
    normalize_image_center_scale,
    normalize,
    float_to_uint,
    plot_prepped,
    get_random_crop_3D,
    perform_crop_3D,
    RandomCrop3D,
)


def test_normalize_image_zero_one():
    im = np.random.randn(10, 20, 30)
    im_norm = normalize_image_zero_one(im)
    assert np.isclose(np.min(im_norm), 0) and np.isclose(np.max(im_norm), 1)


def test_normalize_image_center_scale():
    im = np.random.randn(10, 20, 30)
    im_norm = normalize_image_center_scale(im)
    assert np.isclose(np.mean(im_norm), 0) and np.isclose(np.std(im_norm), 1)


def test_normalize():
    im = np.random.randn(10, 20, 30)

    im_norm_fl = normalize(im, content="Fluor")
    assert np.isclose(np.min(im_norm_fl), 0) and np.isclose(np.max(im_norm_fl), 1)

    im_norm_bf = normalize(im, content="Brightfield")
    assert np.isclose(np.mean(im_norm_bf), 0) and np.isclose(np.std(im_norm_bf), 1)


def test_float_to_uint():
    arr_f = np.random.rand(10, 20, 30)
    arr_u = float_to_uint(arr_f)
    assert np.min(arr_u) == 0 and np.max(arr_u) == 255


def test_plot_prepped():
    arr = np.random.rand(10, 20, 30)
    arr = normalize(arr, content="Fluor")
    im = plot_prepped(arr)


def test_get_random_crop_3D():
    arr = np.random.randn(10, 20, 30)
    zlims, ylims, xlims = get_random_crop_3D(arr, 5, 10, 15)
    assert zlims[0] >= 0 and zlims[1] <= 10 and zlims[1] - zlims[0] == 5
    assert ylims[0] >= 0 and ylims[1] <= 20 and ylims[1] - ylims[0] == 10
    assert xlims[0] >= 0 and xlims[1] <= 30 and xlims[1] - xlims[0] == 15


def test_perform_crop_3D():
    arr = np.random.randn(10, 20, 30)
    arr_crop = perform_crop_3D(arr, [1, 3], [2, 5], [3, 7])
    assert arr_crop.shape == (2, 3, 4)


def test_RandomCrop3D():
    arr = np.random.randn(10, 20, 30)
    arr2 = np.random.randn(10, 20, 30)
    rc = RandomCrop3D(arr, 2, 3, 4)
    arr_crop = rc.crop(arr2)
    assert arr_crop.shape == (2, 3, 4)