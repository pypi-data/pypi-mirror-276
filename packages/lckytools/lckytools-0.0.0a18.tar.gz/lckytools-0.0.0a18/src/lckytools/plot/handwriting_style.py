import matplotlib.pyplot as plt


def handwriting_style():
    plt.xkcd(randomness=2)
    plt.rcParams.update({"font.family": ["xkcd Script", "xkcd Script", "Comic Neue", "Comic Sans MS"]})
