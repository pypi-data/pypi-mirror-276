from flameai.plot import roc_curve

y_true = [0, 1, 1, 0, 1, 1, 0, 0, 1, 1]
y_score = [0.1, 0.4, 0.35, 0.8, 0.15, 0.35, 0.2, 0.7, 0.05, 0.9]

roc_curve(y_true, y_score)
