import pandas

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

df = pandas.DataFrame()
df.loc[:,'变量名'] = list(en_to_zh_translates.keys())
df.loc[:,'意义'] = list(en_to_zh_translates.values())

print(df)
df.to_excel('qwe.xlsx')