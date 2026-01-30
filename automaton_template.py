from make_tape2Andmake_tape1 import *

# オートマトンのテープ図の単体，または矢印で結んだ流れ図を作る関数．全ての関数の中で最も重要
def make_automaton_template(
    root_dir_name: str,  # 親フォルダ名
    sub_root_dir_name: str,  # 子フォルダ名．親フォルダ名と子フォルダ名の使い分けは例えば親：言語名(Pal)，子：語(abba)，他には親：言語(Pal)，子：受理するオートマトン(inNPDA)
    automaton_arrs: list,  # 状態、input tape, storage tapeの中身をまとめて記述した配列を作成
    arrow_descriptions: list,  # 状態遷移の矢印の下に書く図
    is_tape1: bool,  # Trueだったらk-lna, Falseだったらk-snaを作成
    filenames: str,  # 出来上がったファイルの名前(.texなし)
    documentclass: str,  # standaloneやjlreqなど入れたいパッケージを入れる。
    want_individual_pdfs: bool,  # オートマトンの構成図をひとつずつ作りたいときはTrue.
    want_mix_tex_and_pdf: bool,  # オートマトンの構成図を矢印でつないでいったファイルを作りたいときはTrue
    want_standalone_seperate_pdfs: bool,  # オートマトンの構成図を矢印でつないでいったファイルで，合わせたいとき
    want_integrate_standalones_tex_and_pdf: bool,  # オートマトンの構成図を矢印でつないでいったファイルで，合わせたいとき
    standalone_options: str,  # want_fix_fileがTrueで，includestandaloneのオプションのscale調整
    *seperate_file_number: int,  # オートマトン図の何個目で切っていくかを指定．0始まり．指定した数から別ファイルになる．
):
    """
    オートマトンのテープ図単体のpdf,texファイルと，それらを矢印でつないだテープの変遷図のpdf,texファイルを生成する．

        - root_dir_name: str,  親フォルダ名．この中のoutputフォルダにテープ図ファイルが生成される．

        - sub_root_dir_name: str,  子フォルダ名．""とすると，親フォルダ直下にoutputフォルダ作る．そうでなければ親フォルダの中に子フォルダが作られ，その中にoutputフォルダを生成する．親フォルダ名と子フォルダ名の使い分けは例えば親：言語名(Pal)，子：語(abba)，他には親：言語(Pal)，子：受理するオートマトン(inNPDA)

        - automaton_arrs: list,  状態、input tape, storage tapeの中身をまとめて記述した二次元listを入れる.例： [["q_0","▷w_1w_2\\cdots w_nw_n\\cdots w_2w_1◁",0,"▷□□□□□□□□",0],["q_{acc}", "▷aabbcccc◁", 9, "▷CCEC", 4]]

        - arrow_descriptions:list, 状態遷移の矢印の下に書く図

        - automaton_flag: bool,  Trueだったらk-lna, Falseだったらk-snaを作成

        - filenames: str,  生成する時のファイルの名前(.pdf,.texなどの拡張子は必要なし) pythonファイルを実行すると，filenamesに0から始まる半角数字が付いた名前になる．

        - documentclass: str,  standaloneやjlreqなど，入れたいdocumentclassの名前。

        - want_individual_pdfs: bool,  # オートマトンの構成図をひとつずつ作りたいときはTrue.

        - want_mix_tex_and_pdf: bool,  # オートマトンの構成図を矢印でつないでいったファイルを作りたいときはTrue

        - want_standalone_seperate_pdfs: bool,  # オートマトンの構成図を矢印でつないでいったファイルで，合わせたいとき

        - want_integrate_standalones_tex_and_pdf: bool,  # オートマトンの構成図を矢印でつないでいったファイルで，合わせたいとき

        - standalone_options: str, # want_fix_fileがTrueで，includestandaloneのオプションのscale調整

        - *seperate_file_number: int , # オートマトン図の何個目で切っていくかを指定．0始まり．指定した数から別ファイルになる．
    """
    # automaton_flag
    # True: k-lna
    # False: k-sna
    root_dir = root_dir_name
    if sub_root_dir_name != "":
        sub_root_dir = root_dir + "/" + sub_root_dir_name
    else:
        sub_root_dir = root_dir
    all_tikzpictures = preamble_text(documentclass)
    tmp_tex_code = ""
    tmp_tikzpictures = preamble_text(documentclass)
    sep_file_tape_number = sorted(seperate_file_number)
    tmp_index = 0
    if is_tape1:
        klnas = automaton_arrs
        for i, model_info_list in enumerate(klnas):
            if i <= len(klnas) - 1 and i >= 1:
                all_tikzpictures += arrow_tikzpicture(arrow_descriptions[i-1])
                tmp_tikzpictures += arrow_tikzpicture(arrow_descriptions[i-1])
            tmp_tex_code += use_tape1_maker(
                sub_root_dir,
                model_info_list,
                filenames + str(i),
                want_individual_pdfs,
            )
            all_tikzpictures += tmp_tex_code
            tmp_tikzpictures += tmp_tex_code

            if tmp_index <= len(sep_file_tape_number) - 1:
                if i == sep_file_tape_number[tmp_index]:
                    tmp_tikzpictures += footer_text()
                    make_standalone_tex(
                        sub_root_dir, filenames, tmp_tikzpictures, tmp_index
                    )
                    if want_standalone_seperate_pdfs:
                        compile_latex_to_pdf(
                            sub_root_dir
                            + "/output/"
                            + filenames
                            + "Sep"
                            + str(tmp_index)
                            + ".tex",
                            sub_root_dir + "/output/",
                        )
                        process_auxiliary_files(
                            sub_root_dir, filenames + "Sep" + str(tmp_index)
                        )
                    tmp_index += 1
                    tmp_tikzpictures = preamble_text(documentclass)
            tmp_tex_code = ""

    else:
        ksnas = automaton_arrs
        for i, model_info_list in enumerate(ksnas):
            if i <= len(ksnas) - 1 and i >= 1:
                all_tikzpictures += arrow_tikzpicture(arrow_descriptions[i-1])
                tmp_tikzpictures += arrow_tikzpicture(arrow_descriptions[i-1])
            tmp_tex_code += use_tape2_maker(
                sub_root_dir,
                model_info_list,
                filenames + str(i),
                want_individual_pdfs,
            )
            all_tikzpictures += tmp_tex_code
            tmp_tikzpictures += tmp_tex_code
            if tmp_index <= len(sep_file_tape_number)-1:
                if i == sep_file_tape_number[tmp_index]:
                    tmp_tikzpictures += footer_text()
                    make_standalone_tex(
                        sub_root_dir, filenames, tmp_tikzpictures, tmp_index
                    )
                    if want_standalone_seperate_pdfs:
                        compile_latex_to_pdf(
                            sub_root_dir
                            + "/output/"
                            + filenames
                            + "Sep"
                            + str(tmp_index)
                            + ".tex",
                            sub_root_dir + "/output/",
                        )
                        process_auxiliary_files(
                            sub_root_dir, filenames + "Sep" + str(tmp_index)
                        )
                    tmp_index += 1
                    tmp_tikzpictures = preamble_text(documentclass)
            tmp_tex_code = ""

    # 分割した所から一番最後までの処理
    tmp_tikzpictures += footer_text()
    make_standalone_tex(
        sub_root_dir, filenames, tmp_tikzpictures, tmp_index
    )
    if want_standalone_seperate_pdfs:
        compile_latex_to_pdf(
            sub_root_dir
            + "/output/"
            + filenames
            + "Sep"
            + str(tmp_index)
            + ".tex",
            sub_root_dir + "/output/",
        )
        process_auxiliary_files(
            sub_root_dir, filenames + "Sep" + str(tmp_index)
        )

    # すべてのtikzpictureを統合したファイル作成
    all_tikzpictures += footer_text()
    if want_mix_tex_and_pdf:
        make_mix_tizpictures_file(sub_root_dir, filenames, all_tikzpictures)

    # すべてのstandaloneを統合して，standaloneオプション付きのファイル生成
    if want_integrate_standalones_tex_and_pdf:
        make_integrate_standalones_tex_and_pdf(
            sub_root_dir,
            filenames,
            documentclass,
            len(seperate_file_number)+1,
            standalone_options,
        )


# すべてのtikzpictureを統合したファイルを作成する関数
def make_integrate_standalones_tex_and_pdf(
    parent_dir: str,
    filename: str,
    documentclass: str,
    the_number_of_standalone_files: int,
    standalone_option: str,
):
    line_break_code = (
        "\\begin{itemize}\n\t\t" "\\item []\n\t\t" "\\item []\n\t" "\\end{itemize}\n\t"
    )
    tex_code = (
        f"\\documentclass[]{{{documentclass}}}\n"  # jlreq or standalone
        "\\usepackage{tikz,amsfonts,standalone}\n\n"
        "\\usetikzlibrary{calc,arrows.meta,bending,positioning,decorations.pathreplacing}\n\n"
        "\\begin{document}\n"
    )
    for i in range(the_number_of_standalone_files):
        tex_code += f"\\includestandalone[{standalone_option}]{{{parent_dir}/output/{filename}Sep{str(i)}}}\n\t"
        if i != the_number_of_standalone_files - 1:
            tex_code += line_break_code
    tex_code += footer_text()
    with open(
        parent_dir + "/output/" + filename + "Integrate.tex", "w", encoding="utf-8"
    ) as outfile:
        outfile.write(tex_code)
    if os.path.isdir(parent_dir + "/output/") == False:
        os.makedirs(parent_dir + "/output/")
    compile_latex_to_pdf(
        parent_dir + "/output/" + filename + "Integrate.tex", parent_dir + "/output/"
    )
    process_auxiliary_files(parent_dir, filename + "Integrate")


# standaloneファイルの作成
def make_standalone_tex(
    parent_dir: str,
    filename: str,
    tmp_tikzpictures: str,
    tmp_index: int,
):
    with open(
        parent_dir + "/output/" + filename + "Sep" + str(tmp_index) + ".tex",
        "w",
        encoding="utf-8",
    ) as outfile:
        outfile.write(tmp_tikzpictures)
    if os.path.isdir(parent_dir + "/output/") == False:
        os.makedirs(parent_dir + "/output/")

    # compile_latex_to_pdf(
    #     sub_root_dir + "/output/" + filenames + "Sep" + str(tmp_index) + ".tex",
    #     sub_root_dir + "/output/",
    # )


# すべてのtikzpictureを統合したファイルを作成する関数
def make_mix_tizpictures_file(parent_dir: str, filename: str, all_tikzpictures: str):
    with open(
        parent_dir + "/output/" + filename + "Mix.tex", "w", encoding="utf-8"
    ) as outfile:
        outfile.write(all_tikzpictures)
    if os.path.isdir(parent_dir + "/output/") == False:
        os.makedirs(parent_dir + "/output/")
    compile_latex_to_pdf(
        parent_dir + "/output/" + filename + "Mix.tex", parent_dir + "/output/"
    )
    process_auxiliary_files(parent_dir, filename + "Mix")


# テープ図間を結ぶ矢印を作成する関数
def arrow_tikzpicture(arrow_description: str):
    return (
        "\\begin{tikzpicture}[baseline={(0,-1.6)}]\n\t\t"
        f"\\node[font=\\Large,align=center,red] (textbox) {{${arrow_description}$}};\n"
        f"\\draw[-{{Stealth[length=3mm]}},red,very thick] let \\p1=(textbox.north west),\\p2=(textbox.north east) in (\\x1,\\y1+10)-- (\\x2,\\y2+10);\n"
        # f"\\draw[-{{Stealth[length=3mm]}},red,very thick] (0,0) -- node[below=0.2,align=center,red,font=\\Large] {{${arrow_description}$}} (1,0);\n\t"
        "\\end{tikzpicture}\n\t"
    )
