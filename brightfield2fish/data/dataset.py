import warnings
import numpy as np
from torch.utils.data import Dataset
from aicsimageio import AICSImage
from .utils import normalize_image_zero_one, normalize_image_center_scale


class FishDataframeDataset(Dataset):
    """Dataset class for Brghtfield -> FISH prediction"""

    def __init__(
        self,
        df,
        channel_content="DNA",
        normalize=False,
        math_dtype=np.float64,
        out_dtype=np.float32,
    ):
        """
        Args:
            df (pandas.DataFrame): data_by_channels.csv dataframe output by preprocess_csv.py
            channel_content (str): Name of the probe we want to predict from Brightfield, e.g. "DNA", "BMPER", etc
        """
        self.df = df[df["channel_content"] == channel_content].reset_index(drop=True)[
            ["file", "channel_index"]
        ]
        self._normalize = normalize
        self._math_dtype = math_dtype
        self._out_dtype = out_dtype

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        brightfield_channel_index = 0
        target_channel_index = row["channel_index"]
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=FutureWarning)
            image = AICSImage(row["file"])
        bright = image.get_image_data("ZYX", T=0, C=brightfield_channel_index)
        target = image.get_image_data("ZYX", T=0, C=target_channel_index)
        if self._normalize:
            bright = normalize_image_center_scale(bright.astype(self._math_dtype))
            target = normalize_image_zero_one(target.astype(self._math_dtype))
        return {
            "Brightfield": bright.astype(self._out_dtype),
            "Target": target.astype(self._out_dtype),
        }
