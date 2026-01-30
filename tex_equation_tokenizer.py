# TeXの数式を受け取ってそこから字句を切り出すpython古コード
import re

def tokenize_tex_equation(equation:str):
    tokens = []
    i = 0
    while i < len(equation):
        # 角括弧[]で囲まれた部分の処理
        if equation[i] == '[':
            end = find_matching_bracket(equation, i, '[', ']')
            if end != -1:
                tokens.append(equation[i:end+1])
                i = end + 1
                continue

        # 空白の処理
        if equation[i].isspace():
            i += 1
            continue

        # ギリシャ文字と添字/指数の複合処理
        complex_token = extract_complex_token(equation[i:])
        if complex_token:
            tokens.append(complex_token)
            i += len(complex_token)
        else:
            # その他の文字の処理（1文字ずつ）
            tokens.append(equation[i])
            i += 1

    return tokens

def find_matching_bracket(text, start, open_bracket, close_bracket):
    stack = []
    for i in range(start, len(text)):
        if text[i] == open_bracket:
            stack.append(open_bracket)
        elif text[i] == close_bracket:
            if stack:
                stack.pop()
                if not stack:
                    return i
    return -1  # マッチする閉じ括弧が見つからない場合

def extract_complex_token(text):
    # ギリシャ文字パターン
    greek_pattern = r"\\([a-zA-Z]+|#)"

    # 上付き文字と下付き文字のパターン（1文字または{}で囲まれた部分）
    script_pattern = r'(?:\^|_)(?:\{[^}]*\}|[^{}\s])'

    # 複合パターン（ギリシャ文字または通常の文字 + オプションの上付き/下付き）
    complex_pattern = f'({greek_pattern}|[a-zA-Z]|■|□)({script_pattern})?({script_pattern})?'

    match = re.match(complex_pattern, text)
    if match:
        return match.group(0)

    return None

# 使用例
equations = [
    "▷a^{n_2}b^{n_2}bb^{m_2-n_2-1}c^{p_2}\\#\\cdots ◁",
    "スタックで記号列導出$\\\\$S\\overset{*}{\\Rightarrow}\\alpha_1\\cdots\\alpha_{m-1}\\alpha_m ",
    "▷a^{n_2}b^{m_2}c^{p_2}\\#\\cdots◁",
    "▷■^{n_2}■□□□□",
    "▷a^{n_2}b^{m_2}c^{p_2}\\sharp\\cdots◁",
    r"\alpha_1",
    r"\alpha_1BB",
    r"\gamma^{(a)}_{ab}",
    r"ab^3",
    r"[^{□}_{\gamma^{e}_{i-1}}]",
    r"\cdots x_2",
    r"\gamma A",
    r"E = mc^2 + \alpha_1 + \beta_{test} + [x_i^2]",
    r"▷x_1x_2\cdots x_{n-1}x_n◁",
    r"▷□□□□□□□◁",
]
# print(tokenize_tex_equation(equations[0]))

# for eq in equations:
    # result = tokenize_tex_equation(eq)
#     print(f"入力: {eq}")
#     print(f"出力: {result}")
#     print()
