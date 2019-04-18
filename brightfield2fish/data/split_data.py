import os
import pandas as pd
from pytorch_learning_tools.utils.hashsplit import hashsplit


def split_and_save(
    csv_path="/allen/aics/modeling/data/brightfield2fish/preprocessed/data_by_images_normalized.csv",
    split_col="file",
    save_dir="data",
    splits={"train": 0.7, "valid": 0.15, "test": 0.15},
    seed=0,
):

    df = pd.read_csv(csv_path)
    splits = hashsplit(df[split_col], splits=splits, salt=seed)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for k, v in splits.items():
        df_subset = df.iloc[v, :].reset_index(drop=True)
        fname = "{}.csv".format(k)
        fpath = os.path.join(save_dir, fname)
        df_subset.to_csv(fpath, index=False)
