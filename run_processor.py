import glob
import os
from pathlib import Path
from processor import station_data_processor

root_path = os.getenv("DATA_ROOT_PATH")
text_file_path = os.getenv("FILES_EDITED_PATH")
today = "2021-08-17"


def get_today_files_not_processed():
    today_input_directory = Path(root_path) / str(today).replace("-", r"/")

    with open(text_file_path, 'r') as file:
        files_processed = []
        for line in file:
            line_stripped = line.rstrip("\n")
            files_processed.append(line_stripped)

    files = glob.glob(str(today_input_directory / "*"))
    files_not_processed = set(files) - set(files_processed)
    return list(files_not_processed)


if __name__ == "__main__":

    today_input_directory = Path(root_path) / str(today).replace("-", r"/")
    paths = glob.glob(str(today_input_directory / "*"))
    for path in paths:
        processor = station_data_processor.StationDataProcessor(path)
        processor.process_file()

