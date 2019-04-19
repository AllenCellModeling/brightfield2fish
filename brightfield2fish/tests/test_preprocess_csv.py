import os
import numpy as np
import pandas as pd

from aicsimageio import OmeTifWriter
from brightfield2fish.data.preprocess_csv import find_czis, filter_czis


def test_find_and_filter_czis(data="fake"):

    dirname = os.path.dirname(__file__)
    csv_path = os.path.join(
        os.path.dirname(os.path.dirname(dirname)), "data", "data.csv"
    )

    df = pd.read_csv(csv_path)
    df = df.rename(index=str, columns={"link_to_data": "directory"})
    df["plate"] = df["plate"].astype(str)
    df = df.replace({"PRSS35": "PRSS3", "COL2A": "COL2A1"})

    # add CAAX signal to channel info:
    for i, row in df.iterrows():
        if row["cell_line"] == "CAAX":
            df.loc[i, "probe_561"] = "CAAX"

    # add fake czi files
    if data == "fake":

        for i, row in df.iterrows():
            df.loc[i, "directory"] = row["directory"].replace(
                "/allen/aics/microscopy/Data/RnD_Sandbox",
                os.path.join(os.path.dirname(os.path.dirname(dirname)), "fake_czis"),
            )

        for directory in df["directory"].unique():
            if not os.path.exists(directory):
                os.makedirs(directory)
            fake_fname = "5500000007_40X_20181010_2-Scene-17-P27-B04.czi"
            fpath = os.path.join(directory, fake_fname)

            arr = np.random.randint(
                low=0, high=2 ** 16 - 1, size=(1, 1, 2, 3, 4), dtype=np.uint16
            )
            writer = OmeTifWriter(fpath, overwrite_file=True)
            writer.save(arr)

            # Path(fpath).touch()

    # find the actual czis and filter for ones that are the right shape
    df = find_czis(df)
    df = filter_czis(df)
