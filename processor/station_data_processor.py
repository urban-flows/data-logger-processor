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
        self.today_output_directory = Path(output_path) / str(today).replace("-", r"/")
        self.today_output_directory.mkdir(parents=True, exist_ok=True)
        self.station_id = None
        self.df_pivot = None

    def process_file(self):
        self._read_pivot_file()
        self._get_datetime_from_df()
        output_path_sensor = str(Path(self.today_output_directory) / self.station_id)
        for frequency in frequencies:
            frequency_file_name = output_path_sensor + '_' + frequency
            self.df_pivot[frequencies[frequency]].dropna(how='all').to_csv(frequency_file_name)
            self.write_to_tracking_file(frequency_file_name)

    def _read_pivot_file(self):
        df = pd.read_csv(self.filename, names=columns, header=None, dtype=str)
        self.station_id = df.iloc[0, 0]
        df['datetime'] = pd.to_datetime(df['Date'] + df['Time'], format='%Y%m%d%H%M%S')
        self.df_pivot = df.pivot(index='datetime', columns='Sensor ID', values='Measurements')

    def _get_datetime_from_df(self):
        self.file_start_time = self.df.iloc[0, 0]

    @staticmethod
    def write_to_tracking_file(filename: str):
        with open(text_file_path, 'a') as file:
            file.write(filename + "\n")
