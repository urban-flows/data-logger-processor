import glob
import sys
import os
from pathlib import Path
from processor import station_data_processor
from datetime import datetime
root_path = Path(os.getenv("DATA_ROOT_PATH"))
text_file_path = Path(os.getenv("FILES_EDITED_PATH"))
today = "2021-08-17"
checked_files_path = Path(os.getenv("FILES_CHECKED_PATH"))
lock_file_path = Path(os.getenv("LOCK_FILE_PATH"))


def get_today_files_not_processed(files_processed: list[str]):
    today_input_directory = Path(root_path) / str(today).replace("-", r"/")

    # with open(text_file_path, 'r') as file:
    #     files_processed = []
    #     for line in file:
    #         line_stripped = line.rstrip("\n")
    #         files_processed.append(line_stripped)
    #
    files_all = glob.glob(str(today_input_directory / "*"))
    if files_processed:
        files_not_processed = set(files_all) - set(files_processed)
    else:
        files_not_processed = set(files_all)
    return list(files_not_processed)


def check_tracking_file(file_path: Path):
    date_format = "%Y-%m-%d"
    files = []
    if file_path.is_file():
        with file_path.open("r") as file:
            date = file.readline().rstrip("\n")
            try:
                date = datetime.strptime(date, date_format).date()
            except ValueError:
                print("First line of file was not the correct date format")
                raise
            if date != datetime.now().date():
                file_path.rename(Path(str(file_path) + ".old"))
                return files
            else:
                files = file.read()
                return files

    with file_path.open("w") as file:
        file.write(str(datetime.now().date()) + "\n")


def set_files_processed(file_path: Path, processed_files: list[str]):
    with file_path.open("a") as file:
        for processed_file in processed_files:
            file.write(processed_file + "\n")


def check_create_lock_file(file_path: Path):
    if file_path.exists():
        print("Lock file already exists, program will exit")
        sys.exit()
    else:
        open(file_path, 'w').close()  # Create lock file and close, similar to touch in unix.

if __name__ == "__main__":
    files_processed = check_tracking_file(checked_files_path)
    files_not_processed = get_today_files_not_processed(files_processed)
    set_files_processed(checked_files_path, files_not_processed)
    check_create_lock_file(lock_file_path)
    for path in files_not_processed:
        processor = station_data_processor.StationDataProcessor(path)
        processor.process_file()
    lock_file_path.unlink()
