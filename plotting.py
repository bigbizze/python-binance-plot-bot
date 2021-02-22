import io

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def get_line_plot(symbol: str, data) -> io.BytesIO:
    sns.set_theme(style="darkgrid")
    sns.set(rc={'figure.figsize': (19.2, 10.8)})
    svm = sns.lineplot(x="time (EST)", y="price", data=data)
    svm.set_title(symbol.upper())
    ax = plt.gca()
    x_ticks = ax.get_xticks()
    ax.set_xticklabels([pd.to_datetime(tm, unit='ms').strftime("%H:%M:%S:%f")[:-3] for tm in x_ticks], rotation=50)
    fig = svm.get_figure()
    pic_io_bytes = io.BytesIO()
    fig.savefig(pic_io_bytes, format='jpg')
    pic_io_bytes.seek(0)
    plt.clf()
    return pic_io_bytes



