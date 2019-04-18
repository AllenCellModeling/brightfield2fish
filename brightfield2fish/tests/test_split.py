import os
from brightfield2fish.dataplit_data import split_and_save


def test_split_data():
    dirname = os.path.dirname(__file__)
    csv_path = os.path.join(
        os.path.dirname(os.path.dirname(dirname)),
        "data",
        "data_by_images_normalized.csv",
    )

    split_and_save(csv_path)
