from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature


mpl.rcParams['font.family'] = 'SimHei'
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False


class MapDrawer:
    # 读取CN-border-La.dat文件
    with open('CN-border-La.dat') as src:
        context = src.read()
        blocks = [cnt for cnt in context.split('>') if len(cnt) > 0]
        borders = [np.fromstring(block, dtype=float, sep=' ') for block in blocks]
    figure = plt.figure()
    # 设置投影类型和经纬度
    ax = plt.axes(projection=ccrs.LambertConformal(central_latitude=90,
                                                   central_longitude=105))
    # 画海，陆地，河流，湖泊
    ax.add_feature(cfeature.OCEAN.with_scale('110m'))
    ax.add_feature(cfeature.LAND.with_scale('110m'))
    ax.add_feature(cfeature.RIVERS.with_scale('110m'))
    ax.add_feature(cfeature.LAKES.with_scale('110m'))

    # 画经纬度网格
    ax.gridlines(linestyle='--')
    # 框出区域
    ax.set_extent([80, 130, 13, 55])

    # 画国界
    for line in borders:
        ax.plot(line[0::2], line[1::2], '-', color='grey', transform=ccrs.Geodetic())

    def __init__(self, **kwargs):
        self.master = kwargs['master']
        self.canvas = FigureCanvasTkAgg(self.figure, self.master)
        self.widget = self.canvas.get_tk_widget()

    def get_widget(self):
        return self.widget


r = Tk()
m = MapDrawer(master=r)
w = m.get_widget()
w.pack(fill=BOTH, expand=True)

r.mainloop()
