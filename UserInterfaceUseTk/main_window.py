from tkinter import Listbox
from ttkbootstrap import *
from UserInterfaceUseTk.mpls import *
from UserInterfaceUseTk.date_selector import TimeScale
from pandas import concat
from ChartGenerate.chart_generate import *
from datetime import datetime

date_fmt = '%Y-%m-%d'


def fake_func(a, b, c):
    print('fake_func, args:', a, b, c)
    return b, c


def fake_find_y_lim_func(a, b):
    print('fake_find_y_lim_func args:', a, b)
    return 0, 10


class ObjBox:
    def __init__(self, obj=None):
        self.obj = obj

    def set(self, obj):
        self.obj = obj

    def get(self):
        return self.obj


class MainWindow(Window):
    font_middle = '微软雅黑 10'

    def __init__(self):
        super().__init__()
        #  字体和界面配置
        self.default_config()
        #  内部变量
        #  选项参数
        self.options_args = {
            'locations': [],
            'sort_type': [],
            'unit': [],
            'data_type': [],
            'time_span': [],
        }

        self.selected_locations = []
        self.unselected_locations = []

        #  必要组件
        self.chart_notebook = Notebook()
        self.list_box = Listbox()
        self.combobox_sort_type = Combobox()
        self.combobox_unit = Combobox()
        self.combobox_data_type = Combobox()
        self.timescale = TimeScale()

        #  多图
        self.current_chart = None
        self.charts = {}

        #  外部函数
        self.sort_func = fake_func
        self.find_y_lim_func = fake_find_y_lim_func

        #  当前作图所用数据
        self.using_data = {}
        self.x_list = None  # DataFrame
        self.annotates = ObjBox()

    def default_config(self):
        self.title('Epidemiological Data Visualization')
        self.geometry('1500x800+100+50')
        self.bind('<Escape>', lambda e: self.full_screen(e, False))
        self.bind('<Button-2>', lambda e: self.full_screen(e, True))

    def full_screen(self, e, state):
        self.attributes('-fullscreen', state)

    def add_one_chart(self, chart_name, update_func, show_func):
        figure, axe = get_figure_and_ax()
        mpl_canvas = get_mpl_canvas(self.chart_notebook, figure)
        self.charts[chart_name] = {
            'axe': axe,
            'figure': figure,
            'mpl_canvas': mpl_canvas,
            'update_func': update_func,
            'show_func': show_func,
        }
        mpl_canvas.mpl_connect('motion_notify_event',
                               lambda e: show_func(
                                   axe,
                                   e,
                                   mpl_canvas,
                                   self.annotates,
                                   self.using_data,
                                   self.x_list,
                                   self.get_canvas_args('time_span')
                               ))
        self.current_chart = chart_name
        chart_widget = get_tk_mpl_widget(mpl_canvas)
        chart_widget.pack(fill=BOTH, expand=True)
        self.chart_notebook.add(chart_widget, text=chart_name)
        self.chart_notebook.select(chart_widget)

    def get_charts_name(self):
        return list(self.charts.keys())

    def get_canvas_args(self, arg_name):
        if arg_name == 'locations':
            locations = []
            for i in self.list_box.curselection():
                locations.append(self.list_box.get(i))
            return locations
        elif arg_name == 'sort_type':
            return self.combobox_sort_type.get()
        elif arg_name == 'unit':
            return self.combobox_unit.get()
        elif arg_name == 'data_type':
            return self.combobox_data_type.get()
        elif arg_name == 'time_span':
            return [self.timescale.datetime_start, self.timescale.datetime_end]

    def update_current_picture_time_span(self):
        #  x轴范围调节
        self.charts[self.current_chart]['axe'].set_xlim(*self.get_canvas_args('time_span'))
        #  检测y轴范围
        miny, maxy = self.find_y_lim_func(self.using_data['coord'], self.get_canvas_args('time_span'))
        self.charts[self.current_chart]['axe'].set_ylim(miny, maxy)
        #  更新图
        self.charts[self.current_chart]['mpl_canvas'].draw()

    def update_current_picture_all(self):
        def collect_all_x_data(df_dict):
            #  集中所有x轴数据
            df = None
            for i in df_dict:
                if df is not None:
                    df = df_dict[i].loc[:, 'x']
                else:
                    df = concat([df, df_dict[i].loc[:, 'x']])
            if df is not None:
                return df.drop_duplicates()
            else:
                return None

        self.using_data = self.charts[self.current_chart]['update_func']()
        self.x_list = collect_all_x_data(self.using_data['coord'])
        self.charts[self.current_chart]['axe'].set_xlim(*self.get_canvas_args('time_span'))
        self.charts[self.current_chart]['mpl_canvas'].draw()

    def update_option_args(self):
        self.combobox_sort_type['value'] = self.options_args['sort_type']
        self.combobox_unit['value'] = self.options_args['unit']
        self.combobox_data_type['value'] = self.options_args['data_type']

    def update_basic_widgets(self):
        self.list_box.delete(0, END)
        for location in self.options_args['locations']:
            self.list_box.insert(END, location)
        self.combobox_sort_type['value'] = self.options_args['sort_type']
        self.combobox_unit['value'] = self.options_args['unit']
        self.combobox_data_type['value'] = self.options_args['data_type']
        if self.options_args['time_span']:
            from_ = self.options_args['time_span'][0]
            to = self.options_args['time_span'][1]
            self.timescale.set_dates_range(from_, to)

    def list_box_bind(self, e):
        self.change_location_list_box(e)
        self.update_current_picture_all()

    def change_location_list_box(self, e):
        #  重新排序
        curselection = self.list_box.curselection()
        self.selected_locations = []
        self.unselected_locations = []
        for i in range(self.list_box.size()):
            if i in curselection:
                self.selected_locations.append(self.list_box.get(i))
            else:
                self.unselected_locations.append(self.list_box.get(i))
        self.list_box.delete(0, END)
        self.selected_locations, self.unselected_locations = \
            self.sort_func(self.get_canvas_args('sort_type'), self.selected_locations, self.unselected_locations)
        for item in self.selected_locations:
            self.list_box.insert(END, item)
            self.list_box.select_set(END)
        for item in self.unselected_locations:
            self.list_box.insert(END, item)

    def change_combobox(self, e):
        self.list_box.delete(0, END)
        if not (self.selected_locations and self.unselected_locations):
            self.unselected_locations = self.options_args['locations']
        self.selected_locations, self.unselected_locations = \
            self.sort_func(self.get_canvas_args('sort_type'), self.selected_locations, self.unselected_locations)
        for item in self.selected_locations:
            self.list_box.insert(END, item)
            self.list_box.select_set(END)
        for item in self.unselected_locations:
            self.list_box.insert(END, item)
        self.update_current_picture_all()

    def change_list_box_width(self, e):
        char_width = 100
        box_width = self.list_box.cget('width')
        new_width = box_width + int(e.x / char_width)
        print(int(e.x / char_width))
        if new_width > 1:
            self.list_box.config(width=new_width)

    def set_frames(self):
        #  选项区域
        select_frame_areas = Frame(self)
        select_frame_data_types = Frame(self)
        select_frame_time_span = Frame(self)
        #  图表框
        chart_frame = Frame(self)

        def layout1():
            #  grid:row3, column2
            #  col0
            select_frame_areas.grid(row=0, column=0, rowspan=3, sticky='swen')
            #  col1
            select_frame_data_types.grid(row=0, column=1, sticky='swen')
            chart_frame.grid(row=1, column=1, sticky='swen')
            select_frame_time_span.grid(row=2, column=1, sticky='swen')

            self.rowconfigure(1, weight=1)
            self.columnconfigure(1, weight=1)

        #  布局
        layout1()

        #  添加地区选择
        list_box_frame = Frame(select_frame_areas)
        list_box_frame.grid(row=1, column=0, columnspan=2, sticky='swen')
        self.list_box = Listbox(list_box_frame, selectmode=MULTIPLE, font=self.font_middle)
        self.list_box.bind('<<ListboxSelect>>', self.list_box_bind)
        #  添加滑块
        self.list_box.pack(side=LEFT, expand=True, fill=BOTH)
        list_box_scb = Scrollbar(list_box_frame, command=self.list_box.yview)
        list_box_scb.pack(side=LEFT, fill=Y, expand=True)
        self.list_box.config(yscrollcommand=list_box_scb.set)
        select_frame_areas.rowconfigure(1, weight=1)
        select_frame_areas.columnconfigure(1, weight=1)

        #  设置排序方式选项
        Label(select_frame_areas, text='排序方式', font=self.font_middle).grid(row=0, column=0, sticky='we')

        self.combobox_sort_type = Combobox(
            select_frame_areas,
            width=5,
            font=self.font_middle,
            state=READONLY
        )
        self.combobox_sort_type.bind('<<ComboboxSelected>>', self.change_combobox)
        self.combobox_sort_type.grid(row=0, column=1, sticky='we')

        #  设置数据类型选项
        Label(select_frame_data_types, text='数据', font=self.font_middle).grid(row=0, column=0)
        Label(select_frame_data_types, text='图表类型', font=self.font_middle).grid(row=0, column=1)

        self.combobox_unit = Combobox(
            select_frame_data_types,
            width=5,
            font=self.font_middle,
            state=READONLY,
        )
        self.combobox_unit.bind('<<ComboboxSelected>>', self.change_combobox)

        self.combobox_data_type = Combobox(
            select_frame_data_types,
            width=5,
            font=self.font_middle,
            state=READONLY,
        )
        self.combobox_data_type.bind('<<ComboboxSelected>>', self.change_combobox)
        self.combobox_unit.grid(row=1, column=0, sticky='swen')
        self.combobox_data_type.grid(row=1, column=1, sticky='swen')
        select_frame_data_types.columnconfigure(0, weight=1)
        select_frame_data_types.columnconfigure(1, weight=1)

        #  设置时间区间选项
        self.timescale = TimeScale(master=select_frame_time_span)
        self.timescale.pack(fill=BOTH, expand=True)

        def change_time_span():
            self.update_current_picture_time_span()

        self.timescale.bind_date_change(change_time_span)

        #  图表NoteBook
        self.chart_notebook = Notebook(chart_frame)
        self.chart_notebook.pack(fill=BOTH, expand=True)

        def update_current_chart(e):
            self.current_chart = self.chart_notebook.tab(self.chart_notebook.select(), 'text')

        self.chart_notebook.bind('<<NotebookTabChanged>>', update_current_chart)

    def set_menu(self, menu_config):
        def set_menu(father, this):
            for item in this:
                if type(this[item]) is not dict:
                    father.add_command(label=item, command=this[item])
                else:
                    menu = Menu(father)
                    father.add_cascade(label=item, menu=menu)
                    set_menu(menu, this[item])

        menubar = Menu(self)

        set_menu(menubar, menu_config)

        self.config(menu=menubar)


if __name__ == '__main__':
    mw = MainWindow()

    mw.set_frames()
    mw.mainloop()
