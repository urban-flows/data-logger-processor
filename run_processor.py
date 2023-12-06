import glob
import os
from pathlib import Path
from processor import station_data_processor

root_path = os.getenv("DATA_ROOT_PATH")

today = "2021-08-17"

if __name__ == "__main__":
    today_input_directory = Path(root_path) / str(today).replace("-", r"/")
    paths = glob.glob(str(today_input_directory / "*"))
    for path in paths:
        processor = station_data_processor.StationDataProcessor(path)
        processor.process_file()

