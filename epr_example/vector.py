from manim import *

class EPRPairMatrixWalkthrough(Scene):
    def construct(self):
        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage{braket}")

        # Title
        title = Tex(r"EPR Pair Generation – Step-by-Step", font_size=48, tex_template=tex_template)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        ## Stage 1: Initial state
        initial_label = Tex(r"Initial State:", font_size=36)
        initial_ket = Tex(r"$\ket{00} = \begin{bmatrix}1 \\ 0 \\ 0 \\ 0\end{bmatrix}$", font_size=36, tex_template=tex_template)

        group1 = VGroup(initial_label, initial_ket).arrange(DOWN, center=True).move_to(ORIGIN)
        self.play(FadeIn(group1))
        self.wait(2)
        self.play(FadeOut(group1))

        ## Stage 2: Apply H ⊗ I
        h_step_label = Tex(r"Apply $H \otimes I$ on $\ket{00}$:", font_size=36, tex_template=tex_template)
        h_matrix = Tex(r"""$
        H \otimes I =
        \frac{1}{\sqrt{2}}
        \begin{bmatrix}
        1 & 0 & 1 & 0 \\
        0 & 1 & 0 & 1 \\
        1 & 0 & -1 & 0 \\
        0 & 1 & 0 & -1
        \end{bmatrix}
        $""", font_size=34, tex_template=tex_template)

        h_mult = Tex(r"""$
        (H \otimes I)\ket{00} =
        \frac{1}{\sqrt{2}} \begin{bmatrix}1 \\ 0 \\ 1 \\ 0\end{bmatrix}
        = \frac{1}{\sqrt{2}}(\ket{00} + \ket{10})
        $""", font_size=34, tex_template=tex_template)

        group2 = VGroup(h_step_label, h_matrix, h_mult).arrange(DOWN, buff=0.5).scale(0.95).move_to(ORIGIN)
        self.play(FadeIn(group2))
        self.wait(3)
        self.play(FadeOut(group2))

        ## Stage 3: Apply CNOT
        cnot_label = Tex(r"Apply CNOT:", font_size=36)
        cnot_matrix = Tex(r"""$
        \text{CNOT} =
        \begin{bmatrix}
        1 & 0 & 0 & 0 \\
        0 & 1 & 0 & 0 \\
        0 & 0 & 0 & 1 \\
        0 & 0 & 1 & 0
        \end{bmatrix}
        $""", font_size=34)

        cnot_mult = Tex(r"""$
        \text{CNOT}\left(\frac{1}{\sqrt{2}} \begin{bmatrix}1 \\ 0 \\ 1 \\ 0\end{bmatrix}\right)
        =
        \frac{1}{\sqrt{2}} \begin{bmatrix}1 \\ 0 \\ 0 \\ 1\end{bmatrix}
        = \frac{1}{\sqrt{2}}(\ket{00} + \ket{11})
        $""", font_size=34, tex_template=tex_template)

        final_state = Tex(r"Final EPR State: $\ket{\Phi^+} = \frac{1}{\sqrt{2}}(\ket{00} + \ket{11})$", font_size=36, color=YELLOW, tex_template=tex_template)

        group3 = VGroup(cnot_label, cnot_matrix, cnot_mult, final_state).arrange(DOWN, buff=0.5).scale(0.95).move_to(ORIGIN)
        self.play(FadeIn(group3))
        self.wait(4)
        self.play(Indicate(final_state))
        self.wait(2)
