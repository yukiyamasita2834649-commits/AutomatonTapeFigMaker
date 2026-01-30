from automaton_template import *

global_parent_path = "."


def main():
    TuringMachine()
    PushdownAutomaton()
    # CFLeqNPDA()


def TuringMachine():
    make_automaton_template("TuringMachine","",
                            [
                                ["q","\\triangleright aabb\\triangleleft",0]
                            ],
                            [],
                            True,
                            "TuringMachineExample",
                            "jlreq",
                            False,False,
                            False,True,"scale=1",
                            )

def PushdownAutomaton():
    make_automaton_template(
        "PushdownAutomaton",
        "",
        [["q", "aabb", 0, "\\triangleright ABC", 0]],
        [],
        False,
        "PushdownAutomaton",
        "jlreq",
        False,
        False,
        False,
        True,
        "scale=1",
    )


def CFLeqNPDA():
    make_automaton_template("CFL=NPDA","L(G)inL(M)",
                            [
                                ["q_G","\\sigma_1\\sigma_2\\cdots\\sigma_{n-1}\\sigma_n",0,"▷\\space\\space\\space\\space\\space",0],
                                ["q_G","\\sigma_1\\sigma_2\\cdots\\sigma_{n-1}\\sigma_n",0,"▷S\\space\\space\\space\\space",1],
                                ["q_G","\\sigma_1\\sigma_2\\cdots\\sigma_{n-1}\\sigma_n",0,"▷\\alpha_m\\alpha_{m-1}\\cdots\\alpha_1\\space",4],
                                ["q_G","\\sigma_1\\sigma_2\\cdots\\sigma_{n-1}\\sigma_n",0,"▷\\beta_m\\beta_{l-1}\\cdots\\beta_1\\space",4],
                                ["q_G","\\sigma_1\\sigma_2\\cdots\\sigma_{n-1}\\sigma_n",0,"▷\\sigma_n\\sigma_{n-1}\\cdots\\sigma_2\\sigma_1\\space",5],
                                ["q_{pop}","\\sigma_1\\sigma_2\\cdots\\sigma_{n-1}\\sigma_n",1,"▷\\sigma_n\\sigma_{n-1}\\cdots\\sigma_2\\space\\space",4],
                                ["q_{pop}","\\sigma_1\\sigma_2\\cdots\\sigma_{n-1}\\sigma_n",3,"▷\\sigma_n\\sigma_{n-1}\\space\\space\\space\\space",2],
                                ["q_{pop}","\\sigma_1\\sigma_2\\cdots\\sigma_{n-1}\\sigma_n",4,"▷\\sigma_n\\space\\space\\space\\space\\space",1],
                                ["q_{pop}","\\sigma_1\\sigma_2\\cdots\\sigma_{n-1}\\sigma_n",4,"▷\\space\\space\\space\\space\\space\\space",0],
                                ["q_{f}","\\sigma_1\\sigma_2\\cdots\\sigma_{n-1}\\sigma_n",4,"▷\\space\\space\\space\\space\\space\\space",0],
                            ],
                            [
                                "スタックに開始記号S置く",
                                "スタックで記号列導出$\\\\$S\\stackrel{*}{\\Rightarrow}\\alpha_1\\cdots\\alpha_{m-1}\\alpha_m ",
                                "スタックで記号列導出$\\\\$\\alpha_1\\cdots\\alpha_{m-1}\\alpha_m\\stackrel{*}{\\Rightarrow}\\beta_1\\cdots\\beta_{l-1}\\beta_l ",
                                "スタックで記号列導出$\\\\$\\beta_1\\cdots\\beta_{l-1}\\beta_l\\stackrel{*}{\\Rightarrow}\\sigma_1\\sigma_2\\cdots\\sigma_{n-1}\\sigma_n ",
                                "入力テープとスタックで$\\\\$文字一致したらpop．\\space\\sigma_1一致",
                                "入力テープとスタックの$\\\\$文字一致したらpop．\\space\\sigma_2一致",
                                "入力テープとスタックの$\\\\$文字一致したらpop．\\space\\sigma_{n-2}まで一致",
                                "入力テープとスタックの$\\\\$文字一致したらpop．\\space\\sigma_{n-1}まで一致",
                                "入力テープとスタックの$\\\\$文字一致したらpop．\\space\\sigma_n一致",
                                "入力読み切って，スタックからだったら受理",
                            ],False,
                            "cfg_to_npda",
                            "jlreq",
                            False,False,
                            False,True,"scale=0.5",
                            1,3,5,7
                            )
# 矢印の下の改行\\は$\\\\$を使う

if __name__ == "__main__":
    main()
