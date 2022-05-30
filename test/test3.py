from cartopy import crs
from cartopy import feature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplotlib import pyplot as plt
import numpy as np

ax = plt.axes(projection=crs.PlateCarree(central_longitude=70))
ax.add_feature(feature.OCEAN.with_scale('50m'))
ax.add_feature(feature.LAND.with_scale('50m'), lw=2)
ax.set_extent([0,100,10,80], crs=crs.PlateCarree())

plt.tight_layout()
plt.show()


