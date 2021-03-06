from posixpath import dirname
from pprint import pprint
import numpy as np
import glob as glob
import sys, os
from dataclasses import dataclass
from py_color import PyColor
import pandas as pd

# make sleep stage graph
def make_ss_graph(input_dirname : str,
                  output_dirname : str) -> None:
    
# from folder name(which is specified in csv), does folder name exit or not
def folder_exists(csv_file : str) -> None:
    root_dir = os.path.join("c:/users/taiki/Desktop/adding_sleep_datas")
    df = pd.read_csv(csv_file, header=0)
    subjetcts_list = df["subjects_date_and_name"]
    for subject in subjetcts_list:
        if os.path.exists(os.path.join(root_dir,
                                       subject)):
            print(PyColor.GREEN,
                  f"{subject} exists!",
                  PyColor.END)
        else:
            print(PyColor.RED,
                  f"{subject} does not exist",
                  PyColor.END)

# return root dir which is targeted
def return_target_folders() -> list:
    root_dir = os.path.join("c:/users/taiki/Desktop/adding_sleep_datas")  # NOTE : network server need \\
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

# 
def write2csv(csv_file : str, added_dict : dict) -> None:
    df = pd.DataFrame(added_dict)
    df.to_csv(csv_file)
    return

# aboarting list class
@dataclass
class AboartingList:
    ignoring_file_in_emoor_sleep_data_list = \
    [
        "xlsx",
        "csv",
        "?????????",
        "140421_KINJYO",
        "figures"
    ]

if __name__ == "__main__":
    folders = return_target_folders()
    aboarter = AboartingList()
    counter = 0
    target_folders_list = abandon_folders(target_folders=folders,
                                          aboarting_list=aboarter.ignoring_file_in_emoor_sleep_data_list)
    has_ssf_list = list()
    dirname_list = list()
    for target_dir in target_folders_list:
        has_ssf = catch_csv(target_dir=target_dir)
        _, dir_name = os.path.split(target_dir)
        dirname_list.append(dir_name)
        if has_ssf:
            counter += 1
            print(PyColor.GREEN,
                  f"*** {dir_name} has csv file under alice folder ***",
                  PyColor.END)
            has_ssf_list.append(True)
        else:
            print(PyColor.RED,
                  f"*** {dir_name} does not have csv file under alice folder ***",
                  PyColor.END)
            has_ssf_list.append(False)
    print(counter)
    # FIXME : ??????????????????????????????????????????????????????
    csv_file = os.path.join("c:/users/taiki/desktop/adding_sleep_datas/summary.csv")
    has_ssf_dict = {"dir_name":dirname_list,
                    "has_csv_under_alice":has_ssf_list}
    # write into summary.csv
    write2csv(csv_file=csv_file, added_dict = has_ssf_dict)