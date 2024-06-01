from flameai.metrics import eval_binary, eval_regression, Metric


y_true = [0, 0, 0, 1, 0, 1, 0, 1, 1, 0]
y_pred = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


def test_eval_binary_with_threshold():
    """set threshold by hand."""
    y_label, _ = eval_binary(y_true, y_pred, threshold=0.5, ret=True)
    assert y_label == [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]


def test_eval_binary_maximize_precision():
    """Find a threshold to maximize precision."""
    eval_binary(y_true, y_pred, metric=Metric.PRECISION)


def test_eval_binary_maximize_recall():
    """Find a threshold to maximize recall."""
    eval_binary(y_true, y_pred, metric=Metric.RECALL)


def test_eval_binary_maximize_f1_score():
    """Find a threshold to maximize f1_score."""
    eval_binary(y_true, y_pred, metric=Metric.F1_SCORE)


def test_eval_regression():
    """Evaluates the performance of a regression model."""
    y_true = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
    y_pred = [0.11, 0.23, 0.29, 0.45, 0.50, 0.59, 0.72, 0.76, 0.94, 1.00]
    eval_regression(y_true, y_pred)
