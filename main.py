# summary.csvのhas_csv_under_aliceの列を読み込む
# trueであれば，csvファイルの睡眠段階の列からグラフを作成し保存する
# 出来れば，パワポに張り付ける
from utils import *
from py_color import PyColor
import pandas as pd


def main():
    pass

if __name__ == "__main__":
    # summary.csvを読み込む
    csv_file_path = os.path.join("c:/users/taiki/desktop/adding_sleep_datas/summary.csv")
    df = pd.DataFrame(csv_file_path)
    output_file_name = "c:/users/taiki/desktop/adding_sleep_datas/figures"
    input_file_root = "c:/users/taiki/desktop/adding_sleep_datas"

    # csvファイルの睡眠段階の列がtrueならばグラフを作成し，保存する関数を呼ぶ
    for input_file_name, has_csv in zip(df["dir_name"], df["has_csv_under_alice"]):
        if has_csv:
            print(PyColor.GREEN,
                  f"{input_file_name} has csv",
                  PyColor.END)
            input_file_name = os.path.join(input_file_root, input_file_name)
            make_ss_graph(input_dirname = input_file_name,
                          output_dirname = output_file_name)
        else:
            print(PyColor.RED,
                  f"{input_file_name} does not have csv",
                  PyColor.END)
