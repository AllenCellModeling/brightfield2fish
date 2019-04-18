import warnings
import numpy as np
import pandas as pd
from scipy.ndimage.interpolation import zoom
import torch
from torch.utils.data import Dataset
from aicsimageio import AICSImage
from .utils import RandomCrop3D, normalize


class FishDataframeDatasetTIFF(Dataset):
    """
    Dataset class for Brghtfield -> FISH prediction that reads single channel tiffs.
    """

    def __init__(
        self,
        df,
        csv=False,
        channel_content="DNA",
        resize_original=None,
        random_crop=None,
        math_dtype=np.float64,
        out_dtype=np.float32,
        output_torch=True,
        channel_dim=True,
        return_tuple=True,
    ):
        """
        Args:
            df (pandas.DataFrame): data_by_channels.csv dataframe output by preprocess_csv.py
            channel_content (str): Name of the ll probe we want to predict from Brightfield, e.g. "DNA", "BMPER", etc
        """

        if csv:
            df = pd.read_csv(df)

        df_channel = df[df["channel_content"] == channel_content].reset_index(
            drop=True
        )[["file", "normalized_single_channel_image"]]

        df_brightf = df[
            (df["channel_content"] == "Brightfield")
            & (df["file"].isin(df_channel["file"]))
        ].reset_index(drop=True)[["file", "normalized_single_channel_image"]]

        df_channel.rename(
            {"normalized_single_channel_image": "Target"}, axis="columns", inplace=True
        )
        df_brightf.rename(
            {"normalized_single_channel_image": "Brightfield"},
            axis="columns",
            inplace=True,
        )

        self.df = df_brightf.merge(df_channel, how="inner", on="file")[
            ["Brightfield", "Target"]
        ].reset_index(drop=True)

        self._resize_original = resize_original
        self._random_crop = random_crop
        self._math_dtype = math_dtype
        self._out_dtype = out_dtype
        self._output_torch = output_torch
        self._channel_dim = channel_dim
        self._return_tuple = return_tuple

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):

        row = self.df.iloc[idx]

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=FutureWarning)
            out = {
                k: AICSImage(row[k]).get_image_data("ZYX")
                for k in ("Brightfield", "Target")
            }

        if self._resize_original is not None:
            out = {
                k: zoom(v.astype(self._math_dtype), self._resize_original).astype(
                    self._out_dtype
                )
                for k, v in out.items()
            }

        out = {
            k: normalize(v.astype(self._math_dtype), content=k).astype(self._out_dtype)
            for k, v in out.items()
        }

        if self._random_crop is not None:
            randomcropper = RandomCrop3D(out["Brightfield"], *self._random_crop)
            out = {k: randomcropper.crop(v) for k, v in out.items()}

        if self._output_torch:
            out = {k: torch.from_numpy(v) for k, v in out.items()}

        if self._channel_dim:
            out = {k: torch.unsqueeze(v, 0) for k, v in out.items()}

        if self._return_tuple:
            out = (out["Brightfield"], out["Target"])

        return out
