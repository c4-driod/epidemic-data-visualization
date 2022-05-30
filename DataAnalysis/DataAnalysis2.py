from DataTransfer.Functions import *


class DataManager:
    infos = []
    statics = {}

    #  默认名字-类型表
    name_type = {'location': 'Location', 'time': 'Collection date', 'status': 'Patient status'}

    def set_data(self, infos):
        self.infos = infos

    def read_excel(self, filename):
        infos = xlsx_file_to_infos(filename)
        self.infos = infos

    def get_vaccinated(self):
        time_series = {}
        for item in self.infos:

            time_series[item[self.name_type['time']]] = {}
