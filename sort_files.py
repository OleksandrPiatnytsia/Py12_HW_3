from threading import Thread
from time import time
import logging
from pathlib import Path
import sys


def getfiles(path):
    file_path = Path(path)

    if not file_path.exists():
        return None

    if file_path.is_dir():
        for include_file in file_path.iterdir():
            getfiles(include_file)
    else:
        logging.debug(f'FileName:  {file_path.resolve()}')


def get_folders(path):
    file_path = Path(path)

    folders = []
    if file_path.is_dir():

        folders.append(file_path.resolve())

        for include_file in file_path.iterdir():
            if include_file.is_dir():
                folders += get_folders(include_file)

    return folders


def transfer_files(path, base_path):
    logging.debug(f'File replacing from folder:  {path} is started')

    file_path = Path(path)

    for include_file in file_path.iterdir():
        if not include_file.is_dir():

            base_folder_name = f"{base_path}\\{include_file.suffix.replace('.', '').upper()}"
            base_folder = Path(base_folder_name)
            base_folder.mkdir(exist_ok=True)

            if include_file.parent == Path(base_folder_name):
                continue

            counter = 0
            while True:

                new_path = Path(
                    f"{base_folder_name}\\{include_file.name.replace(include_file.suffix, '')}{'' if counter == 0 else '_' + str(counter)}{include_file.suffix}")

                counter += 1
                if not new_path.exists():
                    break

            include_file.rename(new_path)

            logging.debug(f'Replaced:  {new_path}')


def main():
    try:
        path = sys.argv[1]
    except IndexError:
        print(f"Path for sorting is empty!")
        return None

    logging.basicConfig(level=logging.DEBUG)

    timestamp = time()

    folders = get_folders(path)

    threads = []
    for i in folders:
        thread = Thread(target=transfer_files, args=(i, path))
        thread.start()
        threads.append(thread)

    [el.join() for el in threads]

    # folders.reverse()
    #
    # for i in folders:
    #     if str(i) != path:
    #         logging.debug(f'Deleting empty folder:  {i.absolute()}')
    #         i.rmdir()
    #
    # logging.debug(f'performing time:  {time() - timestamp}')


if __name__ == '__main__':
    main()
