from app import app
import io
import random
from flask import Response, session, send_file
import matplotlib
matplotlib.use('Agg') # issue when running locall if this isn't in here.
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import matplotlib.style as style
import matplotlib.pylab as pylab
import pandas as pd
import numpy as np
from flask import g, session
from bs4 import BeautifulSoup


def thousands(x, pos):
    return '$%1.fk' % (x*1e-3)

def italicize_texts(string, texts):
    for text in texts:
        for word in text.split(' '):
            string = string.replace(word,'$\it{{' + word+ '}}$' )
    return string

def set_sizes():
    params = {'legend.fontsize': 'medium',
         'axes.labelsize': 'medium',
         'axes.titlesize':'medium',
         'xtick.labelsize':'medium',
         'ytick.labelsize':'medium'}
    pylab.rcParams.update(params)

def create_whatif_plot(ax, x, y, hline, hline_label, marker, x_label, y_label):
    set_sizes()

    y_max = max(0, max(y))
    y_min = min(0, min(y))
    y_avg = y.mean()
    y_pad = 0.1 * y_avg
    y_range = y_max + y_pad - y_min

    arrow_length = y_range * 0.3

    x_max = max(x)
    x_min = min(x)
    x_avg = x.mean()
    x_range = x_max - x_min
    x_pad = 0.05 * x_range

    y_label_small = 'Final investment value'

    ax.set(xlabel = x_label, ylabel = y_label_small, 
        ylim = (y_min, y_max + y_pad))

    if hline:
        ax.axhline(y = hline, color='k', linestyle='--')
        ax.annotate('Final investment value\nRent home', xy=(x_max - x_pad, hline), xytext=(x_max - x_pad, hline - arrow_length),
                arrowprops=dict(facecolor='green', shrink=0.05), horizontalalignment = 'right')

    ax.annotate('{}\n(current)'.format(y_label), xy=marker, xytext=(marker[0], marker[1] - arrow_length ),
            arrowprops=dict(facecolor='green', shrink=0.05), horizontalalignment = 'center')
    
    ax.scatter(x = marker[0], y = marker[1], s = 40, color = 'red', zorder=10)

    ax.yaxis.set_major_formatter(FuncFormatter(thousands))
    if x_avg >= 500:
        ax.xaxis.set_major_formatter(FuncFormatter(thousands))

    ax.plot(x, y, label = y_label)
    ax.legend(loc = 'lower left')
    return ax

def normalise_svg_plot_size(img):
    soup = BeautifulSoup(img.read(), "html.parser")
    soup.find('svg')['width'] = "100%"
    del soup.find('svg')['height']
    return str(soup)

# For use when generating an svg file (without a file or route, use the raw svg xml code)
def create_whatif_df_svg(page, variable, marker_y, y_label, hline = None, hline_label = None):
    dfs = session[page]['whatif_dfs']
    df = pd.read_json(dfs[variable])
    plt.close('all') # clear plot from previously to save memory
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(1, figsize = (9, 5), dpi = 110)
    create_whatif_plot(
        ax = ax,
        x = df[variable], 
        y = df['Final investment value'], 
        hline = session[page][hline] if hline else None,
        hline_label = hline_label,
        marker = (session[page]['model_inputs'][variable], session[page][marker_y]),
        x_label = session[page]['labels'][variable],
        y_label = y_label
    )
    canvas = FigureCanvas(fig)
    img = io.StringIO()
    fig.savefig(img, format = 'svg')
    img.seek(0)
    return normalise_svg_plot_size(img)