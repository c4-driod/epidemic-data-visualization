import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from cartopy import crs


#  基本配置
mpl.use('Agg')
mpl.rcParams['font.family'] = 'SimHei'
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False


def get_figure_and_ax():
    figure = Figure(tight_layout=True)
    ax = figure.add_subplot(111)
    ax.spines[['left', 'top', 'right']].set_visible(False)
    return figure, ax


def get_figure_and_ax_map():
    figure = Figure(tight_layout=True)
    ax = figure.add_subplot(111, projection=crs.PlateCarree())
    return figure, ax


def get_mpl_canvas(master, figure):
    return FigureCanvasTkAgg(figure=figure, master=master)


def get_tk_mpl_widget(mpl_canvas):
    widget = mpl_canvas.get_tk_widget()
    mpl_canvas.draw()
    return widget


def get_tk_mpl_widget_with_toolbar(master, mpl_canvas):
    tool_bar = NavigationToolbar2Tk(mpl_canvas, master)
    tool_bar.update()
    return mpl_canvas.get_tk_widget()






