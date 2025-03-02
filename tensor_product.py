from manim import *

# TODO: making portable --> define common gates as matrices --> then plug n chug
class TensorProductStepByStep(Scene):
    def construct(self):
        # Define basis vectors
        scale_factor = 0.8  # Scaling to fit everything on screen
        ket0 = MathTex(r"|0\rangle = \begin{bmatrix}1 \\ 0\end{bmatrix}").scale(scale_factor)
        ket1 = MathTex(r"|1\rangle = \begin{bmatrix}0 \\ 1\end{bmatrix}").scale(scale_factor)
        tensor_symbol = MathTex(r"\otimes").scale(scale_factor)

        # Positioning
        ket0.move_to(LEFT * 2.5 + UP * 1.2)
        ket1.move_to(LEFT * 2.5 + DOWN * 1.2)
        tensor_symbol.move_to(LEFT * 1.2)

        # Show basis vectors
        self.play(Write(ket0), Write(ket1), Write(tensor_symbol))
        self.wait(1)

        # Tensor product expansion step-by-step
        step1 = MathTex(r"\begin{bmatrix}1 \\ 0\end{bmatrix} \otimes \begin{bmatrix}1 \\ 0\end{bmatrix} =").scale(scale_factor)
        step1.next_to(tensor_symbol, RIGHT * 1.5)
        self.play(Write(step1))
        self.wait(1)

        step2 = MathTex(r"\begin{bmatrix}1 \cdot 1 \\ 1 \cdot 0 \\ 0 \cdot 1 \\ 0 \cdot 0\end{bmatrix} = \begin{bmatrix}1 \\ 0 \\ 0 \\ 0\end{bmatrix}").scale(scale_factor)
        step2.next_to(step1, RIGHT * 1.5)
        self.play(Write(step2))
        self.wait(2)

        # Expand for all basis combinations
        full_basis = MathTex(
            r"|00\rangle = \begin{bmatrix}1 \\ 0 \\ 0 \\ 0\end{bmatrix}, "
            r"|01\rangle = \begin{bmatrix}0 \\ 1 \\ 0 \\ 0\end{bmatrix}, "
            r"|10\rangle = \begin{bmatrix}0 \\ 0 \\ 1 \\ 0\end{bmatrix}, "
            r"|11\rangle = \begin{bmatrix}0 \\ 0 \\ 0 \\ 1\end{bmatrix}"
        ).scale(scale_factor)
        full_basis.next_to(step2, DOWN * 1.5)
        
        # Show the full tensor product space
        self.play(Write(full_basis))
        self.wait(3)
        
        # Fade out everything
        self.play(FadeOut(ket0), FadeOut(ket1), FadeOut(tensor_symbol),
                  FadeOut(step1), FadeOut(step2), FadeOut(full_basis))
