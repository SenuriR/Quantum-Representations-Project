from manim import *
from two_bloch import TwoQubitColoredBlochSpheres
from circuit import Circuit
from entangled_qubits import TwoEntangledQubits
from vector import EPRPairMatrixWalkthrough

# THIS IS THE CODE WE NEED TO EDIT 5/2/25

class QuantumReps(ThreeDScene):
    def get_bloch_sphere(self, sphere_color=BLUE, state_vector_endpoint=[0, 0, 1.5]):
        state_vector_endpoint = np.array(state_vector_endpoint, dtype=float)
        bloch_sphere = Sphere(radius=1)
        bloch_sphere.set_fill(color=sphere_color, opacity=0.5)
        bloch_sphere.set_stroke(color=sphere_color, opacity=0.6)

        x_axis = Arrow3D(start=[-1.5, 0, 0], end=[1.5, 0, 0], color=WHITE)
        y_axis = Arrow3D(start=[0, -1.5, 0], end=[0, 1.5, 0], color=WHITE)
        z_axis = Arrow3D(start=[0, 0, -1.5], end=[0, 0, 1.5], color=WHITE)
        state_vector_arrow = Arrow3D(start=[0, 0, 0], end=state_vector_endpoint, color=RED)

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
        bloch_group = VGroup(bloch_sphere, axes_group, state_labels, state_vector_arrow)
        bloch_group.scale(1.2)

        return bloch_group

    def construct(self):
        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage{braket}")

        original_phi = self.camera.get_phi()
        original_theta = self.camera.get_theta()
        original_gamma = self.camera.get_gamma()
        original_focal_distance = self.camera.focal_distance

        caption = Text("Hadamard gate on $q_0$", font_size=28).to_corner(UL).set_opacity(0.85)

        # === CONFIG ===
        width = 2.5
        gate_gap = 0.4
        qubit_spacing = 1.2
        wire_length = width * 2
        x_start = 0
        x_end = x_start + wire_length

        y_q0 = qubit_spacing / 2
        y_q1 = -qubit_spacing / 2

        q0_label = Tex("$q_0$")
        q1_label = Tex("$q_1$")
        q0_label.next_to([x_start - 0.4, y_q0, 0], LEFT)
        q1_label.next_to([x_start - 0.4, y_q1, 0], LEFT)

        time_axis = Line([x_start, -1.8, 0], [x_end, -1.8, 0], color=YELLOW)
        time_label = Tex("t").next_to(time_axis, DOWN)

        t1_mid = x_start + width / 2
        line_q0_1a = Line([x_start, y_q0, 0], [t1_mid - gate_gap, y_q0, 0])
        line_q0_1b = Line([t1_mid + gate_gap, y_q0, 0], [x_start + width, y_q0, 0])
        line_q1_1 = Line([x_start, y_q1, 0], [x_start + width, y_q1, 0])

        h_gate = Square(0.6).move_to([t1_mid, y_q0, 0])
        h_label = Tex("H").scale(1.2).move_to(h_gate)
        h_group = VGroup(h_gate, h_label)

        t2_mid = x_start + width + width / 2
        line_q0_2a = Line([x_start + width, y_q0, 0], [t2_mid - gate_gap, y_q0, 0])
        line_q0_2b = Line([t2_mid + gate_gap, y_q0, 0], [x_end, y_q0, 0])
        line_q1_2a = Line([x_start + width, y_q1, 0], [t2_mid - gate_gap, y_q1, 0])
        line_q1_2b = Line([t2_mid + gate_gap, y_q1, 0], [x_end, y_q1, 0])

        ctrl_dot = Dot(radius=0.07).move_to([t2_mid, y_q0, 0])
        tgt_circle = Circle(radius=0.15).move_to([t2_mid, y_q1, 0])
        vert_line = Line(ctrl_dot.get_center(), tgt_circle.get_center())
        cx_group = VGroup(ctrl_dot, tgt_circle, vert_line)

        self.clear()
        self.play(FadeIn(caption))

        h_circuit = VGroup(
            q0_label.copy(), q1_label.copy(),
            line_q0_1a.copy(), h_group.copy(), line_q0_1b.copy(),
            line_q1_1.copy(),
            time_axis.copy(), time_label.copy()
        )
        h_circuit.scale(0.55).to_edge(LEFT).shift(LEFT * 0.5)

        h_step_label = Tex(r"Apply $H \otimes I$ on $\ket{00}$:", font_size=34, tex_template=tex_template)
        h_mult = Tex(r"""$
        (H \otimes I)\ket{00} =
        \frac{1}{\sqrt{2}}(\ket{00} + \ket{10})
        $""", font_size=32, tex_template=tex_template)
        h_vector = VGroup(h_step_label, h_mult).arrange(DOWN, buff=0.4).scale(0.9).move_to(ORIGIN)

        self.play(FadeIn(h_circuit), FadeIn(h_vector))
        self.wait(3)

        self.clear()
        caption = Text("Bloch Sphere after H gate", font_size=28).to_corner(UL).set_opacity(0.85)
        self.play(FadeIn(caption))
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        red_qubit = self.get_bloch_sphere(sphere_color=YELLOW, state_vector_endpoint=[1, 0, 0]).scale(0.45).shift(RIGHT * 2.5)
        blue_qubit = self.get_bloch_sphere(sphere_color=YELLOW, state_vector_endpoint=[0, 1, 0]).scale(0.45).shift(RIGHT * 4.5)
        bloch_view_h = VGroup(red_qubit, blue_qubit)
        self.play(FadeIn(bloch_view_h))
        self.wait(3)
        self.clear()

        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        caption = Text("Apply CNOT gate", font_size=28).to_corner(UL).set_opacity(0.85)
        self.play(FadeIn(caption))

        full_circuit = VGroup(
            q0_label.copy(), q1_label.copy(),
            line_q0_1a.copy(), h_group.copy(), line_q0_1b.copy(),
            line_q1_1.copy(),
            line_q0_2a.copy(), cx_group.copy(), line_q0_2b.copy(),
            line_q1_2a.copy(), line_q1_2b.copy(),
            time_axis.copy(), time_label.copy()
        )
        full_circuit.scale(0.55).to_edge(LEFT).shift(LEFT * 0.5)

        cnot_label = Tex(r"Apply CNOT:", font_size=34)
        cnot_mult = Tex(r"""$
        \text{CNOT}\left(\frac{1}{\sqrt{2}} \begin{bmatrix}1 \\ 0 \\ 1 \\ 0\end{bmatrix}\right)
        =
        \frac{1}{\sqrt{2}} \begin{bmatrix}1 \\ 0 \\ 0 \\ 1\end{bmatrix}
        = \frac{1}{\sqrt{2}}(\ket{00} + \ket{11})
        $""", font_size=30, tex_template=tex_template)
        final_state = Tex(r"Final EPR State: $\ket{\Phi^+} = \frac{1}{\sqrt{2}}(\ket{00} + \ket{11})$", font_size=34, color=YELLOW, tex_template=tex_template)
        vector_view = VGroup(cnot_label, cnot_mult, final_state).arrange(DOWN, buff=0.4).scale(0.9).move_to(ORIGIN)

        self.play(FadeIn(full_circuit), FadeIn(vector_view))
        self.wait(4)
        self.play(Indicate(final_state))
        self.wait(2)

        self.clear()
        caption = Text("Bloch Sphere of EPR pair", font_size=28).to_corner(UL).set_opacity(0.85)
        self.play(FadeIn(caption))
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        qubit1 = self.get_bloch_sphere(sphere_color=YELLOW, state_vector_endpoint=[1, 0, 0]).scale(0.45).shift(RIGHT * 2.5)
        qubit2 = self.get_bloch_sphere(sphere_color=YELLOW, state_vector_endpoint=[0, 1, 0]).scale(0.45).shift(RIGHT * 4.5)
        bloch_view = VGroup(qubit1, qubit2)
        self.play(FadeIn(bloch_view))
        self.wait(3)

        self.clear()
        self.move_camera(
            phi=original_phi,
            theta=original_theta,
            gamma=original_gamma,
            focal_distance=original_focal_distance,
            run_time=2
        )

        caption = Text("The qubits are now maximally entangled.", font_size=28).to_corner(UL).set_opacity(0.85)
        self.play(FadeIn(caption))
        self.wait(2)
        self.clear()
