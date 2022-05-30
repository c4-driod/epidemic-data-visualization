from matplotlib import pyplot as plt
from cartopy import crs
from cartopy import feature
from numpy import fromstring


def draw_map_world(axe):
    axe.add_feature(feature.LAND.with_scale('110m'))
    axe.add_feature(feature.OCEAN.with_scale('110m'))
    axe.add_feature(feature.COASTLINE.with_scale('110m'))
    axe.add_feature(feature.BORDERS.with_scale('110m'))


def draw_map_china(axe):
    axe.add_feature(feature.LAND.with_scale('110m'), color='white')
    axe.add_feature(feature.OCEAN.with_scale('110m'))
    with open('CN-border-La.dat') as f:
        context = f.read()
        blocks = [cnt for cnt in context.split('>') if len(cnt) > 0]
        borders = [fromstring(block, dtype=float, sep=' ') for block in blocks]
    for line in borders:
        ax.plot(line[0::2], line[1::2], '-', color='gray', transform=crs.Geodetic())

    axe.set_extent([70, 140, 15, 50])


if __name__ == '__main__':
    fig = plt.figure(tight_layout=True)
    ax = plt.axes(projection=crs.PlateCarree())
    draw_map_world(ax)
    plt.show()

