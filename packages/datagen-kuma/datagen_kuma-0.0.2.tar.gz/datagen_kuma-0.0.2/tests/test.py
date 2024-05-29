import os

from icecream import ic
import pandas as pd
from datagen_kuma.datagen import DataGen


data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data"
)


def test_datagen():
    df = pd.read_csv(os.path.join(data_dir, "events.csv"))
    series_len = len(df.timestamp)
    df["test_datetime"] = pd.date_range("2020-01-01", "2024-05-28", periods=series_len)
    true_count = int(series_len * 0.7)
    false_count = series_len - true_count
    df["test_bool"] = ([True] * true_count) + ([False] * false_count)
    df["test_object"] = [[1, 2, 3, 4, 5]] * series_len
    ic(df.info())
    ic(df)

    generate_data_count = 1000000
    datagen = DataGen(df=df, count=generate_data_count)
    ic(datagen.column_types)
    ic(datagen.column_types.values())
    ic(datagen.statistics)

    generated_df = datagen.dataframe
    ic(generated_df.info())
    ic(generated_df)

    assert len(generated_df.timestamp) == generate_data_count
    assert df.columns.tolist().sort() == generated_df.columns.tolist().sort()