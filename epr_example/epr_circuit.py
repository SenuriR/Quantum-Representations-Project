from manim import *

class EPRCircuit(Scene):
    def construct(self):
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

        self.play(Create(line_q0_1a), Create(line_q1_1))
        self.play(FadeIn(h_group))
        self.play(Create(line_q0_1b))

        self.play(Create(line_q0_2a), Create(line_q1_2a))
        self.play(FadeIn(cx_group))
        self.play(Create(line_q0_2b), Create(line_q1_2b))

        self.wait(2)
