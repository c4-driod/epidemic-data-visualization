import pandas as pd
import numpy as np
from tkinter import *
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import ctypes


#  基本配置
mpl.use('Agg')
ctypes.windll.shcore.SetProcessDpiAwareness(True)
mpl.rcParams['font.family'] = 'SimHei'
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False


fig = plt.figure(figsize=(5, 4), tight_layout=True)
ax = fig.add_subplot(111)
ax.plot(np.arange(0, 100), np.arange(0, 2e5, 2000))
ax.set_ylabel('ylabel')
ax.set_xlabel('xlabel')


r = Tk()


canvas = FigureCanvasTkAgg(fig, master=r)
canvas.draw()
canvas.get_tk_widget().pack(fill=BOTH, expand=True)


def change():
    new_ar = np.arange(0, 1e5, 1000)
    ax.plot(new_ar)
    canvas.draw()
    r.update()


Button(r, text='qwe', command=change).pack()

r.mainloop()
