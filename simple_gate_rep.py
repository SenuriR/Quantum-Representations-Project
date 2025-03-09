from manim import *

class QuantumGateMatrices(Scene):
    def construct(self):
        self.gate_name = "Identity Gate (I)"
        title = Title("Matrix Representations of Common Quantum Gates")
        self.play(Write(title))
        self.wait(1)
        
        gates = [
            ("Identity Gate (I)", MathTex(r"I = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}")),
            ("Pauli-X Gate (X)", MathTex(r"X = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}")),
            ("Pauli-Y Gate (Y)", MathTex(r"Y = \begin{bmatrix} 0 & -	i \\ 	i & 0 \end{bmatrix}")),
            ("Pauli-Z Gate (Z)", MathTex(r"Z = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}")),
            ("Hadamard Gate (H)", MathTex(r"H = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}")),
            ("CNOT Gate", MathTex(r"\text{CNOT} = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{bmatrix}"))
        ]

        self.gates_dict = {gate_name: math_tex for gate_name, math_tex in gates}
        print(self.gates_dict)

        matrix_tex = self.gates_dict[self.gate_name]
        print(f"matrix_tex: {matrix_tex}")

        gate_label = Tex(self.gate_name).scale(1.2)
        group = VGroup(gate_label, matrix_tex).arrange(DOWN, buff=0.5)
        
        self.play(Write(gate_label))
        self.wait(1)
        self.play(FadeIn(matrix_tex))
        self.wait(2)
        self.play(FadeOut(group))
            
        self.play(FadeOut(title))
        self.wait(1)


        def get_matrix_rep(gate_name):
            matrix_tex = self.gates_dict[gate_name]
            print(f"matrix_tex: {matrix_tex}")

            gate_label = Tex(gate_name).scale(1.2)
            group = VGroup(gate_label, matrix_tex).arrange(DOWN, buff=0.5)
            
            self.play(Write(gate_label))
            self.wait(1)
            self.play(FadeIn(matrix_tex))
            self.wait(2)
            self.play(FadeOut(group))
'''
        for gate_name, matrix_tex in gates:
            gate_label = Tex(gate_name).scale(1.2)
            group = VGroup(gate_label, matrix_tex).arrange(DOWN, buff=0.5)
            
            self.play(Write(gate_label))
            self.wait(1)
            self.play(FadeIn(matrix_tex))
            self.wait(2)
            self.play(FadeOut(group))
            
        self.play(FadeOut(title))
        self.wait(1)
'''