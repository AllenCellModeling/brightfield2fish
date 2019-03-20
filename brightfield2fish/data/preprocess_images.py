"""
This module/script takes the raw czi images and normalizes each channel,
and saves each channel of each image to a single channel ZYX tiff file in
/allen/aics/modeling/data/brightfield2fish/preprocessed.
The df it needs as input is created by preprocess_csv.py.
"""

import os
import warnings
import concurrent
import functools
from tqdm import tqdm

import pandas as pd
import numpy as np

from utils import prep_fish

from aicsimageio import AICSImage, OmeTifWriter


def normalize(image, channel=0):
    if channel == 0:
        out = prep_fish(
            image,
            channel=channel,
            T=0,
            clip_percentiles=[0.01, 99.99],
            median_subtract=False,
            math_dtype=np.float64,
            out_dtype=np.uint16,
        )
    else:
        out = prep_fish(
            image,
            channel=channel,
            T=0,
            clip_percentiles=[0, 99.99],
            median_subtract=True,
            math_dtype=np.float64,
            out_dtype=np.uint16,
        )
    return out


def worker_full(file, df):
    df_file = df[df["file"] == file]
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        image = AICSImage(file)
    for i, row in df_file.iterrows():
        image_ZYX = normalize(image, channel=row["channel_index"])
        with OmeTifWriter(
            row["normalized_single_channel_image"], overwrite_file=True
        ) as writer:
            writer.save(
                image_ZYX,
                channel_names=row["channel_content"],
                pixels_physical_size=image.get_physical_pixel_size(),
            )


if __name__ == "__main__":
    preprocessed_par_dir = "/allen/aics/modeling/data/brightfield2fish/preprocessed"
    preprocessed_im_dir = os.path.join(preprocessed_par_dir, "images")

    df = pd.read_csv("data_by_channels.csv")
    df["normalized_single_channel_image"] = (
        preprocessed_im_dir
        + os.path.sep
        + df["file"].apply(lambda x: os.path.splitext(os.path.basename(x))[0])
        + "_channel_"
        + df["channel_index"].astype(str)
        + ".tif"
    )
    assert len(np.unique(df["normalized_single_channel_image"])) == len(df)
    df.to_csv(
        os.path.join(preprocessed_par_dir, "data_by_images_normalized.csv"), index=False
    )

    worker = functools.partial(worker_full, df=df)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        tqdm(
            executor.map(worker, np.unique(df["file"])),
            total=len(np.unique(df["file"])),
        )
