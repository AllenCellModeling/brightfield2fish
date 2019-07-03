import os
import numpy as np
import pandas as pd

from aicsimageio import OmeTifWriter
from brightfield2fish.data.dataset import (
    FishDataframeDatasetTIFF,
    FishSegDataframeDatasetTIFF,
)


def test_FishDataframeDatasetTIFF(
    channel_content="MYL2",
    split="valid",
    data="fake",
    resize_original=(1, 1, 1),
    random_crop=(1, 2, 3),
):
    dirname = os.path.dirname(__file__)
    csv_path = os.path.join(
        os.path.dirname(os.path.dirname(dirname)),
        "data",
        "splits",
        "{}.csv".format(split),
    )

    df = pd.read_csv(csv_path)

    dset = FishDataframeDatasetTIFF(
        csv_path,
        channel_content=channel_content,
        csv=True,
        resize_original=resize_original,
        random_crop=random_crop,
    )

    assert len(dset) == len(
        df[df["channel_content"] == channel_content]["file"].unique()
    )

    if data == "fake":
        fake_tiff_dir = "fake_tiffs"
        if not os.path.exists(fake_tiff_dir):
            os.makedirs(fake_tiff_dir)

        for i, row in dset.df.iterrows():
            for channel in ("Brightfield", "Target"):
                fpath = os.path.join(fake_tiff_dir, "{0}_{1}.tiff".format(channel, i))
                dset.df.loc[i, channel] = fpath
                arr = np.random.randint(
                    low=0, high=2 ** 16 - 1, size=(1, 1, 2, 3, 4), dtype=np.uint16
                )
                writer = OmeTifWriter(fpath, overwrite_file=True)
                writer.save(arr)

    j = np.random.randint(len(dset.df))
    sample = dset[j]
    assert sample[0].shape == sample[1].shape


def test_FishSegDataframeDatasetTIFF(
    channel_content="MYL2",
    split="valid",
    data="fake",
    resize_original=(1, 1, 1),
    random_crop=(1, 2, 3),
):
    dirname = os.path.dirname(__file__)
    csv_path = os.path.join(
        os.path.dirname(os.path.dirname(dirname)),
        "data",
        "splits",
        "{}.csv".format(split),
    )

    df = pd.read_csv(csv_path)

    dset = FishSegDataframeDatasetTIFF(
        csv_path,
        channel_content=channel_content,
        csv=True,
        resize_original=resize_original,
        random_crop=random_crop,
    )

    assert len(dset) == len(
        df[df["channel_content"] == channel_content]["file"].unique()
    )

    if data == "fake":
        fake_tiff_dir = "fake_tiffs"
        if not os.path.exists(fake_tiff_dir):
            os.makedirs(fake_tiff_dir)

        for i, row in dset.df.iterrows():
            for channel in ("Brightfield", "Target"):
                fpath = os.path.join(fake_tiff_dir, "{0}_{1}.tiff".format(channel, i))
                dset.df.loc[i, channel] = fpath
                arr = np.random.randint(
                    low=0, high=2 ** 16 - 1, size=(1, 1, 2, 3, 4), dtype=np.uint16
                )
                writer = OmeTifWriter(fpath, overwrite_file=True)
                writer.save(arr)

    j = np.random.randint(len(dset.df))
    sample = dset[j]
    assert sample[0].shape == sample[1].shape
