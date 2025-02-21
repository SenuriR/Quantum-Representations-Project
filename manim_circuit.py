from manim import *
from qiskit import QuantumCircuit
import numpy as np

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

        # Initialize quantum and classical lines
        qubit_lines = VGroup(*[Line(LEFT * 4, RIGHT * 4) for _ in range(self.num_qubits)]).arrange(DOWN, buff=1)
        classical_line = DashedLine(LEFT * 4, RIGHT * 4, color=GRAY).next_to(qubit_lines, DOWN, buff=1)
        all_lines = VGroup(qubit_lines, classical_line)
        self.play(Create(all_lines))

        # Time axis (t-axis) moved below the diagram
        t_axis = Line(LEFT * 4, RIGHT * 4, color=YELLOW).next_to(classical_line, DOWN, buff=1.5)
        t_label = Tex("t").next_to(t_axis, DOWN)
        self.play(Create(t_axis), Write(t_label))
        self.wait(1)

        # Add qubit labels
        qubit_labels = VGroup(*[Tex(f"$q_{i}$").next_to(qubit_lines[i], LEFT) for i in range(self.num_qubits)])
        classical_label = Tex("$c$").next_to(classical_line, LEFT)
        all_labels = VGroup(qubit_labels, classical_label)
        self.play(Write(all_labels))
        self.wait(1)

        # Process the circuit step by step
        x_offset = -3  # Initial x position of gates
        t_position = -3  # Initial time position on t-axis

        for instruction in self.qc.data:
            gate, qubits, clbits = instruction.operation, instruction.qubits, instruction.clbits
            q_indices = [self.qc.find_bit(q).index for q in qubits]
            c_indices = [self.qc.find_bit(c).index for c in clbits] if clbits else []
            
            gate_group = None
            
            # Controlled gates (CX, CCX, etc.)
            if gate.name in ["cx", "ccx"]:
                ctrl_dot = Dot().move_to(qubit_lines[q_indices[0]].get_center() + RIGHT * x_offset)
                target_circle = Circle().scale(0.3).move_to(qubit_lines[q_indices[1]].get_center() + RIGHT * x_offset)
                ctrl_line = Line(ctrl_dot.get_center(), target_circle.get_center())
                gate_group = VGroup(ctrl_dot, target_circle, ctrl_line)
            
            # Measurement operations
            elif gate.name in ["measure"]:
                measure_box = Square().scale(0.5).move_to(qubit_lines[q_indices[0]].get_center() + RIGHT * x_offset)
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
                gate_box = Square().scale(0.5).move_to(qubit_lines[q_indices[0]].get_center() + RIGHT * x_offset)
                gate_label = Tex(gate.name.upper()).move_to(gate_box)
                gate_group = VGroup(gate_box, gate_label)
            
            if gate_group:
                self.play(FadeIn(gate_group))
                x_offset += 1.5  # Move to the right for next gate
                
                # Animate time axis increment
                t_marker = Tex(f"t={t_position}").next_to(t_axis, UP).shift(RIGHT * t_position)
                self.play(Write(t_marker))
                t_position += 1.5
                self.wait(0.5)
        
        self.wait(2)
        # Fade out everything
        self.play(FadeOut(all_lines, all_labels, t_axis, t_label))
        self.wait(1)

if __name__ == "__main__":
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.measure([0, 1, 2], [0, 1, 2])
    
    scene = QuantumCircuitVisualization(qc)
    scene.render()

'''
No lines through the boxes (e.g., H gate, M gate, etc.)
Line should not extend past the measurement box (remember the line represent the qubit, when we measure the qubit, we are “destroying” it)    
Should be a plus sign inside the circle (just extend to other end of circle)
Experiment with colors 
'''