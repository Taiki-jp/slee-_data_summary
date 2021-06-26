from posixpath import dirname
from pprint import pprint
import numpy as np
import glob as glob
import sys, os
from dataclasses import dataclass
from py_color import PyColor

# return root dir which is targeted
def return_target_folders() -> list:
    root_dir = os.path.join("\\\gamma", "SleepData", "EMOOR_sleepData")  # NOTE : network server need \\
    # show root dir if there is not directory
    if not os.path.exists(root_dir):
        print(f"{root_dir} does not exist")
        sys.exit(1)
    # return all folders(files) under the root dir
    return glob.glob(os.path.join(root_dir, "*"))

# confirm whether datas should be abandoned or not
def should_abondon(target_list : list, key_list : list) -> list:
    aboundon_list = [False for _ in range(len(target_list))]
    for counter, target_folder in enumerate(target_list):
        _, dir_name = os.path.split(target_folder)
        for key_name in key_list:
            if key_name in dir_name:
                aboundon_list[counter] = True
                print(PyColor.RED,
                      f"{dir_name} was caught by key name({key_name})", 
                      PyColor.END)
                break
    return aboundon_list

# abandon some files or folders that are specified in key list
def abandon_folders(target_folders : list, aboarting_list : list) ->  list:
    aboundon_list = should_abondon(target_list=target_folders,
                                   key_list=aboarting_list)
    _returned_list = list()
    for is_aboundaned, target_folder in zip(aboundon_list, target_folders):
        if not is_aboundaned:
            _returned_list.append(target_folder)
    return _returned_list     

# target folder has sleep stage data under alice folder?
def has_sleep_stage_file(target_dir : str) -> bool:
    alice_path = os.path.join(target_dir, "ALICE")
    for _, _, filenames in os.walk(alice_path):
        for filename in filenames:
            if "SleepStage" in filename or \
                "SpeepStage" in filename or \
                "PSG" in filename:
                return True
    return False

# target folder
def catch_csv(target_dir : str) -> bool:
    alice_path = os.path.join(target_dir, "ALICE")
    under_alice_folders = glob.glob(os.path.join(alice_path, "*"))
    for abs_path in under_alice_folders:
        _, dir_name = os.path.split(abs_path)
        if "csv" in dir_name:
            return True
    return False

# aboarting list class
@dataclass
class AboartingList:
    ignoring_file_in_emoor_sleep_data_list = \
    [
        "xlsx",
        "csv",
        "未整理",
        "140421_KINJYO"
    ]

if __name__ == "__main__":
    folders = return_target_folders()
    aboarter = AboartingList()
    counter = 0
    target_folders_list = abandon_folders(target_folders=folders,
                                          aboarting_list=aboarter.ignoring_file_in_emoor_sleep_data_list)
    for target_dir in target_folders_list:
        has_ssf = catch_csv(target_dir=target_dir)
        _, dir_name = os.path.split(target_dir)
        if has_ssf:
            counter += 1
            print(PyColor.GREEN,
                  f"*** {dir_name} has csv file under alice folder ***",
                  PyColor.END)
    print(counter)