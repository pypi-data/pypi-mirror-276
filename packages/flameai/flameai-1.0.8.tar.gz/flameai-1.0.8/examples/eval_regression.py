import flameai

y_true = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
y_pred = [0.11, 0.23, 0.29, 0.45, 0.50, 0.59, 0.72, 0.76, 0.94, 1.00]

# Evaluate the performance of a linear regression model
flameai.eval_regression(y_true, y_pred)
