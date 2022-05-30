from tkinter import Listbox
from WebSpiders.request_spider import *
from ttkbootstrap import *
from time import sleep
from threading import Thread


class SpiderChoose(Window):
    def __init__(self, **kwargs):
        info_dict = kwargs.get('information', {})
        kwargs.pop('information')
        super().__init__(**kwargs)
        self.geometry('800x400+400+200')

        # 选中的案例名称（字典中）
        self.selected_name = None

        def choose_name():
            self.selected_name = spider_lb.get(spider_lb.curselection()[0])

        spider_frame = Frame(self)
        button_frame = Frame(self)
        spider_frame.pack(side=LEFT, fill=Y)
        button_frame.pack(side=LEFT, fill=BOTH, expand=True)

        max_length = 30
        for name in info_dict:
            max_length = max(len(name), max_length)
        if max_length > 30:
            max_length += 10

        spider_lb = Listbox(spider_frame, width=max_length)
        scb = Scrollbar(spider_frame)
        spider_lb.config(yscrollcommand=scb.set)
        scb.config(command=spider_lb.yview)

        spider_lb.pack(side=LEFT, expand=True, fill=BOTH)
        scb.pack(side=LEFT, fill=Y)

        name_label = Label(button_frame, anchor='n', font='微软雅黑 18 bold')
        name_label.grid(row=0, column=0, columnspan=2, sticky='nwe')
        Label(button_frame, text='地址: ').grid(row=1, column=0, sticky='w')
        web_site_label = Label(button_frame)
        web_site_label.grid(row=1, column=1, sticky='we')
        Label(button_frame, text='描述: ', anchor='n').grid(row=2, column=0, sticky='nw')
        description = Label(button_frame)
        description.grid(row=2, column=1, sticky='we')
        ensure_bt = Button(button_frame, text='下载', command=choose_name)
        ensure_bt.grid(row=3, column=0, columnspan=2, sticky='swe')

        button_frame.columnconfigure(1, weight=1)
        button_frame.rowconfigure(3, weight=1)

        for spider in info_dict:
            spider_lb.insert(END, spider)

        def show_info(e):
            selected = spider_lb.curselection()
            if selected:
                name = spider_lb.get(selected[0])
                url_str = info_dict[name]['url']
                old_description_str = info_dict[name]['description']
                #  调整字符，产生换行
                max_str_num = 20
                description_str = ''
                if len(old_description_str) > max_str_num:
                    for i in range(int(len(old_description_str) / max_str_num)):
                        description_str += old_description_str[max_str_num * i: max_str_num * (i + 1)] + '\n'
                    else:
                        last_num = len(old_description_str) % max_str_num
                        print(last_num)
                        if last_num:
                            description_str += old_description_str[- last_num:]
                        else:
                            pass
                else:
                    description_str = old_description_str

                name_label.config(text=name)
                web_site_label.config(text=url_str)
                description.config(text=description_str)
            else:
                name_label.config(text='')
                web_site_label.config(text='')
                description.config(text='')

        spider_lb.bind('<<ListboxSelect>>', show_info)


class ChartConfig(Window):
    pass


class DataConfig(Window):
    def __init__(self, recognizable_name_dict, to_recognize_name_list):
        super().__init__()



def get_virus_name(name_dict):
    s = SpiderChoose(information=name_dict)
    s.title('选择数据')
    s.mainloop()
    return s.selected_name


if __name__ == '__main__':
    # r = Window()
    information_dict = {
        '全球新冠': {
            'url': 'qweqwe://qweqweq',
            'description': '委委屈诶去哦',
        },
        'qwqqqq': {
            'url': 'qweqwe://qweqweq',
            'description': '这一驱蚊器翁群翁萨达大大所大所',
        }
    }
    get_virus_name(information_dict)
