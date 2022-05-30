from ttkbootstrap import *
from dateutil.parser import parse
from pandas import Timedelta
from time import sleep
from threading import Thread


def is_in_bbox(rect, e):
    if rect is None:
        return False
    if rect[0] > rect[2]:
        rect[0], rect[2] = rect[2], rect[0]
    if rect[1] > rect[3]:
        rect[1], rect[3] = rect[3], rect[1]
    return (rect[0] <= e.x <= rect[2]) and (rect[1] <= e.y <= rect[3])


def get_date_by_percent(from_, to, percent):
    days = (to - from_).days
    specific = from_ + Timedelta(days=days*percent)
    return specific, specific.strftime(default_date_fmt)


default_date_fmt = '%Y-%m-%d'


class TimeScale(Canvas):
    _r = 7
    player_stop_fig = [-_r, -_r * 1.73, _r * 1.73, 0, -_r, _r * 1.73]
    color_player = '#888888'
    color_scale_empty = '#bbbbbb'
    color_scale_fill = '#0048f2'
    default_time_str = '2000-10-23'
    default_time = parse(default_time_str)

    def __init__(self, **kw):
        self.from_ = parse(kw.pop('from_', self.default_time_str))
        self.to = parse(kw.pop('to', self.default_time_str))
        self.font = kw.pop('font', '微软雅黑 10')
        super().__init__(**kw)
        self.player_length_half = 25
        self.text_length_half = 70
        self.scale_empty_height_half = 3
        self.scale_fill_height_half = 5
        self.pointer_r = 12
        self.text_pointer_sep = 25
        self.default_height = 50
        self.config(height=80)

        self.is_player_on = False
        self.start_percent = 0.0
        self.end_percent = 1.0
        self.date_from = self.from_.strftime(default_date_fmt) if self.from_ != self.default_time else ''
        self.date_to = self.to.strftime(default_date_fmt) if self.to != self.default_time else ''
        self.date_start = ''
        self.date_end = ''
        self.datetime_start = self.from_
        self.datetime_end = self.to
        self.thread_serial_num = 0
        self.player_min_time_sep = 0.3
        self.date_change_func = print
        self.date_change_args = ['日期改变']
        self.player_change_func = print
        self.player_change_args = ['播放状态改变']

        self.width = 0
        self.height = 0
        self.start_x = 0
        self.end_x = 0
        self.length = 0
        self.pointer_now = 0

        self.bind('<Motion>', self.motion)
        self.bind('<Button-1>', self.b1)
        self.bind('<B1-Motion>', self.b1_motion)
        self.bind('<ButtonRelease-1>', self.b1_release)
        self.bind('<Configure>', self.configure_)

        #  图像对象编号
        self.player_on = []
        self.player_stop = 0
        self.text_from = 0
        self.text_to = 0
        self.scale_empty = 0
        self.scale_fill = 0
        self.pointer_1 = 0
        self.pointer_2 = 0
        self.pointer_text1 = 0
        self.pointer_text2 = 0

    def set_dates_range(self, from_str, to_str):
        self.from_ = parse(from_str)
        self.to = parse(to_str)
        self.date_from = self.from_.strftime(default_date_fmt)
        self.date_to = self.to.strftime(default_date_fmt)
        self.datetime_start = self.from_
        self.datetime_end = self.to
        self.update_all()

    def update_player_stop(self):
        self.delete(self.player_stop)
        height = self.canvasy(self.winfo_height())
        player_stop = []
        for i in range(3):
            player_stop.append(self.player_stop_fig[2 * i] + self.player_length_half)
            player_stop.append(self.player_stop_fig[2 * i + 1] + height / 2)
        player = self.create_polygon(*player_stop, fill=self.color_player)
        self.player_stop = player

    def update_player_on(self):
        self.delete(self.player_on)
        height = self.canvasy(self.winfo_height())
        players = []
        for i in [-1, 1]:
            coord1 = (self.player_length_half + self._r * i, height / 2 - self._r * 1.73)
            coord2 = (self.player_length_half + self._r * i / 3, height / 2 + self._r * 1.73)
            players.append(self.create_rectangle(*coord1, *coord2, fill=self.color_player))
        self.player_on = players

    def update_texts(self):
        self.delete(self.text_from, self.text_to)
        width, height = self.canvasx(self.winfo_width()), self.canvasy(self.winfo_height())
        self.text_from = self.create_text(self.text_length_half + self.player_length_half * 2, height / 2,
                                          text=self.date_from, font=self.font)
        self.text_to = self.create_text(width - self.text_length_half, height / 2,
                                        text=self.date_to, font=self.font)

    def update_scale_empty(self):
        self.delete(self.scale_empty)
        self.scale_empty = self.create_rectangle(
            self.start_x,
            self.height / 2 - self.scale_empty_height_half,
            self.end_x,
            self.height / 2 + self.scale_empty_height_half,
            fill=self.color_scale_empty,
            width=0
        )

    def update_scale_fill(self):
        self.delete(self.scale_fill)
        self.scale_fill = self.create_rectangle(
            self.start_x + self.length * self.start_percent,
            self.height / 2 - self.scale_fill_height_half,
            self.start_x + self.length * self.end_percent,
            self.height / 2 + self.scale_fill_height_half,
            fill=self.color_scale_fill,
            width=0
        )

    def update_pointers(self):
        self.delete(self.pointer_1, self.pointer_2)
        self.pointer_1 = self.create_oval(
            self.start_x + self.length * self.start_percent - self.pointer_r,
            self.height / 2 - self.pointer_r,
            self.start_x + self.length * self.start_percent + self.pointer_r,
            self.height / 2 + self.pointer_r,
            outline=self.color_scale_fill,
            fill='white',
            width=3
        )
        self.pointer_2 = self.create_oval(
            self.start_x + self.length * self.end_percent - self.pointer_r,
            self.height / 2 - self.pointer_r,
            self.start_x + self.length * self.end_percent + self.pointer_r,
            self.height / 2 + self.pointer_r,
            outline=self.color_scale_fill,
            fill='white',
            width=3
        )

    def update_pointer_texts(self):
        self.delete(self.pointer_text1, self.pointer_text2)
        self.pointer_text1 = self.create_text(
            self.start_x + self.length * self.start_percent,
            self.height/2 - self.text_pointer_sep,
            text=self.date_start,
            font=self.font
        )
        self.pointer_text2 = self.create_text(
            self.start_x + self.length * self.end_percent,
            self.height/2 - self.text_pointer_sep,
            text=self.date_end,
            font=self.font
        )

    def update_all(self):
        self.update_player_on()
        for item in self.player_on:
            self.itemconfig(item, state=HIDDEN)
        self.update_player_stop()
        self.update_texts()
        self.update_basic_infos()
        self.update_scale_empty()
        self.update_scale_fill()
        self.update_pointers()
        self.update_pointer_texts()

    def change_player(self, e):
        #  分析出判定区域
        if self.is_player_on:
            player_rect = [*self.bbox(self.player_on[0])[:2], *self.bbox(self.player_on[1])[2:]]
        else:
            player_rect = self.bbox(self.player_stop)

        if is_in_bbox(player_rect, e):
            for item in self.player_on:
                self.itemconfig(item, state=HIDDEN if self.is_player_on else NORMAL)
            self.itemconfig(self.player_stop, state=NORMAL if self.is_player_on else HIDDEN)
            self.is_player_on = not self.is_player_on
            if self.is_player_on:
                self.play_func()
            self.player_change_func(*self.player_change_args)

    def _start_slide_points(self, e):
        if is_in_bbox(self.bbox(self.pointer_1), e):
            self.pointer_now = self.pointer_1
        if is_in_bbox(self.bbox(self.pointer_2), e):
            self.pointer_now = self.pointer_2

    def _end_slide_pointers(self):
        #  松开即结束
        self.pointer_now = 0
        #  修正start_percent, end_percent 大小关系
        if self.end_percent < self.start_percent:
            self.start_percent, self.end_percent = self.end_percent, self.start_percent
        self.update_slider()

    def update_slider(self):
        self.coords(
            self.pointer_1,
            self.start_x + self.length * self.start_percent - self.pointer_r,
            self.height / 2 - self.pointer_r,
            self.start_x + self.length * self.start_percent + self.pointer_r,
            self.height / 2 + self.pointer_r,
        )
        self.coords(
            self.pointer_2,
            self.start_x + self.length * self.end_percent - self.pointer_r,
            self.height / 2 - self.pointer_r,
            self.start_x + self.length * self.end_percent + self.pointer_r,
            self.height / 2 + self.pointer_r,
        )
        self.coords(
            self.scale_fill,
            self.start_x + self.length * self.start_percent,
            self.height / 2 - self.scale_fill_height_half,
            self.start_x + self.length * self.end_percent,
            self.height / 2 + self.scale_fill_height_half,
        )

    def slide_pointers(self, e):
        if not self.pointer_now:
            return
        percent = (e.x - self.start_x) / self.length
        percent = min(percent, 1.0)
        percent = max(percent, 0.0)
        if self.pointer_now == self.pointer_1:
            self.start_percent = percent
        elif self.pointer_now == self.pointer_2:
            self.end_percent = percent
        self.update_dates()
        self.update_slider()
        self.date_change_func(*self.date_change_args)

    def date_show_blue(self, e):
        if is_in_bbox(self.bbox(self.text_from), e):
            self.itemconfig(self.text_from, fill=self.color_scale_fill)
        elif is_in_bbox(self.bbox(self.text_to), e):
            self.itemconfig(self.text_to, fill=self.color_scale_fill)
        else:
            self.itemconfig(self.text_from, fill='black')
            self.itemconfig(self.text_to, fill='black')

    def update_dates(self):
        if self.from_ == self.default_time or self.to == self.default_time:
            return
        self.datetime_start, self.date_start = get_date_by_percent(self.from_, self.to, self.start_percent)
        self.datetime_end, self.date_end = get_date_by_percent(self.from_, self.to, self.end_percent)

    def pointer_show_date(self, e):
        if not (is_in_bbox(self.bbox(self.pointer_1), e) or is_in_bbox(self.bbox(self.pointer_2), e)):
            self.itemconfig(self.pointer_text1, state=HIDDEN)
            self.itemconfig(self.pointer_text2, state=HIDDEN)
            return
        self.coords(
            self.pointer_text1,
            self.start_x + self.length * self.start_percent,
            self.height/2 + self.text_pointer_sep,
        )
        self.coords(
            self.pointer_text2,
            self.start_x + self.length * self.end_percent,
            self.height/2 - self.text_pointer_sep,
        )
        self.update_dates()
        self.itemconfig(self.pointer_text1, text=self.date_start, state=NORMAL)
        self.itemconfig(self.pointer_text2, text=self.date_end, state=NORMAL)

    def slide_pointer_show_date(self, e):
        if not self.pointer_now:
            self.itemconfig(self.pointer_text1, state=HIDDEN)
            self.itemconfig(self.pointer_text2, state=HIDDEN)
            return
        self.coords(
            self.pointer_text1,
            self.start_x + self.length * self.start_percent,
            self.height/2 + self.text_pointer_sep,
        )
        self.coords(
            self.pointer_text2,
            self.start_x + self.length * self.end_percent,
            self.height/2 - self.text_pointer_sep,
        )
        self.itemconfig(self.pointer_text1, text=self.date_start, state=NORMAL)
        self.itemconfig(self.pointer_text2, text=self.date_end, state=NORMAL)

    def click_text_to_date(self, e):
        if is_in_bbox(self.bbox(self.text_from), e):
            self.start_percent = 0.0
        elif is_in_bbox(self.bbox(self.text_to), e):
            self.end_percent = 1.0
        self.update_slider()
        self.update_dates()
        self.date_change_func(*self.date_change_args)

    def play_func(self):
        num = self.thread_serial_num + 1
        self.thread_serial_num = num

        def change_():
            while self.is_player_on and self.thread_serial_num == num:
                self.itemconfig(self.pointer_text1, text=self.date_start, state=NORMAL)
                self.itemconfig(self.pointer_text2, text=self.date_end, state=NORMAL)
                try:
                    next_day_datetime = self.datetime_end + Timedelta(days=1)
                    if next_day_datetime != self.to:
                        self.datetime_end = next_day_datetime
                        self.end_percent = (self.datetime_end - self.from_).days / (self.to - self.from_).days
                        self.date_end = self.datetime_end.strftime(default_date_fmt)
                        self.update_slider()
                        self.date_change_func(*self.date_change_args)
                    sleep(self.player_min_time_sep)
                except Exception as e:
                    print(e)
                    pass

            self.itemconfig(self.pointer_text1, state=HIDDEN)
            self.itemconfig(self.pointer_text2, state=HIDDEN)

        Thread(target=change_, daemon=True).start()

    def motion(self, e):
        self.date_show_blue(e)
        self.pointer_show_date(e)

    def b1_motion(self, e):
        self._start_slide_points(e)
        self.slide_pointers(e)
        self.slide_pointer_show_date(e)

    def b1(self, e):
        self.change_player(e)
        self.click_text_to_date(e)

    def configure_(self, e):
        self.update_all()

    def b1_release(self, e):
        self._end_slide_pointers()

    def update_basic_infos(self):
        rect1 = self.bbox(self.text_from)
        rect2 = self.bbox(self.text_to)
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.start_x = rect1[2] + self.text_length_half / 2
        self.end_x = rect2[0] - self.text_length_half / 2
        self.length = self.end_x - self.start_x

    def bind_date_change(self, func, *args):
        self.date_change_func = func
        self.date_change_args = args

    def bind_player_change(self, func, *args):
        self.player_change_func = func
        self.player_change_args = args

    def get_selected_date(self):
        return self.date_start, self.date_end
