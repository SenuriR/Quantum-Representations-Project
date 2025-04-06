# this is going to end up being the main driver code for the program
from manim import *
from qiskit import QuantumCircuit
import numpy as np
    
class Circuit(Scene):
    def __init__(self, qc=None, **kwargs):
        super().__init__(**kwargs)
        if qc is None:
            qc = QuantumCircuit(3, 3)
            qc.h(0)
            qc.cx(0, 1)
            qc.cx(1, 2)
            qc.measure([0, 1, 2], [0, 1, 2])
        self.qc = qc
        self.num_qubits = qc.num_qubits
        self.num_clbits = qc.num_clbits

        self.gates_dict = {
            "id": MathTex(r"I = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}"),  # Identity Gate
            "x": MathTex(r"X = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}"),  # Pauli-X Gate
            "y": MathTex(r"Y = \begin{bmatrix} 0 & -i \\ i & 0 \end{bmatrix}"),  # Pauli-Y Gate
            "z": MathTex(r"Z = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}"),  # Pauli-Z Gate
            "h": MathTex(r"H = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}"),  # Hadamard Gate
            "cx": MathTex(r"\text{CNOT} = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{bmatrix}")  # CNOT Gate
        }

    def construct(self):
        print(self.qc.draw(output='text'))  # Debug print

        circuit_shift = UP * 1.5
        width = 1.0  # consistent width for each segment
        total_timesteps = len(self.qc.data)
        
        # Time axis
        t_axis = Line(LEFT * 6, RIGHT * 6, color=YELLOW).to_edge(DOWN, buff=1)
        t_label = Tex("t").next_to(t_axis, DOWN)
        self.play(Create(t_axis), Write(t_label))
        self.wait(1)

        # Qubit & classical labels
        qubit_labels = VGroup(*[Tex(f"$q_{i}$").to_edge(LEFT).shift(DOWN * i + circuit_shift) for i in range(self.num_qubits)])
        classical_label = Tex("$c$").to_edge(LEFT).shift(DOWN * self.num_qubits + circuit_shift)
        self.play(Write(qubit_labels), Write(classical_label))
        self.wait(1)

        # Store per-qubit line segments
        qubit_line_segments = [[] for _ in range(self.num_qubits)]
        classical_segments = []

        # For each time step
        for t in range(total_timesteps):
            x_pos = LEFT * 6 + RIGHT * (t * width + width / 2)  # center of segment

            instruction = self.qc.data[t]
            gate, qubits, clbits = instruction.operation, instruction.qubits, instruction.clbits
            q_indices = [self.qc.find_bit(q).index for q in qubits]
            c_indices = [self.qc.find_bit(c).index for c in clbits] if clbits else []

            gate_group = None

            # Prepare gate visuals
            if gate.name in ["cx", "ccx"]:
                ctrl_dot = Dot().move_to(np.array([x_pos[0], qubit_labels[q_indices[0]].get_center()[1], 0]))
                tgt_circle = Circle().scale(0.3).move_to(np.array([x_pos[0], qubit_labels[q_indices[1]].get_center()[1], 0]))
                ctrl_line = Line(ctrl_dot.get_center(), tgt_circle.get_center())
                gate_group = VGroup(ctrl_dot, tgt_circle, ctrl_line)

            elif gate.name == "measure":
                y_q = qubit_labels[q_indices[0]].get_center()[1]
                y_c = classical_label.get_center()[1]
                measure_box = Square().scale(0.5).move_to(np.array([x_pos[0], y_q, 0]))
                measure_label = Tex(r"\textbf{M}").scale(0.7).move_to(measure_box)
                arrow = Arrow(measure_box.get_bottom(), measure_box.get_bottom() + DOWN * 0.5, buff=0.1, color=WHITE, stroke_width=2)
                collapse_line = Line(measure_box.get_bottom(), np.array([x_pos[0], y_c, 0]), color=WHITE, stroke_width=2)
                gate_group = VGroup(measure_box, measure_label, arrow, collapse_line)

            elif gate.num_qubits == 1:
                y_q = qubit_labels[q_indices[0]].get_center()[1]
                gate_box = Square().scale(0.5).move_to(np.array([x_pos[0], y_q, 0]))
                gate_label = Tex(gate.name.upper()).move_to(gate_box)
                gate_group = VGroup(gate_box, gate_label)

            if gate_group:
                self.play(FadeIn(gate_group), run_time=0.5)

            # For each qubit, draw segment
            for q in range(self.num_qubits):
                y = qubit_labels[q].get_center()[1]
                segment_start = x_pos[0] - width / 2
                segment_end = x_pos[0] + width / 2

                if q in q_indices:
                    # split into two small segments before/after gate
                    left = Line([segment_start, y, 0], [x_pos[0] - 0.2, y, 0], color=WHITE)
                    right = Line([x_pos[0] + 0.2, y, 0], [segment_end, y, 0], color=WHITE)
                    self.play(Create(left), Create(right), run_time=0.2)
                    qubit_line_segments[q].extend([left, right])
                else:
                    segment = Line([segment_start, y, 0], [segment_end, y, 0], color=WHITE)
                    self.play(Create(segment), run_time=0.2)
                    qubit_line_segments[q].append(segment)

            # For classical bit line
            if self.num_clbits > 0:
                y = classical_label.get_center()[1]
                segment = DashedLine(
                    [x_pos[0] - width / 2, y, 0],
                    [x_pos[0] + width / 2, y, 0],
                    color=GRAY
                )
                self.play(Create(segment), run_time=0.2)
                classical_segments.append(segment)

            # Update time label
            new_time_label = Tex(f"t={t + 1}").to_edge(UP)
            self.play(Transform(t_label, new_time_label), run_time=0.3)

        self.wait(2)
        self.play(FadeOut(*qubit_labels, classical_label, t_axis, t_label, *[seg for row in qubit_line_segments for seg in row], *classical_segments))
        self.wait(1)


if __name__ == "__main__":
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.measure([0, 1, 2], [0, 1, 2])
    
    scene = Circuit(qc)
    scene.render()
