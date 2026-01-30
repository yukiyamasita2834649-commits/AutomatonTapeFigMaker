import re
# from icecream import ic

from tex_equation_tokenizer import tokenize_tex_equation
# from icecream import ic
def generate_tikz_tape(s: str, head: int, style: str,tape_style_flag:int,next_transition_function:str) -> str:
    """
    Generates LaTeX source code for a TikZ diagram representing the tape
    of a Turing machine with specified characteristics, in the style of
    Petzold's "The Annotated Turing".
    Parameters:
        * s: The input string to be displayed inside the tape's squares.
        * head: The index of the square to be highlighted with an ultra-thick
          border, representing the current position of the machine's head.
        * length: The number of squares (excluding extra squares) in the tape.
        * style: A string specifying some options for the tape. The presence of
          the characters 'c', 'l' or 'r' has the following effects:
            - 'c': Center the TikZ picture on the screen.
            - 'l': Add two extra squares at the beginning, with left edges
              missing and "..." displayed.
            - 'r': Add two extra squares at the end, with right edges
              missing and "..." displayed.
        * flag:
            - 0: input tape
            - 1: storage tape
        * next_transition_function:
            !未使用! 遷移するときに使う状態遷移関数。

            入力例）\\delta_2~\\delta_5
    Output: The LaTeX source code for generating the TikZ diagram.
    Writes: The LaTeX code to a file named "tikz_code.tex".
    """

    # nest=s.split("{")
    # new_s=list(nest[0])
    # for i,c in enumerate(nest[1:]):
    #     x = c.split("}")
    # ic(x)
    #     new_s.append(x[0])
    #     for j,d in enumerate(x[1:]):
    #         if c!="":
    #             new_s=new_s+list(d)
    # ic(nest)
    # ic(new_s)

    # tmp=[]
    # f=0
    # for i,c in enumerate(new_s):
    # ic(i,c,f,tmp)
    #     if f==3:
    #         f=0
    #     elif f==2:
    # ic(len(tmp),tmp)
    #         if c=="_":
    #             tmp[len(tmp)-1]=tmp[len(tmp)-1]+(c+"{"+new_s[i+1]+"}"+"]")
    #             f=3
    #             continue
    #             # end with lower track
    #         else:
    #             tmp[len(tmp)-1]=tmp[len(tmp)-1]+"}"

    #     elif f==1:
    #         if new_s[i-1]=="[":
    #             if c.endswith("^"):
    #                 # start with upper track
    #                 tmp.append("["+c+"{"+new_s[i+1])
    #                 f=2
    #             else:
    #                 tmp.append("["+c)
    #                 f=0
    #         else:
    #             tmp[len(tmp)-1]=tmp[len(tmp)-1]+"}"
    #             f=0
    #     elif c=="_":
    #         tmp[len(tmp)-1]=tmp[len(tmp)-1]+"_{"+new_s[i+1]
    #         f=1
    #     elif c=="[":
    #         f=1
    #         continue

    #     elif c.endswith("_") or c.endswith("^"):
    #         tmp.append(c+"{"+new_s[i+1])
    #         f=1
    #         continue
    #     elif c=="]":
    #         continue
    #     # elif c=="\\widehat" or c=="\\symbf":
    #     #     # commands
    #     #     tmp.append(c+"{")
    #     #     f=1
    #     else:
    #         tmp.append(c)

    new_s=tokenize_tex_equation(s)
    # ic(new_s)
    length=len(new_s)

    transitions=tokenize_tex_equation(next_transition_function)
    trans_length=len(transitions)

    # if tape_style_flag==1 and head+1==length:
    #     length=length+1
    # if len(new_s) > length:
    #     raise ValueError("The length of the string cannot exceed the number"
    #                      "of squares!")
    # if head >= length:
    #     raise ValueError("The given index exceeds the number of squares!")

    # asdf{\gamma}[\gamma]

    # Generate LaTeX document preamble and footer:
    # preamble = ("\\documentclass{jlreq}\n"
    #             "\\usepackage{tikz,amsfonts}\n\n"
    #             "\\usetikzlibrary{arrows.meta,bending,positioning}\n\n"
    #             "\\begin{document}\n")
    # footer = "\n\\end{document}"

    # 1辺の長さ
    one_edge_length=1.0

    # storage tape (stack)の幅
    stack_tape_position = tape_style_flag * (-3.5)

    # Begin the environments:
    tab_multiplier = 1
    tab = tab_multiplier * "\t"  # For proper indentation

    if 'c' in style:   # The picture should be centered.
        tikz_code=""
        # tikz_code = tab + "\\begin{center}\n"
        tab_multiplier += 1
        tab = tab_multiplier * "\t"  # Increase indentation inside `center`
    else:
        tikz_code=""

    # tikz_code += tab + "\\begin{tikzpicture}[remember picture]\n" # type: ignore
    tab_multiplier += 1
    tab += "\t"  # Increase indentation inside `tikzpicture` environment

    # Add extra squares at the left and right ends if necessary:
    left_extra = 2 if 'l' in style else 0
    right_extra = 2 if 'r' in style else 0

    # 例えば，a^{{n_2}}個という要素があったらa\\cdots aと変換する．
    str_changed_toThestring_to_midcdots=[] # a\\cdots aと変換した後の字句を格納するリスト
    # append_flag=False
    simply_concatenate_to_tmp_mode=0 # 転載モードとその深さ
    superscript_mode=False
    subcript_mode=False
    tmp=""
    for i,c in enumerate(new_s):

        if c=="}" and simply_concatenate_to_tmp_mode==1:
            # 転載モード終了
            simply_concatenate_to_tmp_mode=0
            tmp=tmp+c
            if superscript_mode==False:
                # 添字モードがoffの時は直接出力配列に連結。
                str_changed_toThestring_to_midcdots.append(tmp)
                tmp=""
        elif c=="}":
            # 転載モード１段上昇
            simply_concatenate_to_tmp_mode=simply_concatenate_to_tmp_mode-1
            tmp=tmp+c
        elif c=="{" and simply_concatenate_to_tmp_mode==0 :
            # 転載モード開始
            simply_concatenate_to_tmp_mode=simply_concatenate_to_tmp_mode+1
            tmp=tmp+c
        elif c=="{":
            # 転載モード１段下降
            simply_concatenate_to_tmp_mode=simply_concatenate_to_tmp_mode+1
            tmp=tmp+c
        elif simply_concatenate_to_tmp_mode==0:
            if subcript_mode:
                # 下付き添字モード終了
                str_changed_toThestring_to_midcdots[len(str_changed_toThestring_to_midcdots)-1] = str_changed_toThestring_to_midcdots[len(str_changed_toThestring_to_midcdots)-1]+"_"+c
                subcript_mode=False
            if superscript_mode:
                # 添字モード終了
                # a...aの列を作る。何個続くかも保存
                if tmp=="":
                    # 添字モード中に転載モードやってなかった時
                    str_changed_toThestring_to_midcdots.append("\\cdots")
                    str_changed_toThestring_to_midcdots.append(
                        [str_changed_toThestring_to_midcdots[len(str_changed_toThestring_to_midcdots)-2], c]
                    )
                superscript_mode=False
            elif c=="_":
                # 下付き添字モード開始
                subcript_mode=True
                # str_changed_toThestring_to_midcdots[len(str_changed_toThestring_to_midcdots)-1]=str_changed_toThestring_to_midcdots[len(str_changed_toThestring_to_midcdots)-1]+c
            elif c=="^":
                # 上付き添字モード開始
                superscript_mode=True
                # str_changed_toThestring_to_midcdots[len(str_changed_toThestring_to_midcdots)-1]=str_changed_toThestring_to_midcdots[len(str_changed_toThestring_to_midcdots)-1]+c
            elif re.match(r"^.\^\{.*\}$", c) != None or re.match(r"^.\^.+$", c) != None:
                # a...aの列を作る。何個続くかも保存
                str_changed_toThestring_to_midcdots.append(c.split("^")[0])
                str_changed_toThestring_to_midcdots.append("\\cdots")
                str_changed_toThestring_to_midcdots.append(
                    [c.split("^")[0], c.split("^")[1]]
                )
            else:
                # 基本：出力配列にappend
                str_changed_toThestring_to_midcdots.append(c)
        else:
            # 転載モードでそのままtmpに連結
            tmp=tmp+c
        if simply_concatenate_to_tmp_mode==0 and superscript_mode==True and tmp!="":
            # 上付き添字モード中に転載モードやってた時
            str_changed_toThestring_to_midcdots.append("\\cdots")
            str_changed_toThestring_to_midcdots.append(
                [
                    str_changed_toThestring_to_midcdots[
                        len(str_changed_toThestring_to_midcdots) - 2
                    ],
                    tmp,
                ]
            )
            superscript_mode=False
        elif simply_concatenate_to_tmp_mode==0 and subcript_mode==True and tmp!="":
            # 下付き添字モード中に転載モードやってた時
            str_changed_toThestring_to_midcdots[len(str_changed_toThestring_to_midcdots)-1]=str_changed_toThestring_to_midcdots[len(str_changed_toThestring_to_midcdots)-1]+"_"+tmp
            subcript_mode=False
        # modeを使わない字句解析。a^{B}しかcdotsに変換しない。
        # if re.match("^.\^\{.*\}$", c) != None:
        #     # a...aの列を作る。何個続くかも保存
        #     str_changed_toThestring_to_midcdots.append(c.split("^")[0])
        #     str_changed_toThestring_to_midcdots.append("\\cdots")
        #     str_changed_toThestring_to_midcdots.append(
        #         [c.split("^")[0], c.split("^")[1]]
        #     )
        # elif c!="{" and c!="}":
        #     if append_flag:
        #         str_changed_toThestring_to_midcdots[
        #             len(str_changed_toThestring_to_midcdots) - 1
        #         ] = (
        #             str_changed_toThestring_to_midcdots[
        #                 len(str_changed_toThestring_to_midcdots) - 1
        #             ]
        #             + f"{{{c}}}"
        #         )
        #         append_flag = False
        #     elif c=="^" or c=="_":
        #         str_changed_toThestring_to_midcdots[len(str_changed_toThestring_to_midcdots)-1]=f"{{{str_changed_toThestring_to_midcdots[len(str_changed_toThestring_to_midcdots)-1]}}}{c}"
        #         append_flag=True
        #     # total_length=total_length+1
        #     else:
        #         str_changed_toThestring_to_midcdots.append(c)
    total_length=len(str_changed_toThestring_to_midcdots)
    # ic(str_changed_toThestring_to_midcdots)
    # ic(str_changed_toThestring_to_midcdots)

    # total_length = length + left_extra + right_extra

    # Define the coordinate points:
    tikz_code += tab + "% Specify the positions of the vertices:\n"
    for i in range(total_length + 4):
        # Bottom vertices of the squares:
        tikz_code += tab + f"\\coordinate ({tape_style_flag}A{i}) at ({one_edge_length * i}, 0+{stack_tape_position}, 0);\n"
        # Top vertices of the squares:
        tikz_code += tab + f"\\coordinate ({tape_style_flag}B{i}) at ({one_edge_length * i}, {one_edge_length}+{stack_tape_position}, 0);\n"
    # ic(tikz_code)
    # Add the string's characters to the diagram:
    tikz_code += tab + "% Specify the position of the characters:\n"
    lenc2_flag=False
    for i, c in enumerate(str_changed_toThestring_to_midcdots):
        # The C_i represent the centers of each cell:： coordinate行追加
        tikz_code += (tab +
                    f"\\coordinate ({tape_style_flag}C{i + left_extra}) at"
                    f"({one_edge_length * (i + left_extra) + one_edge_length/2.0}, {one_edge_length/2.0}+{stack_tape_position}, 0);\n")
        if lenc2_flag:
            # a^{n_2}をa\\cdots aにしているので，その時の中括弧の処理
            if tape_style_flag==0: # 入力テープの時
                # 上側に中括弧付ける．
                tikz_code+=(tab+
                            f"\\draw[decorate,decoration={{brace,amplitude=10pt}}] ({tape_style_flag}B{i-3+left_extra}) -- ({tape_style_flag}B{i+left_extra}) node[midway,above=8pt] {{${str_changed_toThestring_to_midcdots[i-1][1]}$}};\n")
            else: # 作業用テープなどの時
                # 下側に中括弧付ける．
                tikz_code += (
                    tab
                    + f"\\draw[decorate,decoration={{brace,amplitude=10pt}}] ({tape_style_flag}A{i+left_extra}) -- ({tape_style_flag}A{i-3+left_extra}) node[midway,below=8pt] {{${str_changed_toThestring_to_midcdots[i-1][1]}$}};\n"
                )
            lenc2_flag=False
        if type(c) is list and len(c)==2:
            lenc2_flag=True
            # 文字をセルに書き込む
            # ic()
            tikz_code += (
                tab + f"\\node at ({tape_style_flag}C{i + left_extra}) {{${c[0]}$}};\n"
            )
        else:
            # 文字をセルに書き込む
            # ic(c)
            tikz_code += tab + f"\\node at ({tape_style_flag}C{i + left_extra}) {{${c}$}};\n"
    if lenc2_flag:
        # a^{n_2}をa\\cdots aにしているので，その時の中括弧の処理
        if tape_style_flag == 0:  # 入力テープの時
            # 上側に中括弧付ける．
            tikz_code += (
                tab
                + f"\\draw[decorate,decoration={{brace,amplitude=10pt}}] ({tape_style_flag}B{len(str_changed_toThestring_to_midcdots)-3+left_extra}) -- ({tape_style_flag}B{len(str_changed_toThestring_to_midcdots)+left_extra}) node[midway,above=8pt] {{${str_changed_toThestring_to_midcdots[len(str_changed_toThestring_to_midcdots)-1][1]}$}};\n"
            )
        else:  # 作業用テープなどの時
            # 下側に中括弧付ける．
            tikz_code += (
                tab
                + f"\\draw[decorate,decoration={{brace,amplitude=10pt}}] ({tape_style_flag}A{len(str_changed_toThestring_to_midcdots)+left_extra}) -- ({tape_style_flag}A{len(str_changed_toThestring_to_midcdots)-3+left_extra}) node[midway,below=8pt] {{${str_changed_toThestring_to_midcdots[len(str_changed_toThestring_to_midcdots)-1][1]}$}};\n"
            )
        lenc2_flag = False

    # Add "..." to the specified squares if asked to:
    if 'l' in style:
        tikz_code += tab + f"\\coordinate ({tape_style_flag}D) at ({one_edge_length}, {one_edge_length/2.0}+{stack_tape_position}, 0);\n"
        tikz_code += tab + f"\\node at ({tape_style_flag}D){{$ \\cdots $}};\n"
    if 'r' in style:
        tikz_code += (tab +
                      f"\\coordinate ({tape_style_flag}E) at"
                      f"({one_edge_length * (left_extra+total_length+1)}, {one_edge_length/2.0}+{stack_tape_position}, 0);\n")
        tikz_code += tab + f"\\node at ({tape_style_flag}E) {{$ \\cdots $}};\n"

    # Draw the vertical edges:
    tikz_code += tab + "% Draw vertical edges:\n"
    for i in range(left_extra, total_length + left_extra+1):
        tikz_code += tab + f"\\draw ({tape_style_flag}B{i}) -- ({tape_style_flag}A{i});\n"
    # for i in range(left_extra, left_extra+total_length + right_extra+1):
    # if "r" not in style:
    #     tikz_code += tab + f"\\draw ({flag}B{length + left_extra}) -- ({flag}A{length + left_extra});\n"
    # if 'l' not in style:
    #     tikz_code += tab + f"\\draw ({flag}B0) -- ({flag}A0);\n"

    # Draw the bottom and top edges:
    tikz_code += tab + "% Draw horizontal edges:\n"
    b = 1 if 'l' in style else 0
    e = total_length + 1 + left_extra if 'r' in style else total_length
    tikz_code += tab + f"\\draw ({tape_style_flag}A{b}) -- ({tape_style_flag}A{e});\n"
    tikz_code += tab + f"\\draw ({tape_style_flag}B{b}) -- ({tape_style_flag}B{e});\n"

    # Draw an ultra-thick square grid around the specified head's index:
    tikz_code += tab + "% Draw ultra-thick grid at head's position:\n"
    tikz_code += (tab +
                  f"\\draw[ultra thick] ({tape_style_flag}B{head + left_extra}) --"
                  f"({tape_style_flag}A{head + left_extra})"
                  f"-- ({tape_style_flag}A{head + left_extra + 1}) --"
                  f"({tape_style_flag}B{head + left_extra + 1}) -- cycle;\n")

    # Close the environments:
    tab_multiplier -= 1
    tab = tab_multiplier * "\t"

    # tikz_code += tab + "\\end{tikzpicture}\n"
    if 'c' in style:
        tab_multiplier -= 1
        tab = tab_multiplier * "\t"
        # tikz_code += tab + "\\end{center}\n"
    # tikz_code += "\\medskip\n\t"

    # # Combine the preamble, TikZ code, and footer:
    # full_latex_code = preamble + tikz_code + footer

    # # Write the output to a file:
    # with open(filename, "w",encoding="utf-8") as outfile:
    #     outfile.write(full_latex_code)
    # print("The TikZ code has been successfully generated!")

    return tikz_code

# ic(tokenize_tex_equation("▷a^{n_2}b^{n_2}bb^{m_2-n_2-1}c^{p_2}\\#\\cdots ◁"))
# ic(len(tokenize_tex_equation("▷a^{n_2}b^{n_2}bb^{m_2-n_2-1}c^{p_2}\\#\\cdots ◁")))

# print(generate_tikz_tape("▷■^{n_2}□X_1\\cdots ◁",2,"c",1,""))


# Examples:
# if __name__ == "__main__":

#     # Example 1:
#     s = "r e c u r s i o n !"
#     head = 15
#     length = 20
#     style = "c"
#     tikz_code = generate_tikz_tape(s, head, length, style,)

#     # Example 2:
#     s = "@1 1 0 1 0 1 1x0 1"
#     head = 14
#     length = 20
#     style = "lrc"
#     tikz_code = generate_tikz_tape(s, head, length, style)

#     # Example 3:
#     s = "@0 1x0 0 1x0 1x0 1x"
#     head = 7
#     length = 20
#     style = "rc"
#     tikz_code = generate_tikz_tape(s, head, length, style)

#     # Example 4:
#     s = "3:j0[Y!ZaLh?8/btm27"
#     head = 1
#     length = 20
#     style = "lc"
#     tikz_code = generate_tikz_tape(s, head, length, style)
