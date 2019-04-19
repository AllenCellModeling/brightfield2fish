import numpy as np
from aicsimageio import AICSImage, OmeTifWriter

from brightfield2fish.data.preprocess_images import normalize


def test_normalize():
    fpath = "foo.ome.tiff"
    arr = np.random.randint(
        low=0, high=2 ** 16 - 1, size=(1, 2, 3, 4, 5), dtype=np.uint16
    )
    writer = OmeTifWriter(fpath, overwrite_file=True)
    writer.save(arr)
    im = AICSImage(fpath)

    for channel in (0, 1):
        _ = normalize(im, channel=channel)
