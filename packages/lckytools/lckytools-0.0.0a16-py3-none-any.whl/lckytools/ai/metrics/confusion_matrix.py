import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix as _confusion_matrix


def confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    ignore_diagonal: bool = True,
) -> np.ndarray:
    cm = _confusion_matrix(y_true, y_pred)
    cm = cm.astype("float")
    if ignore_diagonal:
        for i in range(cm.shape[0]):
            cm[i][i] = np.nan
    return cm


def plot_confusion_matrix(confusion_matrix: np.ndarray) -> None:
    size = confusion_matrix.shape[0]
    df_cm = pd.DataFrame(
        confusion_matrix,
        index=list(range(size)),
        columns=list(range(size)),
    )

    sns.heatmap(df_cm, annot=True, fmt="0.0f")
    plt.xlabel("Predicted Class", fontsize=14)
    plt.ylabel("Actual Class", fontsize=14)
    plt.title("Confusion Matrix", fontsize=16)
