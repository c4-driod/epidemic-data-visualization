import pandas
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker


def set_major_locator(axe, x_span):
    axe.xaxis.set_major_locator(ticker.MultipleLocator(base=x_span))


def draw_axe(axe, data, x_name, y_name, **kwargs):
    axe.cla()
    if not x_name or not y_name:
        return {'coord': {}, 'color': {}}
    color = {}
    coord = {}
    for name in kwargs['location']:
        data_ = data.loc[data['location'] == name]
        other_keys = list(kwargs.keys())
        try:
            other_keys.remove('location')
            if other_keys:
                for item in other_keys:
                    df = pandas.DataFrame()
                    for value in kwargs[item]:
                        df = pandas.concat([df, data_.loc[data_[item] == value]])
                    data_ = df
        except Exception as e:
            print('draw_axe()出错:')
            print(e)
        x = data_.loc[:, x_name]
        y = data_.loc[:, y_name]
        line = axe.plot(x, y, label=name, linewidth=1.0)
        coord[name] = pandas.DataFrame({
            'x': x,
            'y': y,
        })
        color[name] = line[0].get_color()
    axe.legend(loc='upper left')
    return {'coord': coord, 'color': color}


def color_str_to_int(string):
    def _one_str(s):
        ls = {'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}
        if s.isalpha():
            s = s.lower()
            return ls[s]
        else:
            return int(s)
    num = 0
    count = 0
    for i in string[1:][::-1]:
        num += _one_str(i)*(16**count)
        count += 1
    return num


def color_int_to_str(integer):
    max_int = 16777215
    if 0 <= integer <= max_int:
        string = str(hex(integer))[2:].rjust(6, '0')
        return '#' + string
    elif type(integer) is int:
        return color_int_to_str(integer % max_int)
    else:
        return integer


def deeper_color(color_string, degree=60):
    integer = color_str_to_int(color_string)
    new_color_string = color_int_to_str(integer + degree)
    return new_color_string


def draw_annotate(axe, event, mpl_canvas, last_annotates, using_data, x_list, time_span):
    x_start, x_end = pandas.Timestamp(time_span[0]), pandas.Timestamp(time_span[1])
    ann = last_annotates.get()
    if ann is not None:
        for i in ann:
            i.remove()
    xdata = pandas.Timestamp(event.xdata, unit='D')
    text_xdata = xdata
    ha = 'left'
    if xdata == x_start:
        ha = 'left'
    elif xdata == x_end:
        ha = 'right'
    annotates = []
    if x_list is not None and event.inaxes:
        #  数据中存在的x坐标
        true_xdata = x_list.iloc[(x_list - xdata).abs().argsort().iloc[0]]
        #  横坐标注释在坐标轴上，只有一个
        x_text = str(xdata.strftime('%Y-%m-%d'))
        annotates.append(
            axe.annotate(
                text=x_text,
                xy=(xdata, 0),
                xytext=(text_xdata, 0),
                va='top',
            )
        )
        for location in using_data['coord']:
            #  对应地点的坐标集
            data = using_data['coord'][location]
            #  搜索到的y坐标集
            searched = data.loc[data.loc[:, 'x'] == true_xdata]
            if not len(searched):
                #  没有对应y，忽略
                continue
            else:
                #  取第一个y
                ydata = searched.loc[:, 'y'].iloc[0]
            #  注释展示的文本
            y_text = str(ydata)
            if using_data['color']:
                annotate = axe.annotate(
                    text=y_text,
                    xy=(xdata, ydata),
                    xytext=(text_xdata, ydata),
                    ha=ha,
                    color=deeper_color(using_data['color'][location]),
                )
            else:
                annotate = axe.annotate(
                    text=y_text,
                    xy=(xdata, ydata),
                    xytext=(text_xdata, ydata),
                    ha=ha,
                )

            annotates.append(
                annotate
            )
        mpl_canvas.draw()
    last_annotates.set(annotates)


def find_y_lim_func(using_data_coord, time_span):
    whole_data = pandas.concat(list(using_data_coord.values()))
    whole_data = whole_data.loc[(time_span[0] < whole_data.loc[:, 'x'])&(whole_data.loc[:, 'x'] < time_span[1])]
    statics = whole_data.loc[:, 'y'].dropna().sort_values()
    miny, maxy = statics.iloc[0], statics.iloc[-1]
    # sep = (maxy - miny)
    # miny = miny - sep * 0.1
    return miny, maxy


def create_table(axe, df):
    axe.cla()
    axe.axis('off')
    axe.table(cellText=df.values, colLabels=df.columns, loc='center')


def draw_axe_other_kinds(axe, draw_func_str, data, x_name, y_name, **kwargs):
    axe.cla()
    if not x_name or not y_name:
        return {'coord': {}, 'color': {}}
    draw_funcs = {
        'bar': axe.bar,
        'scatter': axe.scatter,
    }

    color = {}
    coord = {}
    for name in kwargs['location']:
        data_ = data.loc[data['location'] == name]
        other_keys = list(kwargs.keys())
        try:
            other_keys.remove('location')
            if other_keys:
                for item in other_keys:
                    df = pandas.DataFrame()
                    for value in kwargs[item]:
                        df = pandas.concat([df, data_.loc[data_[item] == value]])
                    data_ = df
        except Exception as e:
            print('draw_axe()出错:')
            print(e)
        x = data_.loc[:, x_name]
        y = data_.loc[:, y_name]
        draw_funcs[draw_func_str](x, y, label=name)
        coord[name] = pandas.DataFrame({
            'x': x,
            'y': y,
        })
        print(color)
    axe.legend(loc='upper left')
    return {'coord': coord, 'color': color}


def seaborn_draw(axe, data, kind):
    axe.relplot(data=data, kind=kind)



if __name__ == '__main__':
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    # draw_axe_other_kinds(ax, 'scatter', pandas.read_csv('../测试数据/owid-covid-data.csv'), 'date', 'new_deaths',
                         # location=['India'])
    # set_major_locator(ax, 80)
    seaborn_draw(ax, pandas.read_csv('../test/owid-covid-data.csv'), 'scatter')
    ax.set_xlim('2021-01-01', '2021-06-03')
    plt.show()

