import os
from pathlib import Path

import pandas as pd


output_path = os.getenv("OUTPUT_PATH")
text_file_path = os.getenv("FILES_EDITED_PATH")

columns = ['Station ID', 'Sensor ID', 'Date', 'Time', 'Measurements']

frequencies = {
    "frequency_30": ['0012'],
    "frequency_300": ['0810', '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010', '0013',
                      '0014', '0015'],
    "frequency_900": ['0011'],
}


class StationDataProcessor:
    def __init__(self, filename: str):
        self.filename = filename
        self.today_output_directory = None
        self.station_id = None
        self.df = None
        self.file_start_time = None

    def process_file(self):
        self._read_pivot_file()
        self._get_datetime_from_df()
        self._set_and_create_output_dir()
        output_path_sensor = str(Path(self.today_output_directory) / self.station_id)
        for frequency in frequencies:
            frequency_file_name = output_path_sensor + '_' + frequency
            self.df[frequencies[frequency]].dropna(how='all').to_csv(frequency_file_name)
            self.write_to_tracking_file(frequency_file_name)

    def _read_pivot_file(self):
        df = pd.read_csv(self.filename, names=columns, header=None, dtype=str)
        self.station_id = df.iloc[0, 0]
        df['datetime'] = pd.to_datetime(df['Date'] + df['Time'], format='%Y%m%d%H%M%S')
        self.df = df.pivot(index='datetime', columns='Sensor ID', values='Measurements')

    def _get_datetime_from_df(self):
        self.file_start_time = self.df.index[0]

    def _set_and_create_output_dir(self):
        self.today_output_directory = Path(output_path) / str(self.file_start_time.year) / str(self.file_start_time.month) / str(self.file_start_time.day)
        self.today_output_directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def write_to_tracking_file(filename: str):
        with open(text_file_path, 'a') as file:
            file.write(filename + "\n")
