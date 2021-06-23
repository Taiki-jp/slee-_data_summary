from pprint import pprint
import numpy as np
import glob2 as glob
import sys, os


# return root dir which is targeted
def return_root_dir() -> list:
    root_dir = os.path.join("\\\gamma", "SleepData", "EMOOR_sleepData")  # NOTE : network server need \\
    # show root dir if there is not directory
    if not os.path.exists(root_dir):
        print(f"{root_dir} does not exist")
        sys.exit(1)
    # return all folders(files) under the root dir
    return glob.glob(os.path.join(root_dir, "*"))

if __name__ == "__main__":
    pprint(return_root_dir())
    
    