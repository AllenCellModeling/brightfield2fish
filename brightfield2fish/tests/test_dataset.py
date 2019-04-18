import os
import pandas as pd

from brightfield2fish.data.dataset import FishDataframeDatasetTIFF


def test_FishDataframeDatasetTIFF():
    dirname = os.path.dirname(__file__)
    csv_path = os.path.join(
        os.path.dirname(os.path.dirname(dirname)),
        "data",
        "data_by_images_normalized.csv",
    )
    df = pd.read_csv(csv_path)

    dset = FishDataframeDatasetTIFF(df, channel_content="DNA")

    assert len(dset) == len(df["file"].unique())
