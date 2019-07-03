import os
from brightfield2fish.data.split_data import split_and_save


def test_split_data():
    dirname = os.path.dirname(__file__)
    csv_path = os.path.join(
        os.path.dirname(os.path.dirname(dirname)),
        "data",
        "data_by_images_normalized.csv",
    )

    if os.path.exists(os.path.join("tmp_tests", "data", "splits")):
        for split in ("train", "test", "valid"):
            os.remove(
                os.path.join("tmp_tests", "data", "splits", "{}.csv".format(split))
            )
        os.remove(os.path.join("tmp_tests", "data", "splits", "splits.json"))
        os.rmdir(os.path.join("tmp_tests", "data", "splits"))

    split_and_save(csv_path)
