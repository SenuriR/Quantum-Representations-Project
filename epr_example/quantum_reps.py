from manim import *
from two_bloch import TwoQubitColoredBlochSpheres
from circuit import Circuit
from entangled_qubits import TwoEntangledQubits
from vector import EPRPairMatrixWalkthrough

class QuantumReps(ThreeDScene):
    def get_bloch_sphere(self, sphere_color=BLUE, state_vector_endpoint=[0, 0, 1.5]):
        # Ensure correct type for vector arithmetic
        state_vector_endpoint = np.array(state_vector_endpoint, dtype=float)

        # Bloch Sphere
        bloch_sphere = Sphere(radius=1)
        bloch_sphere.set_fill(color=sphere_color, opacity=0.5)
        bloch_sphere.set_stroke(color=sphere_color, opacity=0.6)

        # Axes
        x_axis = Arrow3D(start=[-1.5, 0, 0], end=[1.5, 0, 0], color=WHITE)
        y_axis = Arrow3D(start=[0, -1.5, 0], end=[0, 1.5, 0], color=WHITE)
        z_axis = Arrow3D(start=[0, 0, -1.5], end=[0, 0, 1.5], color=WHITE)

        # State vector
        state_vector_arrow = Arrow3D(start=[0, 0, 0], end=state_vector_endpoint, color=RED)

        # Helper for state labels
        def state_label(tex_str, pos):
            return Tex(tex_str, color=WHITE).move_to(pos).rotate(PI / 2, axis=RIGHT).rotate(PI - PI / 6, axis=OUT)

        # Labels
        ket_0 = state_label(r"$\left|0\right\rangle$", z_axis.get_end() + 0.3 * OUT)
        ket_1 = state_label(r"$\left|1\right\rangle$", z_axis.get_start() + 0.3 * IN)
        ket_plus = state_label(r"$\left|+\right\rangle$", x_axis.get_end() + 0.3 * RIGHT)
        ket_minus = state_label(r"$\left|-\right\rangle$", x_axis.get_start() + 0.3 * LEFT)
        ket_plus_i = state_label(r"$\left|+i\right\rangle$", y_axis.get_end() + 0.3 * UP)
        ket_minus_i = state_label(r"$\left|-i\right\rangle$", y_axis.get_start() + 0.3 * DOWN)

        # Grouping
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

        # scene 1
        text = Text("EPR Pair Example")
        self.play(FadeIn(text))
        self.wait(2)
        self.play(FadeOut(text))

        text = Text("Start with two qubits")
        self.play(FadeIn(text))
        self.wait(2)
        self.play(FadeOut(text))

        text = Text("Circuit View")
        text.move_to(UP)
        self.play(FadeIn(text))
        self.wait(2)
        self.play(FadeOut(text))

        # intialize all circuit elements
        # === CONFIG ===
        width = 2.5       # spacing per timestep (wider for better visuals)
        gate_gap = 0.4
        qubit_spacing = 1.2
        wire_length = width * 2
        x_start = 0
        x_end = x_start + wire_length

        # === Y POSITIONS ===
        y_q0 = qubit_spacing / 2
        y_q1 = -qubit_spacing / 2

        # === QUBIT LABELS ===
        q0_label = Tex("$q_0$")
        q1_label = Tex("$q_1$")
        q0_label.next_to([x_start - 0.4, y_q0, 0], LEFT)
        q1_label.next_to([x_start - 0.4, y_q1, 0], LEFT)

        # === TIME AXIS ===
        time_axis = Line([x_start, -1.8, 0], [x_end, -1.8, 0], color=YELLOW)
        time_label = Tex("t").next_to(time_axis, DOWN)

        # === TIME STEP 1: Hadamard on q_0 ===
        t1_mid = x_start + width / 2
        line_q0_1a = Line([x_start, y_q0, 0], [t1_mid - gate_gap, y_q0, 0])
        line_q0_1b = Line([t1_mid + gate_gap, y_q0, 0], [x_start + width, y_q0, 0])
        line_q1_1 = Line([x_start, y_q1, 0], [x_start + width, y_q1, 0])

        h_gate = Square(0.6).move_to([t1_mid, y_q0, 0])
        h_label = Tex("H").scale(1.2).move_to(h_gate)
        h_group = VGroup(h_gate, h_label)

        # === TIME STEP 2: CNOT ===
        t2_mid = x_start + width + width / 2
        line_q0_2a = Line([x_start + width, y_q0, 0], [t2_mid - gate_gap, y_q0, 0])
        line_q0_2b = Line([t2_mid + gate_gap, y_q0, 0], [x_end, y_q0, 0])
        line_q1_2a = Line([x_start + width, y_q1, 0], [t2_mid - gate_gap, y_q1, 0])
        line_q1_2b = Line([t2_mid + gate_gap, y_q1, 0], [x_end, y_q1, 0])

        ctrl_dot = Dot(radius=0.07).move_to([t2_mid, y_q0, 0])
        tgt_circle = Circle(radius=0.15).move_to([t2_mid, y_q1, 0])
        vert_line = Line(ctrl_dot.get_center(), tgt_circle.get_center())
        cx_group = VGroup(ctrl_dot, tgt_circle, vert_line)

        # === BUILD FULL CIRCUIT GROUP ===
        circuit_elements = VGroup(
            q0_label, q1_label,
            line_q0_1a, h_group, line_q0_1b,
            line_q1_1,
            line_q0_2a, cx_group, line_q0_2b,
            line_q1_2a, line_q1_2b,
            time_axis, time_label
        )

        # === CENTER + SCALE ===
        circuit_elements.move_to(ORIGIN)  # center in screen
        circuit_elements.scale(1.2)       # scale up proportionally

        # === ANIMATION SEQUENCE ===
        self.play(Create(time_axis), Write(time_label))
        self.play(Write(q0_label), Write(q1_label))

        self.clear()

        text = Text("Vector View")
        text.move_to(UP)
        self.play(FadeIn(text))
        self.wait(2)
        self.play(FadeOut(text))

        ## Stage 1: Initial state
        initial_label = Tex(r"Initial State:", font_size=36)
        initial_ket = Tex(r"$\ket{00} = \begin{bmatrix}1 \\ 0 \\ 0 \\ 0\end{bmatrix}$", font_size=36, tex_template=tex_template)

        group1 = VGroup(initial_label, initial_ket).arrange(DOWN, center=True).move_to(ORIGIN)
        self.play(FadeIn(group1))
        self.wait(2)
        self.play(FadeOut(group1))

        self.clear()

        text = Text("Bloch Sphere View")
        text.move_to(UP)
        self.play(FadeIn(text))
        self.wait(2)
        self.play(FadeOut(text))

        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)

        red_qubit = self.get_bloch_sphere(
            sphere_color=YELLOW,
            state_vector_endpoint=[1, 0, 0]
        ).shift(RIGHT * 3 + DOWN * 0.5 + IN * 1.5)

        blue_qubit = self.get_bloch_sphere(
            sphere_color=YELLOW,
            state_vector_endpoint=[0, 1, 0]
        ).shift(LEFT * 3 + UP * 0.2 + OUT * 0.5)

        # Group both Bloch spheres and scale to fit frame
        both_spheres = VGroup(red_qubit, blue_qubit)
        both_spheres.scale(0.6)  # Adjust this value as needed
        self.add(both_spheres)

        self.wait(3)

        self.clear()
        self.move_camera(
            phi=original_phi,
            theta=original_theta,
            gamma=original_gamma,
            focal_distance=original_focal_distance,
            run_time=2  # or however long you want the animation to last
        )


        text = Text("Apply Hadamard gate to qubit 1")
        text.move_to(UP)
        self.play(FadeIn(text))
        self.wait(2)
        self.play(FadeOut(text))

        
        text = Text("Circuit View")
        text.move_to(UP)
        self.play(FadeIn(text))
        self.wait(2)
        self.play(FadeOut(text))

        self.play(Create(time_axis), Write(time_label))
        self.play(Write(q0_label), Write(q1_label))

        self.play(Create(line_q0_1a), Create(line_q1_1))
        self.play(FadeIn(h_group))
        self.play(Create(line_q0_1b))

        self.clear()

        text = Text("Vector View")
        text.move_to(UP)
        self.play(FadeIn(text))
        self.wait(2)
        self.play(FadeOut(text))

        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage{braket}")

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

        self.clear()

        text = Text("Bloch Sphere View")
        text.move_to(UP)
        self.play(FadeIn(text))
        self.wait(2)
        self.play(FadeOut(text))

        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)

        red_qubit = self.get_bloch_sphere(
            sphere_color=YELLOW,
            state_vector_endpoint=[1, 0, 0]
        ).shift(RIGHT * 3 + DOWN * 0.5 + IN * 1.5)

        blue_qubit = self.get_bloch_sphere(
            sphere_color=YELLOW,
            state_vector_endpoint=[0, 1, 0]
        ).shift(LEFT * 3 + UP * 0.2 + OUT * 0.5)

        # Group both Bloch spheres and scale to fit frame
        both_spheres = VGroup(red_qubit, blue_qubit)
        both_spheres.scale(0.6)  # Adjust this value as needed
        self.add(both_spheres)

        self.wait(3)

        self.clear()
        self.move_camera(
            phi=original_phi,
            theta=original_theta,
            gamma=original_gamma,
            focal_distance=original_focal_distance,
            run_time=2  # or however long you want the animation to last
        )

        text = Text("This puts qubit 1 into superposition")
        text.move_to(UP)
        self.play(FadeIn(text))
        self.wait(2)
        self.play(FadeOut(text))

        text = Text("Apply the CNOT gate")
        text.move_to(UP)
        self.play(FadeIn(text))
        self.wait(2)
        self.play(FadeOut(text))


        text = Text("Circuit View")
        text.move_to(UP)
        self.play(FadeIn(text))
        self.wait(2)
        self.play(FadeOut(text))

        # === ANIMATION SEQUENCE ===
        self.play(Create(time_axis), Write(time_label))
        self.play(Write(q0_label), Write(q1_label))

        self.play(Create(line_q0_1a), Create(line_q1_1))
        self.play(FadeIn(h_group))
        self.play(Create(line_q0_1b))

        self.play(Create(line_q0_2a), Create(line_q1_2a))
        self.play(FadeIn(cx_group))
        self.play(Create(line_q0_2b), Create(line_q1_2b))

        self.wait(2)

        self.clear()

        text = Text("Vector View")
        text.move_to(UP)
        self.play(FadeIn(text))
        self.wait(2)
        self.play(FadeOut(text))

        # Stage 3: Apply CNOT
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

        self.clear()

        text = Text("Bloch Sphere View")
        text.move_to(UP)
        self.play(FadeIn(text))
        self.wait(2)
        self.play(FadeOut(text))

        # Titles
        title = Text("Two Entangled Qubits", font_size=40).to_edge(UP)

        # Create two Bloch spheres using 3D spheres
        qubit1 = Sphere(radius=1, resolution=(24, 48)).shift(LEFT * 3)
        qubit2 = Sphere(radius=1, resolution=(24, 48)).shift(RIGHT * 3)

        qubit1.set_fill(RED, opacity=0.3).set_stroke(WHITE, opacity=0.6)
        qubit2.set_fill(BLUE, opacity=0.3).set_stroke(WHITE, opacity=0.6)

        label1 = Tex(r"$Q_1$").next_to(qubit1, DOWN)
        label2 = Tex(r"$Q_2$").next_to(qubit2, DOWN)

        # Arrows representing Bloch vectors
        vec1 = Arrow3D(start=qubit1.get_center(), end=qubit1.get_center() + OUT, color=YELLOW)
        vec2 = Arrow3D(start=qubit2.get_center(), end=qubit2.get_center() + OUT, color=YELLOW)

        # A line indicating entanglement between the two qubits
        entangled_line = DashedLine(qubit1.get_center(), qubit2.get_center(), color=PURPLE)

        # Optional: State label
        entangled_state = Tex(r"$|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$", font_size=36)
        entangled_state.next_to(entangled_line, DOWN, buff=1)

        self.add(title)
        self.play(FadeIn(qubit1, qubit2), FadeIn(label1, label2))
        self.play(Create(vec1), Create(vec2))
        self.play(Create(entangled_line), Write(entangled_state))
        self.wait(2)

        self.clear()

        text = Text("The qubits are now maximally entangled.")
        text.move_to(UP)
        self.play(FadeIn(text))
        self.wait(2)
        self.play(FadeOut(text))

        self.clear()