import numpy as np
from tkinter import *
import ctypes


ctypes.windll.shcore.SetProcessDpiAwareness(True)
#读取CN-border-La.dat文件
with open('CN-border-La.dat') as src:
    context = src.read()
    blocks = [cnt for cnt in context.split('>') if len(cnt) > 0]
    borders = [np.fromstring(block, dtype=float, sep=' ') for block in blocks]

r = Tk()
winx, winy = 1500, 800
r.geometry('%dx%d+100+50' % (winx, winy))
ca = Canvas(r)
ca.pack(fill=BOTH, expand=True)

#对数据进行处理
min_ = [1000, 1000]
max_ = [0, 0]
for line in borders:
    max_[0] = max(max_[0], max(*line[0::2]))
    min_[0] = min(min_[0], min(*line[0::2]))
    max_[1] = max(max_[1], max(*line[1::2]))
    min_[1] = min(min_[1], min(*line[1::2]))

LARGE = int(min(winx/(max_[0] - min_[0]), winy/(max_[1] - min_[1])))

print('max_:',max_)
print('LARGE:',LARGE)

for line in borders:
    for i in range(int(len(line)/2)):
        line[2*i] = LARGE*(line[2*i] - min_[0])
        line[2*i+1] = LARGE*(max_[1] - line[2*i+1])

for line in borders:
    ca.create_line(*line, width=3)

print('画完')
r.mainloop()

