import glob
import os
from pathlib import Path
from processor import station_data_processor

root_path = os.getenv("DATA_ROOT_PATH")

today = "2021-08-17"
"""
class DataLoggerProcessor:
    def __init__(self):
        # self.today_directory = Path(root_path) / str(date.today()).replace("-", r"/")
        self.today_input_directory = Path(root_path) / str(today).replace("-", r"/")

    def list_files_from_today(self):
        paths = glob.glob(str(self.today_input_directory / "*"))
        return [paths[0]]

    def move_files(self):




    @staticmethod
    def timestamp_from_file(file):
        pass


    @staticmethod
    def write_to_tracking_file(file_name):
        with open(text_file_path, 'a') as file:
            file.write(file_name + "\n")

"""

if __name__ == "__main__":
    today_input_directory = Path(root_path) / str(today).replace("-", r"/")
    paths = glob.glob(str(today_input_directory / "*"))
    for path in paths:
        processor = station_data_processor.StationDataProcessor(path)
        processor.process_file()

