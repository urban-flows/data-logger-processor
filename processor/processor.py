import glob
from datetime import date
from pathlib import Path

import pandas as pd

root_path = r'C:\Users\cs1xcw\PycharmProjects\data-logger-processor\dummy_data'

today = "2021-08-17"
class DataLoggerProcessor:
    def __init__(self):
        #self.today_directory = Path(root_path) / str(date.today()).replace("-", r"/")
        self.today_directory = Path(root_path) / str(today).replace("-", r"/")
    def timestamp_from_file(self):
        pass

    def list_files_from_today(self):
        paths = glob.glob(str(self.today_directory / "*"))
        return [paths[0]]

    def move_files(self):
        columns = ['Station ID', 'Sensor ID', 'Date', 'Time', 'Measurement']
        for file in self.list_files_from_today():
            df = pd.read_csv(file, names=columns, header=None)
            print(df.head())

if __name__ == "__main__":
    data = DataLoggerProcessor()
    data.move_files()
