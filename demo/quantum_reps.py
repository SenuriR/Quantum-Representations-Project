from manim import *
from qiskit import QuantumCircuit
import numpy as np

class QuantumGateMatrices(Scene):
    def construct(self):
        title = Title("Matrix Representations of Common Quantum Gates")
        self.play(Write(title))
        self.wait(1)
        
        gates = [
            ("Identity Gate (I)", MathTex(r"I = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}")),
            ("Pauli-X Gate (X)", MathTex(r"X = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}")),
            ("Pauli-Y Gate (Y)", MathTex(r"Y = \begin{bmatrix} 0 & -	i \\ 	i & 0 \end{bmatrix}")),
            ("Pauli-Z Gate (Z)", MathTex(r"Z = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}")),
            ("Hadamard Gate (H)", MathTex(r"H = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}")),
            ("CNOT Gate", MathTex(r"\text{CNOT} = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{bmatrix}"))
        ]
        
        for gate_name, matrix_tex in gates:
            gate_label = Tex(gate_name).scale(1.2)
            group = VGroup(gate_label, matrix_tex).arrange(DOWN, buff=0.5)
            
            self.play(Write(gate_label))
            self.wait(1)
            self.play(FadeIn(matrix_tex))
            self.wait(2)
            self.play(FadeOut(group))
            
        self.play(FadeOut(title))
        self.wait(1)

class QuantumCircuitVisualization(Scene):
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

    def construct(self):
        print(self.qc.draw(output='text'))  # Print circuit for debugging

        # Shift entire circuit up to avoid overlap with time axis
        circuit_shift = UP * 1.5

        # Properly position the time axis (t-axis) at the bottom
        t_axis = Line(LEFT * 6, RIGHT * 6, color=YELLOW).to_edge(DOWN, buff=1)
        t_label = Tex("t").next_to(t_axis, DOWN)
        self.play(Create(t_axis), Write(t_label))
        self.wait(1)

        # Initialize qubit labels on the left side
        qubit_labels = VGroup(*[Tex(f"$q_{i}$").to_edge(LEFT).shift(DOWN * i + circuit_shift) for i in range(self.num_qubits)])
        classical_label = Tex("$c$").to_edge(LEFT).shift(DOWN * self.num_qubits + circuit_shift)
        self.play(Write(qubit_labels), Write(classical_label))
        self.wait(1)

        # Initialize lines for qubits and classical bit
        qubit_lines = [Line(LEFT * 6, LEFT * 6, color=WHITE).shift(DOWN * i + circuit_shift) for i in range(self.num_qubits)]
        classical_line = DashedLine(LEFT * 6, LEFT * 6, color=GRAY).shift(DOWN * self.num_qubits + circuit_shift)
        all_lines = VGroup(*qubit_lines, classical_line)
        self.add(all_lines)

        # Initialize time label at the top
        time_label = Tex("t=0").to_edge(UP)
        self.add(time_label)

        # Iterate through time t, growing circuit from the left to the right
        for t in range(len(self.qc.data)):
            instruction = self.qc.data[t]
            gate, qubits, clbits = instruction.operation, instruction.qubits, instruction.clbits
            q_indices = [self.qc.find_bit(q).index for q in qubits]
            c_indices = [self.qc.find_bit(c).index for c in clbits] if clbits else []
            
            # Extend lines up to current time t, ensuring simultaneous growth
            new_end = LEFT * 6 + RIGHT * (t + 1.5)
            transformations = []
            for q_index in range(self.num_qubits):
                transformations.append(Transform(qubit_lines[q_index], Line(LEFT * 6, new_end, color=WHITE).shift(DOWN * q_index + circuit_shift)))
            if self.num_clbits > 0:
                transformations.append(Transform(classical_line, DashedLine(LEFT * 6, new_end, color=GRAY).shift(DOWN * self.num_clbits + circuit_shift)))
            self.play(AnimationGroup(*transformations, lag_ratio=0), run_time=0.5)
            
            gate_group = None
            
            # Controlled gates (CX, CCX, etc.)
            if gate.name in ["cx", "ccx"]:
                ctrl_dot = Dot().move_to(qubit_lines[q_indices[0]].get_end())
                target_circle = Circle().scale(0.3).move_to(qubit_lines[q_indices[1]].get_end())
                ctrl_line = Line(ctrl_dot.get_center(), target_circle.get_center())
                gate_group = VGroup(ctrl_dot, target_circle, ctrl_line)
            
            # Measurement operations
            elif gate.name in ["measure"]:
                measure_box = Square().scale(0.5).move_to(qubit_lines[q_indices[0]].get_end())
                measure_label = Tex(r"\textbf{M}").scale(0.7).move_to(measure_box)
                arrow = Arrow(measure_box.get_bottom(), measure_box.get_bottom() + DOWN * 0.5, buff=0.1, color=WHITE, stroke_width=2)
                collapse_line = Line(
                    measure_box.get_bottom(), 
                    np.array([measure_box.get_bottom()[0], classical_line.get_top()[1], 0]),
                    color=WHITE, stroke_width=2
                )
                gate_group = VGroup(measure_box, measure_label, arrow, collapse_line)
            
            # Single-qubit gates
            elif gate.num_qubits == 1:
                gate_box = Square().scale(0.5).move_to(qubit_lines[q_indices[0]].get_end())
                gate_label = Tex(gate.name.upper()).move_to(gate_box)
                gate_group = VGroup(gate_box, gate_label)
            
            if gate_group:
                self.play(FadeIn(gate_group), run_time=0.5)
                self.wait(0.5)
            
            # Update time label at the top instead of multiple markers
            new_time_label = Tex(f"t={t + 1}").to_edge(UP)
            self.play(Transform(time_label, new_time_label), run_time=0.5)
            
        self.wait(2)
        # Fade out everything
        self.play(FadeOut(all_lines, qubit_labels, classical_label, t_axis, t_label, time_label))
        self.wait(1)

if __name__ == "__main__":
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.measure([0, 1, 2], [0, 1, 2])
    
    scene = QuantumCircuitVisualization(qc)
    scene.render()
