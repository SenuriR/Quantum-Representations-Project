from manim import *
from pathlib import Path

# can definitely make this portable-- not just hard coded epr pair

# this is the main driver
class QuantumRepsMultiView(Scene):
    def get_bloch_view(self, step_num):
        # === INSERT YOUR BLOCH IMAGE FILENAMES HERE ===
        filenames = {
            1: ("images/step1_0.png", "images/step1_1.png"),
            2: ("images/step2_0.png", "images/step2_1.png"),
            3: ("images/step3_0.png", "images/step3_1.png"),
        }

        q0_path, q1_path = filenames.get(step_num, (None, None))
        if not (q0_path and q1_path):
            raise ValueError(f"No Bloch sphere images found for step {step_num}.")

        if not (Path(q0_path).exists() and Path(q1_path).exists()):
            raise FileNotFoundError(f"Image files missing: {q0_path}, {q1_path}")

        img_q0 = ImageMobject(q0_path).scale(0.4).shift(LEFT * 1.5)
        img_q1 = ImageMobject(q1_path).scale(0.4).shift(RIGHT * 1.5)

        label_q0 = Text("Qubit 0", font_size=24).next_to(img_q0, DOWN)
        label_q1 = Text("Qubit 1", font_size=24).next_to(img_q1, DOWN)

        return Group(img_q0, img_q1, label_q0, label_q1)

    def get_vector_view(self, step_num):
        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage{braket}")

        if step_num == 1:
            return Tex(
                r"$\ket{00} = \begin{bmatrix} 1 \\ 0 \\ 0 \\ 0 \end{bmatrix}$",
                tex_template=tex_template
            )

        elif step_num == 2:
            return Tex(
                r"$\frac{1}{\sqrt{2}}(\ket{00} + \ket{10}) = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 0 \\ 1 \\ 0 \end{bmatrix}$",
                tex_template=tex_template
            )

        elif step_num == 3:
            return Tex(
                r"$\frac{1}{\sqrt{2}}(\ket{00} + \ket{11}) = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 0 \\ 0 \\ 1 \end{bmatrix}$",
                tex_template=tex_template
            )

    def get_circuit_view(self, step_num):
        x_start = 0
        width = 2.5
        gate_gap = 0.4
        qubit_spacing = 1.2
        x_end = x_start + width * 2

        y_q0 = qubit_spacing / 2
        y_q1 = -qubit_spacing / 2

        q0_label = Tex("$ |0> $").next_to([x_start - 0.4, y_q0, 0], LEFT)
        q1_label = Tex("$ |0> $").next_to([x_start - 0.4, y_q1, 0], LEFT)

        elements = [q0_label, q1_label]

        if step_num >= 1:
            t1_mid = x_start + width / 2
            line_q0_1a = Line([x_start, y_q0, 0], [t1_mid - gate_gap, y_q0, 0])
            line_q0_1b = Line([t1_mid + gate_gap, y_q0, 0], [x_start + width, y_q0, 0])
            line_q1_1 = Line([x_start, y_q1, 0], [x_start + width, y_q1, 0])

            h_gate = Square(0.6).move_to([t1_mid, y_q0, 0])
            h_label = Tex("H").scale(1.2).move_to(h_gate)
            h_group = VGroup(h_gate, h_label)

            elements += [line_q0_1a, h_group, line_q0_1b, line_q1_1]

        if step_num in [2, 3]:
            t2_mid = x_start + width + width / 2
            line_q0_2a = Line([x_start + width, y_q0, 0], [t2_mid - gate_gap, y_q0, 0])
            line_q0_2b = Line([t2_mid + gate_gap, y_q0, 0], [x_end, y_q0, 0])
            line_q1_2a = Line([x_start + width, y_q1, 0], [t2_mid - gate_gap, y_q1, 0])
            line_q1_2b = Line([t2_mid + gate_gap, y_q1, 0], [x_end, y_q1, 0])

            ctrl_dot = Dot(radius=0.07).move_to([t2_mid, y_q0, 0])
            tgt_circle = Circle(radius=0.15).move_to([t2_mid, y_q1, 0])
            vert_line = Line(ctrl_dot.get_center(), tgt_circle.get_center())
            cx_group = VGroup(ctrl_dot, tgt_circle, vert_line)

            elements += [line_q0_2a, cx_group, line_q0_2b, line_q1_2a, line_q1_2b]

        return VGroup(*elements).scale(0.9)

    def show_step(self, step_num, vec_q0, vec_q1):
        # Scale down each component
        circuit = self.get_circuit_view(step_num).scale(0.8).to_edge(LEFT).shift(UP * 0.5)
        vector = self.get_vector_view(step_num).scale(0.9).move_to(DOWN * 1.5)
        bloch = self.get_bloch_view(step_num).scale(0.6).to_edge(RIGHT).shift(UP * 0.5)

        self.play(FadeIn(circuit), FadeIn(vector), FadeIn(bloch))
        self.wait(4)
        self.play(FadeOut(circuit), FadeOut(vector), FadeOut(bloch))


    def construct(self):
        title = Text("EPR Pair Generation – Multi-View", font_size=40)
        self.play(FadeIn(title))
        self.wait(2)
        self.play(FadeOut(title))

        self.show_step(1, vec_q0=[0, 0, 1], vec_q1=[0, 0, 1])
        self.show_step(2, vec_q0=[1, 0, 0], vec_q1=[0, 0, 1])
        self.show_step(3, vec_q0=[1, 0, 0], vec_q1=[1, 0, 0])
