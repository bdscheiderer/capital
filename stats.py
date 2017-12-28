# program to test the stats function

import sqlite3
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import mpld3


def get_stats():
    # open connect to database
    conn = sqlite3.connect('capital_db.sqlite')
    cur = conn.cursor()
    # get score data for 20 and 50 questions quizs
    cur.execute('SELECT score FROM Scores WHERE quiz=20')
    d20 = cur.fetchall()
    dt = np.dtype('int')
    dat20 = np.asarray(d20, dt)
    dat20 = np.reshape(dat20, -1)
    cur.execute('SELECT score FROM Scores WHERE quiz=50')
    d50 = cur.fetchall()
    dat50 = np.asarray(d50, dt)
    dat50 = np.reshape(dat50, -1)
    dat50.ndim
    dat50.shape
    # calculate stats
    dat20avg = get_average(dat20)
    dat50avg = get_average(dat50)
    # create histograms
    dat20plot = get_plot(dat20, 21, 0, 20)
    dat50plot = get_plot(dat50, 51, 0, 50)
    # close database connection
    cur.close()
    conn.close()
    print(type(dat20plot))
    return dat20avg, dat20plot, dat50avg, dat50plot

def get_average(dat):
    dict = {}
    dict['mean'] = int(np.mean(dat) + 0.5)
    dict['median'] = int(np.median(dat) + 0.5)
    dict['std'] = int(np.std(dat) + 0.5)
    return dict

def get_plot(dat, bwidth, bmin, bmax):
    if bwidth <50:
        step = 1
    else:
        step = 2
    counts = np.bincount(dat)
    fig, ax = plt.subplots()
    ax.bar(range(bwidth), counts, width=1, align='center')
    ax.set(xticks=range(0, bwidth, step), xlim=[-1, bwidth])
    plt.title("Histogram of Quiz Scores")
    plt.show()
    chart = mpld3.fig_to_html(fig)
    return chart

def main():
    get_stats()

if __name__ == '__main__':
    main()
    print('Done')
