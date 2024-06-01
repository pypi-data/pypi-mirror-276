import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_correlations(dataframe):
    corr_features = dataframe.columns
    cc = np.corrcoef(dataframe[corr_features], rowvar=False)
    plt.figure(figsize=(11, 11))
    sns.heatmap(
        cc, center=0, cmap="coolwarm", annot=True, fmt=".1f", xticklabels=corr_features, yticklabels=corr_features
    )
    plt.title("Correlation matrix")
    plt.show()
