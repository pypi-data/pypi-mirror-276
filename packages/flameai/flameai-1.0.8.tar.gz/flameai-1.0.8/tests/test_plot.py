from unittest import mock

from flameai.plot import confusion_matrix, roc_curve


def test_roc_curve() -> None:
    y_true = [0, 1, 1, 0, 1, 1, 0, 0, 1, 1]
    y_score = [0.1, 0.4, 0.35, 0.8, 0.15, 0.35, 0.2, 0.7, 0.05, 0.9]
    with mock.patch('matplotlib.pyplot.show'):
        roc_curve(y_true, y_score)


def test_confusion_matrix() -> None:
    y_true = [0, 1, 1, 0, 1, 1, 0, 0, 0, 1]
    y_label = [1, 1, 1, 0, 1, 0, 0, 0, 1, 1]
    with mock.patch('matplotlib.pyplot.show'):
        confusion_matrix(y_true, y_label)
