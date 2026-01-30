from generate_tikz_tape import generate_tikz_tape


def preamble_text(
    documentclass: str,
):
    preamble = (
        f"\\documentclass[]{{{documentclass}}}\n"  # jlreq or standalone
        "\\usepackage{tikz,amsfonts}\n\n"
        "\\usetikzlibrary{calc,arrows.meta,bending,positioning,decorations.pathreplacing}\n\n"
        "\\begin{document}\n"
    )
    return preamble


def footer_text():
    footer = "\n\\end{document}"
    return footer


def two_tape_model(
    state: str,
    input_cells: str,
    input_head: int,
    storage_cells: str,
    storage_head: int,
    output_file_name: str,
    input_tape_style_flag: str,
    output_tape_style_flag: str,
    next_transition_function: str,
    wantInidividuals: bool,
):
    input_latex_code = "\\begin{tikzpicture}[remember picture]\n\t"
    input_latex_code += generate_tikz_tape(
        input_cells, input_head, input_tape_style_flag, 0, next_transition_function
    )
    storage_latex_code = generate_tikz_tape(
        storage_cells, storage_head, output_tape_style_flag, 1, next_transition_function
    )

    # レジスタノード作成
    # register_code = f"\t\t\t\\node [left=0.35 of 0A{input_head+1}] (regTo1) {{}};\n" # ここでinput headの位置調整
    # register_code += f"\t\t\t\\node [left=0.35 of 1B{storage_head+1}] (r2) {{}};\n"  # ここでstorage headの位置調整
    register_code = f"\t\t\t\\node [below=0.3 of 0C{input_head}] (regTo1) {{}};\n" # ここでinput headの位置調整
    register_code += f"\t\t\t\\node [above=0.3 of 1C{storage_head}] (r2) {{}};\n"  # ここでstorage headの位置調整
    register_code
    register_code += f"\t\t\t\\node [above=-0.28 of r2] (regTo2) {{}};\n"
    register_code += (
        f"\t\t\t\\node[below=0.85 of regTo1,draw=black,rectangle] (reg) {{${state}$}};\n"
    )
    register_code += f"\t\t\t\\node[above=0.3 of regTo2] (stor2) {{}};\n"
    # register_code+=f"\t\t\t\\node[]  (stor1) at (\\xrs,\\ystc2) {{}};\n"
    # register_code+=f"\t\t\t\\node[below=0.2 of reg] (stor1) {{}};\n"
    # register_code+=f"\t\t\t\\node[above=-0.24 of reg] (regFrom1) {{}};\n"
    # register_code+=f"\t\t\t\\node[below=-0.18 of reg] (regFrom2) {{}};\n"
    # register_code+=f"\t\t\t\\draw ;\n"
    # register_code+=f"\t\t\t\\draw (stor1) -- (stor2);\n"
    register_code += (
        f"\t\t\t\\draw [-{{Stealth[length=2mm]}}] (reg.north) -- (regTo1);\n"
    )
    register_code += f"\t\t\t\\draw [-{{Stealth[length=2mm]}}] let \\p1 = (reg.south),\\p2 = (stor2.center) in (reg.south) -- (\\x1,\\y2) -- (stor2.center) -- (regTo2);\n\t\t"

    register_code += "\\end{tikzpicture}\n\t"

    # \node[rectangle] (reg) {$state$};
    # \path (reg) edge[->] (0B{input_head});

    # \path[line width=1mm] (reg) edge[->] (1B{storage_head});

    full_code = (
        preamble_text("jlreq")
        + input_latex_code
        + storage_latex_code
        + register_code
        + footer_text()
    )
    # Write the output to a file:
    if wantInidividuals:
        with open(output_file_name, "w", encoding="utf-8") as outfile:
            outfile.write(full_code)
    # print("The TikZ code has been successfully generated!")
    return input_latex_code + storage_latex_code + register_code


def one_tape_model(
    state: str,
    storage_cells: str,
    storage_head: int,
    output_file_name: str,
    tape_style_flag: str,
    next_transition_function: str,
    wantInidividuals: bool,
):
    storage_latex_code = "\\begin{tikzpicture}[remember picture]\n\t"

    # storage tape作成
    storage_latex_code += generate_tikz_tape(
        storage_cells, storage_head, tape_style_flag, 1, next_transition_function
    )

    # レジスタノード作成
    register_code = (
        f"\t\t\t\\node [above=0.27 of 1C{storage_head+2}] (regTo) {{}};\n\t\t"
    )
    register_code += (
        f"\\node [above=1.5 of regTo,draw=black,rectangle] (reg) {{${state}$}};\n\t\t"
    )
    # register_code+=f"\\node[below=-0.25 of reg] (regFrom) {{}};\n\t"
    register_code += f"\\draw [-{{Stealth[length=2mm]}}] (reg.south) -- (regTo);\n\t"

    register_code += "\\end{tikzpicture}\n\t"

    # コード生成
    full_code = (
        preamble_text("jlreq") + storage_latex_code + register_code + footer_text()
    )

    # Write the output to a file:
    if wantInidividuals:
        with open(output_file_name, "w", encoding="utf-8") as outfile:
            outfile.write(full_code)
    # print("The TikZ code has been successfully generated!")
    return storage_latex_code + register_code


# def concatenate_models(tikz_text_src:str,tikz_text_dst:str):
# arrow_tikz = (
#     "\\end{tikzpicture}\n\t"
#     "\\begin{tikzpicture}\n\t"
#     "\\node (a) at (0,0) {};\n"
#     "\\node (b) at (1,0) {};\n"
#     "\\draw[-{Stealth[length=3mm]},red,very thick] (a) -- (b);\n"
#     "\\end{tikzpicture}\n\t"
# )
# concatenate_text=tikz_text_src+arrow_tikz+tikz_text_dst
# return concatenate_text
