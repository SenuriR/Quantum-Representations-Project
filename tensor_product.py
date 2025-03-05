from manim import *

class TensorProductForQuantum(Scene):
    def construct(self):
        # Define scaling factor for fitting elements
        scale_factor = 0.65  # Slightly reduced to fit screen better
        text_scale = 0.9  # Scale down text elements
        
        # Introduction text
        intro_text = Text("Understanding the Tensor Product in Quantum Theory", font_size=32)
        intro_text.to_edge(UP)
        self.play(Write(intro_text))
        self.wait(2)
        self.play(FadeOut(intro_text))

        # Define basis vectors
        ket0 = MathTex(r"|0\rangle = \begin{bmatrix}1 \\ 0\end{bmatrix}").scale(scale_factor)
        ket1 = MathTex(r"|1\rangle = \begin{bmatrix}0 \\ 1\end{bmatrix}").scale(scale_factor)
        tensor_symbol = MathTex(r"\otimes").scale(scale_factor)

        # Positioning
        ket0.move_to(LEFT * 3 + UP * 2)
        ket1.move_to(LEFT * 3 + DOWN * 2)

        # Show basis vectors
        self.play(Write(ket0), Write(ket1))
        self.wait(1)
        self.play(FadeOut(ket0), FadeOut(ket1))

        # Transition text
        transition_text = Text("When we take the tensor product of two qubits, we get four possible basis states.", font_size=28).scale(text_scale)
        transition_text.to_edge(UP)
        self.play(Write(transition_text))
        self.wait(3)

        # Step-by-step tensor product derivation in a single row layout
        tensor_expansion = [
            (r"|0\rangle \otimes |0\rangle =", r"\begin{bmatrix}1 \\ 0\end{bmatrix} \otimes \begin{bmatrix}1 \\ 0\end{bmatrix}", r"= \begin{bmatrix}1 \\ 0 \\ 0 \\ 0\end{bmatrix}"),
            (r"|0\rangle \otimes |1\rangle =", r"\begin{bmatrix}1 \\ 0\end{bmatrix} \otimes \begin{bmatrix}0 \\ 1\end{bmatrix}", r"= \begin{bmatrix}0 \\ 1 \\ 0 \\ 0\end{bmatrix}"),
            (r"|1\rangle \otimes |0\rangle =", r"\begin{bmatrix}0 \\ 1\end{bmatrix} \otimes \begin{bmatrix}1 \\ 0\end{bmatrix}", r"= \begin{bmatrix}0 \\ 0 \\ 1 \\ 0\end{bmatrix}"),
            (r"|1\rangle \otimes |1\rangle =", r"\begin{bmatrix}0 \\ 1\end{bmatrix} \otimes \begin{bmatrix}0 \\ 1\end{bmatrix}", r"= \begin{bmatrix}0 \\ 0 \\ 0 \\ 1\end{bmatrix}")
        ]

        start_x = -4.5  # Adjusted for better centering
        y_position = 0  # Keep all elements in a single row
        x_spacing = 3.5  # Reduced horizontal spacing to fit all elements

        for i, (label, equation, result) in enumerate(tensor_expansion):
            label_tex = MathTex(label).scale(scale_factor)
            equation_tex = MathTex(equation).scale(scale_factor)
            result_tex = MathTex(result).scale(scale_factor).set_color(YELLOW)  # Highlight final basis vectors
            
            x_pos = start_x + i * x_spacing  # Spread elements in one row with reduced spacing
            
            label_tex.move_to([x_pos, y_position, 0])
            equation_tex.next_to(label_tex, DOWN * 0.6)
            result_tex.next_to(equation_tex, DOWN * 0.6)
            
            self.play(Write(label_tex))
            self.wait(1)
            self.play(Write(equation_tex))
            self.wait(1)
            self.play(Write(result_tex))
            self.wait(2)
        
        

        # Conclusion text
        conclusion_text = Text("These basis states span the 4D space of two qubits!", font_size=28).scale(text_scale)
        conclusion_text.to_edge(DOWN)
        self.play(Write(conclusion_text))
        self.wait(3)
        
        # Fade out everything
        self.play(FadeOut(conclusion_text))
