import pandas
import os
import time


def turn_to_datetime(df):
    if 'date' in df:
        if type(df.loc[0, 'date']) is str:
            df.loc[:, 'date'] = pandas.to_datetime(df.loc[:, 'date'])
    return df


class GeneralAnalyst:
    """
    提供各种作图所需数据
    """
    en_to_zh_translates = {
        'iso_code': 'ISO 国家代码',
        'continent': '洲',
        'location': '地区',
        'date': '时间',
        'total_cases': '总确诊数',
        'new_cases': '新增确诊数',
        'new_cases_smoothed': '新增确诊数（平滑处理）',
        'total_deaths': '总死亡数',
        'new_deaths': '新增死亡数',
        'new_deaths_smoothed': '新增死亡数（平滑处理）',
        'total_cases_per_million': '总确诊数/百万人',
        'new_cases_per_million': '新增确诊数/百万人',
        'new_cases_smoothed_per_million': '新增确诊数/百万人（平滑处理）',
        'total_deaths_per_million': '总死亡数/百万人',
        'new_deaths_per_million': '新增死亡数/百万人',
        'new_deaths_smoothed_per_million': '新增死亡数/百万人（平滑处理）',
        'reproduction_rate': '传染率',
        'icu_patients': 'ICU患者数',
        'icu_patients_per_million': 'ICU患者数/百万人',
        'hosp_patients': '住院患者数',
        'hosp_patients_per_million': '住院患者数/百万人',
        'weekly_icu_admissions': '周新增ICU患者数',
        'weekly_icu_admissions_per_million': '周新增ICU患者数/百万人',
        'weekly_hosp_admissions': '周新增住院患者数',
        'weekly_hosp_admissions_per_million': '周新增住院患者数/百万人',
        'total_tests': '总检测数',
        'new_tests': '新增检测数',
        'total_tests_per_thousand': '总检测数/千人',
        'new_tests_per_thousand': '新增检测数/千人',
        'new_tests_smoothed': '新增检测数（平滑处理）',
        'new_tests_smoothed_per_thousand': '新增检测数/千人（平滑处理）',
        'positive_rate': '阳性率',
        'tests_per_case': '检测数/患者数',
        'tests_units': '测试单位',
        'total_vaccinations': '已接种疫苗人数',
        'people_vaccinated': '至少接种一针疫苗人数',
        'people_fully_vaccinated': '完全接种疫苗人数',
        'total_boosters': '总疫苗消耗数',
        'new_vaccinations': '新增接种数',
        'new_vaccinations_smoothed': '新增接种数（平滑处理）',
        'total_vaccinations_per_hundred': '已接种疫苗人数/百人',
        'people_vaccinated_per_hundred': '至少接种一针疫苗人数/百人',
        'people_fully_vaccinated_per_hundred': '完全接种疫苗人数/百人',
        'total_boosters_per_hundred': '总疫苗消耗数/百人',
        'new_vaccinations_smoothed_per_million': '新增接种数/百万人（平滑处理）',
        'new_people_vaccinated_smoothed': '至少接种一针疫苗人数（平滑处理）',
        'new_people_vaccinated_smoothed_per_hundred': '至少接种一针疫苗人数/百人（平滑处理）',
        'stringency_index': '卫生严格指数',
        'population': '人口',
        'population_density': '人口密度',
        'median_age': '年龄中位数',
        'aged_65_older': '高于65岁人数',
        'aged_70_older': '高于70岁人数',
        'gdp_per_capita': '人均生产总值（GDP）',
        'extreme_poverty': '极端贫困率',
        'cardiovasc_death_rate': '心血管死亡率',
        'diabetes_prevalence': '糖尿病患病率',
        'female_smokers': '女性吸烟率',
        'male_smokers': '男性吸烟率',
        'handwashing_facilities': '洗手设施评分',
        'hospital_beds_per_thousand': '医院床位/千人',
        'life_expectancy': '预期寿命',
        'human_development_index': '人类发展指数',
        'excess_mortality_cumulative_absolute': '超额死亡率绝对值累加值',
        'excess_mortality_cumulative': '超额死亡率累加值',
        'excess_mortality': '超额死亡率',
        'excess_mortality_cumulative_per_million': '超额死亡率累加值/百万人',
    }

    def __init__(self):
        #  数据名字对照表，前面部分代表转化前df的对应名称，后面部分代表转化后df对应名称
        self.data_names = {
            'iso_code': 'iso_code',
            'continent': 'continent',
            'location': 'location',
            'date': 'date',
            'total_cases': 'total_cases',
            'new_cases': 'new_cases',
            'new_cases_smoothed': 'new_cases_smoothed',
            'total_deaths': 'total_deaths',
            'new_deaths': 'new_deaths',
            'new_deaths_smoothed': 'new_deaths_smoothed',
            'total_cases_per_million': 'total_cases_per_million',
            'new_cases_per_million': 'new_cases_per_million',
            'new_cases_smoothed_per_million': 'new_cases_smoothed_per_million',
            'total_deaths_per_million': 'total_deaths_per_million',
            'new_deaths_per_million': 'new_deaths_per_million',
            'new_deaths_smoothed_per_million': 'new_deaths_smoothed_per_million',
            'reproduction_rate': 'reproduction_rate',
            'icu_patients': 'icu_patients',
            'icu_patients_per_million': 'icu_patients_per_million',
            'hosp_patients': 'hosp_patients',
            'hosp_patients_per_million': 'hosp_patients_per_million',
            'weekly_icu_admissions': 'weekly_icu_admissions',
            'weekly_icu_admissions_per_million': 'weekly_icu_admissions_per_million',
            'weekly_hosp_admissions': 'weekly_hosp_admissions',
            'weekly_hosp_admissions_per_million': 'weekly_hosp_admissions_per_million',
            'total_tests': 'total_tests',
            'new_tests': 'new_tests',
            'total_tests_per_thousand': 'total_tests_per_thousand',
            'new_tests_per_thousand': 'new_tests_per_thousand',
            'new_tests_smoothed': 'new_tests_smoothed',
            'new_tests_smoothed_per_thousand': 'new_tests_smoothed_per_thousand',
            'positive_rate': 'positive_rate',
            'tests_per_case': 'tests_per_case',
            'tests_units': 'tests_units',
            'total_vaccinations': 'total_vaccinations',
            'people_vaccinated': 'people_vaccinated',
            'people_fully_vaccinated': 'people_fully_vaccinated',
            'total_boosters': 'total_boosters',
            'new_vaccinations': 'new_vaccinations',
            'new_vaccinations_smoothed': 'new_vaccinations_smoothed',
            'total_vaccinations_per_hundred': 'total_vaccinations_per_hundred',
            'people_vaccinated_per_hundred': 'people_vaccinated_per_hundred',
            'people_fully_vaccinated_per_hundred': 'people_fully_vaccinated_per_hundred',
            'total_boosters_per_hundred': 'total_boosters_per_hundred',
            'new_vaccinations_smoothed_per_million': 'new_vaccinations_smoothed_per_million',
            'new_people_vaccinated_smoothed': 'new_people_vaccinated_smoothed',
            'new_people_vaccinated_smoothed_per_hundred': 'new_people_vaccinated_smoothed_per_hundred',
            'stringency_index': 'stringency_index',
            'population': 'population',
            'population_density': 'population_density',
            'median_age': 'median_age',
            'aged_65_older': 'aged_65_older',
            'aged_70_older': 'aged_70_older',
            'gdp_per_capita': 'gdp_per_capita',
            'extreme_poverty': 'extreme_poverty',
            'cardiovasc_death_rate': 'cardiovasc_death_rate',
            'diabetes_prevalence': 'diabetes_prevalence',
            'female_smokers': 'female_smokers',
            'male_smokers': 'male_smokers',
            'handwashing_facilities': 'handwashing_facilities',
            'hospital_beds_per_thousand': 'hospital_beds_per_thousand',
            'life_expectancy': 'life_expectancy',
            'human_development_index': 'human_development_index',
            'excess_mortality_cumulative_absolute': 'excess_mortality_cumulative_absolute',
            'excess_mortality_cumulative': 'excess_mortality_cumulative',
            'excess_mortality': 'excess_mortality',
            'excess_mortality_cumulative_per_million': 'excess_mortality_cumulative_per_million',
        }
        self.key_names = ['iso_code', 'continent', 'location', 'date']
        self.file_open_channels = {
            'csv': pandas.read_csv,
            'xls': pandas.read_excel,
            'xlsx': pandas.read_excel,
            'txt': pandas.read_table,
            'json': pandas.read_json,
            'xml': pandas.read_xml,
            'html': pandas.read_html,
        }
        #  默认日期格式
        self.date_fmt = '%Y-%m-%d'
        #  原始数据集
        self.raw_data_sets = []
        #  主数据
        self.data = pandas.DataFrame()

    def load_data(self, df):
        self.raw_data_sets.append(df)
        #  导入已知信息
        self.load_recognizable_info(self.extract_recognizable_infos(df))
        #  去重
        self.data.drop_duplicates(inplace=True)

    def extract_recognizable_infos(self, df):
        recognizable_df = pandas.DataFrame()
        for item in df:
            if item in self.data_names:
                recognizable_df[self.data_names[item]] = df[item]
        recognizable_df = turn_to_datetime(recognizable_df)
        return recognizable_df

    def load_recognizable_info(self, recognizable_df):
        self.data = pandas.concat([self.data, recognizable_df])

    def get_whole_raw_data(self):
        data_sets_num = len(self.raw_data_sets)
        if not data_sets_num:
            return pandas.DataFrame()
        if data_sets_num == 1:
            return self.raw_data_sets[0]
        else:
            return pandas.concat(self.raw_data_sets)

    def get_time_span(self):
        copy = self.data.loc[:, 'date'].sort_values()
        return [copy.iloc[0].strftime(self.date_fmt), copy.iloc[-1].strftime(self.date_fmt)]

    def get_sort_types(self):
        if self.is_data_not_empty():
            names = list(self.data)
            new_names = []
            for i in names:
                if i not in self.key_names:
                    new_names.append(self.en_to_zh_translates[i])
            return new_names
        else:
            return []

    def get_locations(self):
        if self.is_data_not_empty():
            loc_list = list(self.data.loc[:, 'location'].drop_duplicates())
            return loc_list
        else:
            return []

    def is_data_not_empty(self):
        if self.data.any:
            return True
        else:
            return False

    def translate(self, word):
        if word in self.en_to_zh_translates:
            return self.en_to_zh_translates[word]
        elif word in list(self.en_to_zh_translates.values()):
            for item in self.en_to_zh_translates:
                if word == self.en_to_zh_translates[item]:
                    return item

    def sorted_locations(self, by_name, selected_list, unselected_list):
        if not by_name:
            return selected_list, unselected_list
        elif by_name in self.get_sort_types():
            by_name = self.translate(by_name)
        #  按日期上的最新值，从大到小排序
        sorted_list = []
        if self.is_data_not_empty():
            sorted_df = self.data.loc[:, ['location', by_name]].sort_values(by_name).loc[:, 'location']
            sorted_list = list(sorted_df.drop_duplicates())
        new_list_to_sort = []
        for ls in (selected_list, unselected_list):
            new_ls = []
            for item in sorted_list:
                if item in ls:
                    new_ls.append(item)
            new_list_to_sort.append(new_ls)
        return new_list_to_sort


if __name__ == '__main__':
    # t1 = time.time()
    g = GeneralAnalyst()
    g.load_data('../ChartGenerate/owid-covid-data.csv')
    # print(g.raw_data_sets)
    # print(time.time()-t1)
    print(g.get_time_span())
