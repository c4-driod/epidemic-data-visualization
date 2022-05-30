from tkinter import *
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas

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


def get_mpl_canvas(master, figure):
    return FigureCanvasTkAgg(figure=figure, master=master)


def get_tk_mpl_widget(mpl_canvas):
    widget = mpl_canvas.get_tk_widget()
    mpl_canvas.draw()
    return widget


def print_x_y(e):
    if e.xdata:
        print('xdata', pandas.Period(ordinal=int(e.xdata), freq='D'))
        print('ydata', e.ydata)


test_data = {
    'date': ['2021-01-02', '2021-01-04', '2021-02-04'],
    'rate': [0.1, 0.5, 0.6]
}

df = pandas.DataFrame(test_data)
df.loc[:, 'date'] = pandas.to_datetime(df.loc[:, 'date'])
print('type(df date):', type(df.loc[0, 'date']))


r = Tk()
fig, ax = get_figure_and_ax()
canvas = get_mpl_canvas(r, fig)
canvas.mpl_connect('motion_notify_event', print_x_y)
ax.plot(df['date'], df['rate'])
canvas.draw()



get_tk_mpl_widget(canvas).pack(fill=BOTH, expand=True)


r.mainloop()
