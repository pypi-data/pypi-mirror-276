import matplotlib.pyplot as plt


def plot_embedding(embedding, target, title, cmap="summer"):
    plt.scatter(
        embedding[:, 0],
        embedding[:, 1],
        s=1,
        c=target,
        cmap=cmap,
    )
    plt.gca().set_aspect("equal", "datalim")
    plt.title(title, fontsize=18)
    plt.show()
