from flameai.metrics import Metric
from flameai.train import gen_threshold, gen_threshold_cdf


y_true = [0, 0, 0, 1, 0, 1, 0, 1, 1, 0]
y_pred = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


def test_gen_threshold():
    gen_threshold(y_true=y_true,
                  y_pred=y_pred,
                  metric=Metric.PRECISION,
                  n_trials=200)
    gen_threshold(y_true=y_true,
                  y_pred=y_pred,
                  metric=Metric.RECALL,
                  n_trials=200)
    gen_threshold(y_true=y_true,
                  y_pred=y_pred,
                  metric=Metric.ACCURACY,
                  n_trials=200)
    gen_threshold(y_true=y_true,
                  y_pred=y_pred,
                  metric=Metric.F1_SCORE,
                  n_trials=200)


def test_gen_threshold_cdf():
    result = gen_threshold_cdf(y_pred=y_pred, rate=0.4)
    assert result == 0.55
