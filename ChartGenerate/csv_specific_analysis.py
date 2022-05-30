import pandas
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker


def draw_ax_by_countries(ax, data, type_name, countries=None, x_span=100):
    if not countries:
        countries = data.loc[:, 'location'].drop_duplicates().tolist()
    elif type(countries) is str:
        countries = [countries]
    for country in countries:
        data_ = data[data['location'] == country]
        x = data_.loc[:, 'date']
        y = data_.loc[:, type_name]
        ax.plot(x, y, label=country)
    # ax.legend()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=x_span))


if __name__ == '__main__':
    #  测试
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    draw_ax_by_countries(ax, pandas.read_csv('../test/owid-covid-data.csv'), type_name='new_deaths_smoothed',
                         countries=('India',))
    # ax.set_xlim('2021-09-01', '2022-01-01')

    plt.show()
