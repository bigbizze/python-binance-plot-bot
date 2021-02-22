import base64
import io
import random
import time
from datetime import datetime

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def get_line_plot(symbol: str, data) -> io.BytesIO:
    # sns.lineplot(x="time", y="price", data=data)
    # fig = sns.get_figure()
    # # plt.show()
    # print()
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
    # return base64.b64encode(pic_io_bytes.read())
    return pic_io_bytes


# if __name__ == '__main__':
#     prices = []
#     times = []
#     for i in range(15):
#         prices.append(i + random.random())
#         times.append(datetime.timestamp(datetime.now()))
#         time.sleep(0.001)
#     svm = sns.pointplot(x="time", y="price", data=pd.DataFrame({"price": prices, "time": times}), dodge=False)
#     ax = plt.gca()
#     x_ticks = ax.get_xticks()
#     ax.set_xticklabels([pd.to_datetime(tm, unit='ms').strftime("%H:%M:%S:%f")[:-3] for tm in x_ticks], rotation=50)
#     plt.show()
    # fig = svm.get_figure()
    # pic_io_bytes = io.BytesIO()
    # fig.savefig(pic_io_bytes, format='jpg')
    # pic_io_bytes.seek(0)
    # pic_hash = base64.b64encode(pic_io_bytes.read())



