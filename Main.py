from UserInterfaceUseTk.main_window import MainWindow
from DataAnalysis.general_analysis import GeneralAnalyst
from ChartGenerate.chart_generate import *
from WebSpiders.request_spider import *
from FileOpen.FileOpen import FileManager
from UserInterfaceUseTk.secondary_window import get_virus_name


def load_args():
    mw.options_args['locations'] = analyst.get_locations()
    mw.options_args['sort_type'] = analyst.get_sort_types()
    mw.options_args['unit'] = analyst.get_sort_types()
    mw.options_args['data_type'] = ['7天滚动平均值', '每天新增', '周累计值', '周变化率', '两周累计值', '两周变化率', '总累计值']
    mw.update_basic_widgets()


def open_file(filename=''):
    if filename:
        df = file_manager.open(filename)
    else:
        df = file_manager.ask_and_openfile()
    analyst.load_data(df)
    load_args()
    add_charts()


def add_charts():
    add_one_chart()


def add_one_chart():
    mw.add_one_chart(
        chart_name1,
        lambda: draw_axe(
            mw.charts[mw.current_chart]['axe'],
            analyst.data,
            'date',
            analyst.translate(mw.get_canvas_args('unit')),
            location=mw.get_canvas_args('locations')
        ),
        draw_annotate,
    )
    mw.options_args['time_span'] = analyst.get_time_span()
    mw.update_basic_widgets()


def download_file():
    name = get_virus_name(site_info_dict)
    if name is not None:
        site_info_dict[name]['function']()


def save_to_filename():
    figure = mw.charts[mw.current_chart]['figure']
    filename = file_manager.ask_save_filename()
    figure.savefig(filename)


chart_name1 = '数据图'
chart_name2 = '分布图'
chart_name3 = '表格'

site_info_dict = {
    '新型冠状病毒（COVID-19）': {
        'url': 'https://ourworldindata.org/covid-cases',
        'description': '新型冠状病毒的全球数据集（实时更新）',
        'function': download_cov,
    },
}


mw = MainWindow()
analyst = GeneralAnalyst()
file_manager = FileManager()

menu_config = {
    '开始': {
        '下载案例数据': download_file,
        '打开本地文件': open_file,
    },
    '保存': save_to_filename,
}

mw.sort_func = analyst.sorted_locations
mw.find_y_lim_func = find_y_lim_func

mw.set_frames()
mw.set_menu(menu_config)

# fn = './测试数据/owid-covid-data.csv'
# open_file(fn)

mw.mainloop()
