from flameai.plot import confusion_matrix

y_true = [0, 1, 1, 0, 1, 1, 0, 0, 0, 1]
y_label = [1, 1, 1, 0, 1, 0, 0, 0, 1, 1]

confusion_matrix(y_true, y_label)
