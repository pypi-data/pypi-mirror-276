from flameai.preprocessing import DataLoader, gen_scale_pos_weight, label_encoder
import pandas as pd


def test_label_encoder():
    df = pd.DataFrame({'a': ['a', 'b', 'c', 'a', 'b', 'c'],
                       'b': [1, 2, 3, 2, 1, 0]})
    result = label_encoder(df).reset_index(drop=True)
    assert result['a'].to_list() == [0, 1, 2, 0, 1, 2]
    assert result['b'].to_list() == [1, 2, 3, 2, 1, 0]


def test_gen_scale_pos_weight():
    y_train = pd.Series([0, 1, 0, 0, 1, 0, 0])
    result = gen_scale_pos_weight(y_train)
    assert result == 2.5


def test_data_loader():
    lst1 = [1, 2, 3, 4, 5, 6]
    dt = DataLoader(lst1)
    assert [e for e in dt] == lst1
    assert [e for e in dt] == lst1

    lst2 = [1, 2, 3]
    dt.data = lst2
    assert [e for e in dt] == lst2
    assert dt.data == lst2
