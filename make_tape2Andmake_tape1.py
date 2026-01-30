# from icecream import ic

# 実行の際は起動するときのディレクトリに注意。
from generate_tikz_model import *
from compile_latex import compile_latex_to_pdf
import os, shutil

# def main():
#     parent_path=""
#     which="s"   # ここ変更
#     if which=="s":
#         make_tape2(parent_path)
#     elif which=="l":
#         make_tape1(parent_path)


# tape2本のs作成
def use_tape2_maker(
    parent_path: str, one_tape2s_arr: list, filename: str, wantIndividuals: bool
):
    """
    入力：
        - parent_path: str,

        - one_tape2s_arr: list,

        - filename: str,

        - wantIndividuals: bool

    出力： tape2本の図単体.texのtikzpicture環境コード
        \\begin{tikzpicture}
            tape2本の単体のコード
        \\end{tikzpicture}
    """
    tape2 = one_tape2s_arr
    latex_files = filename + ".tex"
    if os.path.isdir(parent_path + "/output") == False:
        os.makedirs(parent_path + "/output")
    two_tape_model_tikzpicture = two_tape_model(
        tape2[0],
        tape2[1],
        tape2[2],
        tape2[3],
        tape2[4],
        parent_path + "/output/" + latex_files,
        "c",
        "rc",
        "",
        wantIndividuals,
    )
    if wantIndividuals:
        compile_latex_to_pdf(
            parent_path + "/output/" + latex_files, parent_path + "/output"
        )
        # 補助ファイル移動
        process_auxiliary_files(parent_path, filename)
    # os.remove(latex_files+".aux")
    # os.remove(latex_files+".log")
    return two_tape_model_tikzpicture
    # latex_files=""


# tape1本作成
def use_tape1_maker(
    parent_path: str, one_tape1s_arr: list, filename: str, wantIndividuals: bool
):
    """
    出力： tape1本の図単体.texのtikzpicture環境コード
        \\begin{tikzpicture}
            tape1本の単体のコード
        \\end{tikzpicture}
    """
    tape1 = one_tape1s_arr
    latex_files = filename + ".tex"
    if os.path.isdir(parent_path + "/output") == False:
        os.makedirs(parent_path + "/output")
    one_tape_model_tikzpicture = one_tape_model(
        tape1[0],
        tape1[1],
        tape1[2],
        parent_path + "/output/" + latex_files,
        "lrc",
        "",
        wantIndividuals,
    )
    if wantIndividuals:
        compile_latex_to_pdf(
            parent_path + "/output/" + latex_files, parent_path + "/output"
        )
        # 補助ファイル移動
        process_auxiliary_files(parent_path, filename)

    return one_tape_model_tikzpicture
    # latex_files=""


# .auxや.logファイルの処理
def process_auxiliary_files(
    parent_path: str,
    tex_filename: str,
):
    if os.path.isdir(parent_path + "/auxs") == False:
        os.makedirs(parent_path + "/auxs")
    if os.path.isfile(parent_path + "/auxs/" + tex_filename + ".aux") == False:
        shutil.move(
            parent_path + "/output/" + tex_filename + ".aux", parent_path + "/auxs/"
        )
    else:
        os.remove(parent_path + "/auxs/" + tex_filename + ".aux")
        shutil.move(
            parent_path + "/output/" + tex_filename + ".aux", parent_path + "/auxs/"
        )
    if os.path.isdir(parent_path + "/logs") == False:
        os.makedirs(parent_path + "/logs")
    if os.path.isfile(parent_path + "/logs/" + tex_filename + ".log") == False:
        shutil.move(
            parent_path + "/output/" + tex_filename + ".log", parent_path + "/logs/"
        )
    else:
        os.remove(parent_path + "/logs/" + tex_filename + ".log")
        shutil.move(
            parent_path + "/output/" + tex_filename + ".log", parent_path + "/logs/"
        )


# tape2本のs作成
def make_tape2(parent_path: str):
    tape2s = [["q_0", "▷x_1x_2\\cdots x_{n-1}x_n◁", 0, "▷□□□□□□□", 0]]

    for i, c in enumerate(tape2s):
        latex_files = "Inittape2introduction.tex"
        # latex_files="tape2Arrnew"+str(i)+".tex";
        two_tape_model(c[0], c[1], c[2], c[3], c[4], latex_files, "c", "rc", "", True)
        compile_latex_to_pdf(latex_files, parent_path + "/output")

    latex_files = ""


# tape1本作成
def make_tape1(parent_path: str):
    tape1s = [
        ["q", "▷\\cdots B\\gamma^{(0)}_i\\cdots ◁", 3],
        ["q", "▷\\cdots BB\\cdots ◁", 2],
        ["p", "▷\\cdots BB\\cdots ◁", 3],
    ]
    for i, c in enumerate(tape1s):
        latex_files = f"1Lna{i}.tex"
        # latex_files="tape1Arr"+str(i)+".tex";
        one_tape_model(c[0], c[1], c[2], latex_files, "lrc", "", True)
        compile_latex_to_pdf(latex_files, parent_path + "/output")


# if __name__ == "__main__":
#     main()
