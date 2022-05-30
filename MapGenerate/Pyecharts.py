import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


#读取CN-border-La.dat文件
with open('CN-border-La.dat') as src:
    context = src.read()
    blocks = [cnt for cnt in context.split('>') if len(cnt) > 0]
    borders = [np.fromstring(block, dtype=float, sep=' ') for block in blocks]
#设置画图各种参数
fig = plt.figure(figsize=[8, 8])
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
# for line in borders:
#     ax.plot(line[0::2], line[1::2], '-', color='grey',transform=ccrs.Geodetic())


c = 0
for i in range(len(borders)):
    print(len(borders[i]))
    if len(borders[i]) <=1000:
        continue
    else:
        c += 1
    ax.plot(borders[i][0::2], borders[i][1::2], '-', color='grey', transform=ccrs.Geodetic())


print('一共%d个'%c)

# 显示
plt.show()

provinces = {0:'黑龙江', 1: ''}

