from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'SimHei'
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False


class PlotFrame(Frame):
    # 图像
    figure = plt.figure()
    # 当前在画的图
    now_figure = figure.add_subplot()
    # 作图函数
    plot_funcs = {
        'line': now_figure.plot,
        'scatter': now_figure.scatter,
        'bar': now_figure.bar,
        'pie': now_figure.pie,
        'hist': now_figure.hist
    }

    def set_dpi(self, num):
        self.figure.set_dpi(num)

    def clear(self):
        self.figure.clear()

    def draw_scatter(self):
        x = ['中国', '美国', '意大利', '日本', '家喷']
        y = [9, 6, 4, 3, 2]
        self.now_figure.scatter(x, y, color='red')
        self.canvas.draw()

    def draw_line(self):
        x = ['中国', '美国', '意大利', '日本', '家喷']
        y = [9, 6, 4, 3, 2]
        self.now_figure.plot(x, y)
        self.canvas.draw()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.master = kw['master']
        # 画板
        self.canvas = FigureCanvasTkAgg(self.figure, self.master)
        self.widget = self.canvas.get_tk_widget()

    def get_widget(self):
        return self.widget


if __name__ == '__main__':
    r = Tk()
    p = PlotFrame(master=r)
    w = p.get_widget()
    w.pack(fill=BOTH, expand=True)
    dx = [1, 2, 4, 6]
    dy = [4, 2, 9, 1]
    p.draw_scatter()
    r.mainloop()
