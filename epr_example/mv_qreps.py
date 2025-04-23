from manim import *

class QuantumRepsMultiView(ThreeDScene):

    def get_bloch_sphere(self, state_vector_endpoint=[0, 0, 1], sphere_color=YELLOW):
        bloch_sphere = Sphere(radius=1).set_fill(opacity=0.3).set_stroke(WHITE, 0.6)

        x_axis = Arrow3D([-1.5, 0, 0], [1.5, 0, 0], color=WHITE)
        y_axis = Arrow3D([0, -1.5, 0], [0, 1.5, 0], color=WHITE)
        z_axis = Arrow3D([0, 0, -1.5], [0, 0, 1.5], color=WHITE)

        state_vector_arrow = Arrow3D([0, 0, 0], state_vector_endpoint, color=sphere_color)

        def state_label(tex_str, pos):
            return Tex(tex_str, color=WHITE).move_to(pos).rotate(PI / 2, axis=RIGHT).rotate(PI - PI / 6, axis=OUT)

        ket_0 = state_label(r"$\left|0\right\rangle$", z_axis.get_end() + 0.3 * OUT)
        ket_1 = state_label(r"$\left|1\right\rangle$", z_axis.get_start() + 0.3 * IN)
        ket_plus = state_label(r"$\left|+\right\rangle$", x_axis.get_end() + 0.3 * RIGHT)
        ket_minus = state_label(r"$\left|-\right\rangle$", x_axis.get_start() + 0.3 * LEFT)
        ket_plus_i = state_label(r"$\left|+i\right\rangle$", y_axis.get_end() + 0.3 * UP)
        ket_minus_i = state_label(r"$\left|-i\right\rangle$", y_axis.get_start() + 0.3 * DOWN)

        axes_group = VGroup(x_axis, y_axis, z_axis)
        state_labels = VGroup(ket_0, ket_1, ket_plus, ket_minus, ket_plus_i, ket_minus_i)
        bloch_group = VGroup(bloch_sphere, axes_group, state_labels, state_vector_arrow).scale(0.6)
        return bloch_group

    def get_bloch_view(self, vec_q0, vec_q1):
        q0 = self.get_bloch_sphere(vec_q0).shift(LEFT * 1.5)
        q1 = self.get_bloch_sphere(vec_q1).shift(RIGHT * 1.5)
        return VGroup(q0, q1)

    def get_vector_view(self, step_num):
        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\\usepackage{braket}")

        if step_num == 1:
            return Tex(r"$\\ket{00} = \\begin{bmatrix}1 \\\\ 0 \\\\ 0 \\\\ 0\\end{bmatrix}$", tex_template=tex_template)
        elif step_num == 2:
            return Tex(r"""
                $\\frac{1}{\\sqrt{2}}(\\ket{00} + \\ket{10}) =
                \\frac{1}{\\sqrt{2}} \\begin{bmatrix}1 \\\\ 0 \\\\ 1 \\\\ 0\\end{bmatrix}$
            """, font_size=32, tex_template=tex_template)
        elif step_num == 3:
            return Tex(r"""
                $\\frac{1}{\\sqrt{2}}(\\ket{00} + \\ket{11}) =
                \\frac{1}{\\sqrt{2}} \\begin{bmatrix}1 \\\\ 0 \\\\ 0 \\\\ 1\\end{bmatrix}$
            """, font_size=32, tex_template=tex_template)

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

        if step_num == 2 or step_num == 3:
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
        circuit = self.get_circuit_view(step_num).move_to(LEFT * 5)
        vector = self.get_vector_view(step_num).move_to(ORIGIN)
        bloch = self.get_bloch_view(vec_q0, vec_q1).move_to(RIGHT * 5)

        self.play(FadeIn(circuit), FadeIn(vector), FadeIn(bloch))
        self.wait(4)
        self.play(FadeOut(circuit), FadeOut(vector), FadeOut(bloch))

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        title = Text("EPR Pair Generation – Multi-View", font_size=40)
        self.play(FadeIn(title))
        self.wait(2)
        self.play(FadeOut(title))

        self.show_step(1, vec_q0=[0, 0, 1], vec_q1=[0, 0, 1])
        self.show_step(2, vec_q0=[1, 0, 0], vec_q1=[0, 0, 1])
        self.show_step(3, vec_q0=[1, 0, 0], vec_q1=[1, 0, 0])
