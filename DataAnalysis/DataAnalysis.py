import pandas
import time
from re import *
import numpy


def sort_date_str_list(date_str_list):
    int_list = []
    int_date_dict = {}
    for date in date_str_list:
        # 转换成数字进行排序
        date_stamp_str = str.join('', filter(str.isdigit, date))
        date_stamp = int(date_stamp_str)
        int_list.append(date_stamp)
        int_date_dict[date_stamp] = date
    int_list.sort()
    return [int_date_dict[i] for i in int_list]


def location_filter(string):
    if '/' in string:
        string2 = match('([^/]+) /', string).group(1)
    else:
        string2 = string
    return string2


def census_extract(name_range_dict, count_df):
    #  提取包含目标列表内容的行
    sd = count_df
    extract_ar = numpy.array([False] * len(sd))
    #  统计需要留下的行 , 不包含的name忽略掉
    for name in name_range_dict:
        if name not in sd.columns:
            pass
        else:
            add_ar = numpy.array([False] * len(sd))
            for rang in name_range_dict[name]:
                add_ar = add_ar+sd[name]==rang
            for i in range(len(sd)):
                extract_ar[i] = extract_ar[i] * add_ar[i]
    tdf = sd[extract_ar]
    return tdf


def census_pre(df, name1, name2, name3):
    #  统计不同数据的name1、name2共同在name3上的数量分布
    for name in [name1, name2, name3]:
        if name not in df.columns:
            #  参数错误，df表中不存在至少一个对应参数
            print('{0},{1},{2}中至少有一个参数不正确'.format(name1, name2, name3))
            return None

    #  software_count_name
    s_name = 'software_count'
    #  取出目标df
    selected_df = df[[name1, name2, name3]]
    selected_df.loc[:,s_name] = 0
    #  统计密度
    #  count函数会把非索引的所有数据直接转变成int密度统计数据，所以要提前安排一列'software_count'防止无位置给count函数
    #  count函数会生成一个列长度不同于原df的df
    selected_df_count = selected_df.groupby([name1, name2, name3]).count()
    #  还原index
    selected_df_count.reset_index(inplace=True)
    #  按时间等排序
    selected_df_count.sort_values(by=name3)
    #  计算累计函数
    selected_df_count['software_cumsum'] = selected_df_count.groupby([name1, name2])[s_name].cumsum()
    return selected_df_count


def census_get_names(df):
    names = {}
    for info in df.columns:
        names[info] = df[info].unique()
    return names


class DataManager:
    """只负责管理病例数据"""
    PatientData = pandas.DataFrame([{}])
    statics = {'census_all_count': pandas.DataFrame()}

    #  默认名字-类型表
    name_type = {'location': 'Location', 'time': 'Collection date', 'status': 'Patient status',
                 'vaccinated value': 'Vaccinated'}

    def set_patient_data(self, data):
        self.PatientData = data

    def alt_name(self, old_name, new_name):
        self.PatientData.rename(columns={old_name: new_name})

    def get_data(self):
        return self.PatientData

    def set_name_type(self, name_type):
        self.name_type = name_type

    def get_name_type(self, name):
        if name in self.name_type:
            name = self.name_type[name]
        return name

    #  基础计算函数
    def calculate_basic_statics_1(self):
        #  计算常用基础统计量
        describe = self.PatientData.describe()
        self.statics['count'] = describe.loc['count']  # Series类
        self.statics['mean'] = describe.loc['mean']
        self.statics['std'] = describe.loc['std']
        self.statics['min'] = describe.loc['min']
        self.statics['25%'] = describe.loc['25%']
        self.statics['50%'] = describe.loc['50%']
        self.statics['75%'] = describe.loc['75%']
        self.statics['max'] = describe.loc['max']

    def calculate_basic_statics_2(self):
        #  计算高级统计量
        pdata = self.PatientData
        sum = pdata.sum()
        mad = pdata.mad()  # 平均绝对离差
        var = pdata.var()  # 方差
        skew = pdata.skew()  # 偏度
        kurt = pdata.kurt()  # 峰度
        cumsum = pdata.cumsum()  # 样本值累计和
        cummin = pdata.cummin()  # 样本累计最小值
        cummax = pdata.cummax()  # 样本累计最大值
        cumprod = pdata.cumprod()  # 样本值累计积
        diff = pdata.diff()  # 一阶差分
        pct_change = pdata.pct_change()  # 百分数变化

        self.statics['max'] = sum
        self.statics['mad'] = mad
        self.statics['var'] = var
        self.statics['skew'] = skew
        self.statics['kurt'] = kurt
        self.statics['cumsum'] = cumsum
        self.statics['cummin'] = cummin
        self.statics['cummax'] = cummax
        self.statics['cumprod'] = cumprod
        self.statics['diff'] = diff
        self.statics['pct_change'] = pct_change

    def calculate_basic_statics_special(self, calculate_string):
        #  根据输入的字符自定义统计量
        pass

    def get_vaccinate(self):
        location_list = {}
        for i in range(len(self.PatientData.index)):
            now_line = self.PatientData.iloc[i]
            location = now_line[self.get_name_type('location')]
            location = location_filter(location)
            datetime = now_line[self.get_name_type('time')]
            vaccinate_status = now_line[self.get_name_type('status')]
            if not vaccinate_status == self.get_name_type('vaccinated value'):
                #  未注射疫苗，跳过，统计下一个
                times = 0
            else:
                times = 1
            if location not in location_list:
                location_list[location] = {datetime: times}
            else:
                if datetime not in location_list[location]:
                    location_list[location][datetime] = times
                else:
                    location_list[location][datetime] += times
        #  统计完毕
        df = pandas.DataFrame(location_list)
        return df

    def get_vaccinated(self):
        #  统计已注射疫苗的人数/国家
        df = self.get_vaccinate()
        df.sort_index(inplace=True)
        for col in df:
            new_col = df[col].cumsum(axis=0)
            df[col] = new_col
        return df

    def v_test(self):
        g = self.get_name_type
        copy = self.PatientData.copy()
        #  地址清洗
        loc_str = self.get_name_type('location')
        copy[loc_str] = copy[loc_str].apply(location_filter)
        # 统计
        loc = census_get_names(copy)[g('location')]
        print('loc:',loc)
        copy = copy[copy[g('location')] == loc[0]]
        sta = census_get_names(copy)[g('status')]
        print('sta:', sta)
        copy = copy[copy[g('status')] == sta[1]]
        copy.sort_values(by=g('time'))
        print('copy:')
        print(copy[[g('location'), g('time'), g('status')]])
        vd = census_pre(copy, g('location'), g('time'), g('status'))
        return vd
