import os
import warnings
import concurrent
import pandas as pd
from tqdm import tqdm
from aicsimageio import AICSImage


def parse_plate_well(path):
    dirname, fname = os.path.split(path)
    plate = dirname.split(os.path.sep)[6]
    well, ext = os.path.splitext(fname.split("_")[-1].split("-")[4])
    return {"plate": plate, "well": well}


def find_czis(df):
    czis = {d: os.listdir(d) for d in df["directory"].unique()}
    czis = {k: [f for f in v if ".czi" in f] for k, v in czis.items()}
    czis = [[os.path.join(k, f) for f in v] for k, v in czis.items()]
    czis = [item for sublist in czis for item in sublist]
    df_czi = pd.DataFrame([{**parse_plate_well(czi), "file": czi} for czi in czis])
    df = df.merge(df_czi, how="inner")
    df = df[~df["file"].str.contains("FORFUN")]
    return df


def image_shape(czi_path):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        image = AICSImage(czi_path)
    return {"file": czi_path, "shape": image.shape}


def filter_czis(df, shape=(1, 5, 50, 624, 924)):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        shapes = list(tqdm(executor.map(image_shape, df["file"]), total=len(df)))
    full_ims = [x["file"] for x in shapes if x["shape"] == shape]
    return df[df["file"].isin(full_ims)].reset_index(drop=True)


if __name__ == "__main__":
    # load original csv and fix some typos
    df = pd.read_csv("data.csv")
    df = df.rename(index=str, columns={"link_to_data": "directory"})
    df["plate"] = df["plate"].astype(str)
    df = df.replace({"PRSS35": "PRSS3", "COL2A": "COL2A1"})

    # find the actual czis and filter for ones that are the right shape
    df = find_czis(df)
    df = filter_czis(df)

    # save a filtered copy
    df.to_csv("data_by_images.csv", index=False)

    # melt the dataframe so each row is a seprate channel
    df = df.rename(
        index=str,
        columns={
            "probe_488": "channel_1",
            "probe_561": "channel_2",
            "probe_638": "channel_3",
        },
    )
    df["channel_0"] = "Brightfield"
    df["channel_4"] = "DNA"
    df = pd.melt(
        df,
        id_vars=[c for c in df.columns if "channel_" not in c],
        value_vars=[c for c in df.columns if "channel_" in c],
        var_name="channel_index",
        value_name="channel_content",
    )
    df["channel_index"] = df["channel_index"].str[-1].astype(int)
    df = df[df["channel_content"].astype(str) != "nan"]

    # save it
    df.to_csv("data_by_channels.csv", index=False)
