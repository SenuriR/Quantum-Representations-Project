from manim import *

class TensorProductForQuantum(Scene):
    def construct(self):
        # Define scaling factor for fitting elements
        scale_factor = 0.7  # Slightly reduced to fit screen
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

        # Explain tensor product conceptually
        explanation = Text("The tensor product expands the space to represent joint states", font_size=28).scale(text_scale)
        explanation.to_edge(UP)
        self.play(Write(explanation))
        self.wait(3)
        self.play(FadeOut(explanation))

        # Step-by-step tensor product derivation in a grid layout
        tensor_expansion = [
            (r"|0\rangle \otimes |0\rangle =", r"\begin{bmatrix}1 \\ 0\end{bmatrix} \otimes \begin{bmatrix}1 \\ 0\end{bmatrix}", r"= \begin{bmatrix}1 \\ 0 \\ 0 \\ 0\end{bmatrix}"),
            (r"|0\rangle \otimes |1\rangle =", r"\begin{bmatrix}1 \\ 0\end{bmatrix} \otimes \begin{bmatrix}0 \\ 1\end{bmatrix}", r"= \begin{bmatrix}0 \\ 1 \\ 0 \\ 0\end{bmatrix}"),
            (r"|1\rangle \otimes |0\rangle =", r"\begin{bmatrix}0 \\ 1\end{bmatrix} \otimes \begin{bmatrix}1 \\ 0\end{bmatrix}", r"= \begin{bmatrix}0 \\ 0 \\ 1 \\ 0\end{bmatrix}"),
            (r"|1\rangle \otimes |1\rangle =", r"\begin{bmatrix}0 \\ 1\end{bmatrix} \otimes \begin{bmatrix}0 \\ 1\end{bmatrix}", r"= \begin{bmatrix}0 \\ 0 \\ 0 \\ 1\end{bmatrix}")
        ]

        start_x = -3  # Left alignment
        start_y = 1.5  # Start below the ket vectors
        x_spacing = 5  # Horizontal spacing
        y_spacing = -1.5  # Vertical spacing

        for i, (label, equation, result) in enumerate(tensor_expansion):
            label_tex = MathTex(label).scale(scale_factor)
            equation_tex = MathTex(equation).scale(scale_factor)
            result_tex = MathTex(result).scale(scale_factor)
            
            col = i % 2  # Two columns
            row = i // 2  # Two rows
            
            label_tex.move_to([start_x + col * x_spacing, start_y + row * y_spacing, 0])
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
        self.play(FadeOut(ket0), FadeOut(ket1), FadeOut(tensor_symbol),
                  FadeOut(conclusion_text))
