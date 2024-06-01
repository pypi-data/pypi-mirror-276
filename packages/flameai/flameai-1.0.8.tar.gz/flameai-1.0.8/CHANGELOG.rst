.. currentmodule:: flameai

Version 1.0.8
-------------

Released 2024-06-01

-   Fix an error caused by the ``hive_cli`` function


Version 1.0.7
-------------

Released 2024-05-31

-   Added two optional arguments ``--conf``, ``--print`` to the ``hive_cli`` function.


Version 1.0.6
-------------

Released 2024-05-25

-   Added support for binary classification model evaluation.
    -   Allows specifying a threshold for model output probabilities.
    -   If no threshold is provided, FlameAI will automatically search for the optimal
        threshold based on an objective function (e.g., maximizing precision).
-   Added support for linear regression model evaluation.
-   Added support for data preprocessing.
    -   Convert categorical labels into numeric format.
    -   Calculate the scaling factor for an imbalanced dataset.
    -   Implement a simple DataLoader.
-   Added support for plotting ROC curves and confusion matrices.
-   Added support for a command-line tool.
    -   Check if Python, Hive and PyTorch are installed in the current env.
    -   Hive command-line tool to execute an HQL file and save the result to a CSV file
        with the same name as HQL file.
- Run nox tests using GitHub Actions.
- Added some examples.
- Removed several modules from ``__all__`` to fix the issue of slow loading of FlameAI.
- Removed torch from ``pyproject.toml``'s dependencies.


Version 1.0.0
-------------

Released 2024-05-23

-   Initial release.
