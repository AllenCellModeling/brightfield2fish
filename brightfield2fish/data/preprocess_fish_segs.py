"""
This script takes the provisinoal 2D fish segmentations and matches them with 3D brightfield data.
Not cleaning this up since the whole process should really be pulls from a database.
"""


if __name__ == "__main__":

    import os
    from pathlib import Path
    import numpy as np
    import pandas as pd

    PAR_DIR = "/allen/aics/microscopy/Data/fish/mip_with_seg"
    FISH_SEG_CSV = "fish_seg.csv"
    SEG_EXPORT_CSV = "seg_export.csv"

    fpath_fish_seg_csv = Path(PAR_DIR).joinpath(FISH_SEG_CSV)
    fpath_fish_export_csv = Path(PAR_DIR).joinpath(SEG_EXPORT_CSV)

    df_seg = pd.read_csv(fpath_fish_seg_csv)
    df_exp = pd.read_csv(fpath_fish_export_csv)

    idvars = ["plate", "cell_line", "cell_age", "well"]

    df_bf = pd.DataFrame({"brightfield filename": np.unique(df_exp[["FileName_BF"]])})
    df_bf["scene id"] = (
        df_bf["brightfield filename"].str.split("-OME").str[0].str.split(".").str[0]
    )
    df_bf["plate"] = df_bf["scene id"].str.split("_").str[0]
    df_bf["well"] = df_bf["scene id"].str.split("-").str[-1]

    df_probe = pd.melt(
        df_seg,
        id_vars=idvars,
        value_vars=["probe_488", "probe_638", "probe_561"],
        var_name="wavelength",
        value_name="probe name",
    ).dropna()
    df_probe["wavelength"] = df_probe["wavelength"].str.split("_").str[-1].astype(int)

    df_dot = pd.melt(
        df_seg,
        id_vars=idvars,
        value_vars=["dot_488", "dot_638", "dot_561"],
        var_name="wavelength",
        value_name="dot value",
    ).dropna()
    df_dot["wavelength"] = df_dot["wavelength"].str.split("_").str[-1].astype(int)

    df_tidy = df_probe.merge(df_dot, how="inner", on=idvars + ["wavelength"])
    df_tidy["plate"] = df_tidy["plate"].astype(str)
    df_tidy["directory"] = (
        PAR_DIR
        + os.path.sep
        + (df_tidy["plate"].astype(str) + "_" + df_tidy["cell_line"]).str.replace(
            "_0", ""
        )
    )
    df_tidy["out subdir"] = (
        df_tidy["directory"]
        + os.path.sep
        + "out_"
        + df_tidy["wavelength"].astype(str)
        + "_"
        + df_tidy["dot value"].astype(str)
    )
    df_tidy = df_tidy.merge(df_bf, on=["plate", "well"], how="inner")

    ls_out = {
        d: os.listdir(os.path.join(PAR_DIR, d)) for d in df_tidy["directory"].unique()
    }
    ls_out = {d: [s for s in subdirs if "out" in s] for d, subdirs in ls_out.items()}
    ls_out = [
        [os.path.join(PAR_DIR, d, s) for s in subdirs] for d, subdirs in ls_out.items()
    ]
    ls_out = [item for sublist in ls_out for item in sublist]

    seg_tiff_list = [
        [os.path.abspath(tiff) for tiff in os.listdir(lso)] for lso in ls_out
    ]
    seg_tiff_list = [item for sublist in seg_tiff_list for item in sublist]

    df_tidy["fish segmentation filename"] = ""
    for i, row in df_tidy.iterrows():
        seg_tiff = [
            tiff for tiff in os.listdir(row["out subdir"]) if row["scene id"] in tiff
        ]
        assert len(seg_tiff) == 1
        df_tidy.loc[i, "fish segmentation filename"] = seg_tiff[0]

    df_3d = pd.read_csv("../data/data_by_images.csv")
    df_3d["scene id"] = df_3d["file"].apply(
        lambda x: os.path.splitext(os.path.basename(x))[0]
    )

    df_tidy["fish segmetation path"] = (
        df_tidy["out subdir"] + os.path.sep + df_tidy["fish segmentation filename"]
    )
    df_final = (
        df_tidy.drop(
            [
                "directory",
                "out subdir",
                "brightfield filename",
                "fish segmentation filename",
            ],
            axis=1,
        )
        .merge(df_3d[["file", "scene id"]], how="inner", on="scene id")
        .drop(["scene id"], axis=1)
    )

    df_final.to_csv("../data/data_by_images_with_fish_segmentations.csv", index=False)
