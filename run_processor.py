import glob
import os
from pathlib import Path
from processor import station_data_processor
from datetime import datetime
root_path = os.getenv("DATA_ROOT_PATH")
text_file_path = os.getenv("FILES_EDITED_PATH")
today = "2021-08-17"
checked_files_path = os.getenv("CHECKED_FILES_PATH")

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


def check_tracking_file(file_path: Path):
    date_format = "%Y-%m-%d"
    if file_path.is_file():
        with file_path.open("r") as file:
            date = file.readline()
            try:
                date = datetime.strptime(date, date_format).date()
            except ValueError:
                print("First line of file was not the correct date format")
                raise
        if date != datetime.now().date():
            file_path.rename(Path(str(file_path) + ".old"))
        else:
            return

    with file_path.open("w") as file:
        file.write(str(datetime.now().date()))


if __name__ == "__main__":
    check_tracking_file(Path(checked_files_path))
    # today_input_directory = Path(root_path) / str(today).replace("-", r"/")
    # paths = glob.glob(str(today_input_directory / "*"))
    # for path in paths:
    #     processor = station_data_processor.StationDataProcessor(path)
    #     processor.process_file()

