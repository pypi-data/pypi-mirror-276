import flameai

y_true = [0, 0, 0, 1, 0, 1, 0, 1, 1, 0]
y_pred = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

# Evaluate the performance of a binary classification model
flameai.eval_binary(y_true, y_pred, threshold=0.5)
