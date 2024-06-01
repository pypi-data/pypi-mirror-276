from flameai.mining import value_counts
import pandas as pd


def test_value_counts():
    df = pd.DataFrame({'a': [5, 1, 3, 4, 3, 6, 6, 8, 8, 10],
                       'b': [1, 0, 3, 7, 5, 6, 7, 11, 5, 10],
                       })
    result = value_counts(df)
    assert result.equals(pd.DataFrame({'col_name': ['a', 'b'],
                                       'val_cnt': [7, 8]}))
