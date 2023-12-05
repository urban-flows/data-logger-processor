import glob
import os
from datetime import date
from pathlib import Path

import pandas as pd

root_path = os.getenv("DATA_ROOT_PATH")
output_path = os.getenv("OUTPUT_PATH")
text_file_path = os.getenv("FILES_EDITED_PATH")

today = "2021-08-17"

frequency_30 = ['0012']
frequency_300 = ['0810', '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010', '0013', '0014', '0015']
frequency_900 = ['0011']

columns = ['Station ID', 'Sensor ID', 'Date', 'Time', 'Measurements']

class DataLoggerProcessor:
    def __init__(self):
        # self.today_directory = Path(root_path) / str(date.today()).replace("-", r"/")
        self.today_input_directory = Path(root_path) / str(today).replace("-", r"/")
        self.today_output_directory = Path(output_path) / str(today).replace("-", r"/")
        self.today_output_directory.mkdir(parents=True, exist_ok=True)

    def timestamp_from_file(self):
        pass

    def list_files_from_today(self):
        paths = glob.glob(str(self.today_input_directory / "*"))
        return [paths[0]]

    def move_files(self):
        for file in self.list_files_from_today():
            df = pd.read_csv(file, names=columns, header=None, dtype=str)
            output_path_sensor = str(Path(self.today_output_directory) / df.iloc[0, 0])

            df['datetime'] = pd.to_datetime(df['Date'] + df['Time'], format='%Y%m%d%H%M%S')
            df_pivot = df.pivot(index='datetime', columns='Sensor ID', values='Measurements')
            df_pivot[frequency_30].dropna(how='all').to_csv(output_path_sensor + '_30_seconds')
            df_pivot[frequency_300].dropna(how='all').to_csv(output_path_sensor + '_300_seconds')
            df_pivot[frequency_900].dropna(how='all').to_csv(output_path_sensor + '_900_seconds')

    @staticmethod
    def write_to_tracking_file(file_name):
        with open(text_file_path, 'a') as file:
            file.write(file_name + "\n")


if __name__ == "__main__":
    data = DataLoggerProcessor()
    data.move_files()
