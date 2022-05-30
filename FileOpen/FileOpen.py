from tkinter.filedialog import askopenfilename, asksaveasfilename
import ctypes
import pandas
import os


class FileManager:
    REST = 'rest'
    OPENING = 'opening'
    UNSUPPORTED_TYPE = 'unsupported type'
    FILE_NOT_EXIST = 'file not exist'

    def __init__(self):
        self.file_open_channels = {
            'csv': pandas.read_csv,
            'xls': pandas.read_excel,
            'xlsx': pandas.read_excel,
            'txt': pandas.read_table,
            'json': pandas.read_json,
            'xml': pandas.read_xml,
            'html': pandas.read_html,
        }
        #  让文件选择器打开的时候不模糊
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
        #  状态值
        self.status = self.REST

    def open(self, filename):
        self.status = self.OPENING
        suffix = os.path.splitext(filename)[1].lstrip('.')
        if suffix in self.file_open_channels:
            if os.path.exists(filename):
                df = self.file_open_channels[suffix](filename)
                self.status = self.REST
                return df
            else:
                self.status = self.FILE_NOT_EXIST
        else:
            self.status = self.UNSUPPORTED_TYPE
        return self.status

    def ask_and_openfile(self):
        return self.open(askopenfilename())

    def ask_save_filename(self):
        filename = asksaveasfilename(
            filetypes=[
                ('图片', '.png'),
            ],
            initialfile='pic.png'
        )
        return filename
