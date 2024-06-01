from flameai import eval_binary, Metric
from flameai.cmd import header

y_true = [0, 0, 0, 1, 0, 1, 0, 1, 1, 0]
y_pred = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

# Evaluate the performance of a binary classification model
header('set threshold to 0.5')
eval_binary(y_true, y_pred, threshold=0.5)

header('find a threshold to maximize precision')
eval_binary(y_true, y_pred, metric=Metric.PRECISION)

header('find a threshold to maximize recall')
eval_binary(y_true, y_pred, metric=Metric.RECALL)

header('find a threshold to maximize f1 score')
eval_binary(y_true, y_pred, metric=Metric.F1_SCORE)

header('ret = True, verbose = 0')
y_label, threshold = eval_binary(y_true,
                                 y_pred,
                                 metric=Metric.F1_SCORE,
                                 ret=True,
                                 verbose=0)
print(f'y_label: {y_label}')
print(f'threshold: {threshold:.3f}')
