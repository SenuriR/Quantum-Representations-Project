from manim import *
from qiskit import QuantumCircuit
from qiskit.visualization import circuit_drawer
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
        self.qc = qc
        self.num_qubits = qc.num_qubits
        self.num_clbits = qc.num_clbits

    def construct(self):
        print(self.qc.draw(output='text'))  # Print circuit to terminal for debugging
        
        # Convert the circuit to an image
        circuit_img = circuit_drawer(self.qc, output='mpl')
        circuit_img.savefig("quantum_circuit.png")
        
        # Load and display the quantum circuit image in Manim
        circuit_diagram = ImageMobject("quantum_circuit.png")
        circuit_diagram.scale(0.8)
        circuit_diagram.to_edge(DOWN).shift(UP * 0.5)
        self.play(FadeIn(circuit_diagram))
        self.wait(2)
        
        # Create qubit and classical bit lines dynamically
        qubit_lines = VGroup(*[
            Line(LEFT * 4, RIGHT * 4) for _ in range(self.num_qubits)
        ]).arrange(DOWN, buff=1)
        classical_lines = DashedLine(LEFT * 4, RIGHT * 4, color=GRAY).move_to(qubit_lines[-1].get_center() + DOWN * 1.5).arrange(DOWN, buff=1).next_to(qubit_lines, DOWN, buff=0.5)
        
        all_lines = VGroup(qubit_lines, classical_lines).scale(0.8).move_to(ORIGIN)
        self.play(Create(all_lines))
        
        # Add qubit and classical labels
        qubit_labels = VGroup(*[
            Tex(f"$q_{i}$").next_to(qubit_lines[i], LEFT) for i in range(self.num_qubits)
        ])
        classical_labels = VGroup(*[
            Tex(f"$c_{i}$").next_to(classical_lines[i], LEFT) for i in range(self.num_clbits)
        ])
        
        all_labels = VGroup(qubit_labels, classical_labels).scale(0.8)
        self.play(Write(all_labels))
        self.wait(1)
        
        # Process circuit operations and place them dynamically
        operations = []
        x_offset = -3  # Initial position of gates
        for instruction in self.qc.data:
            gate, qubits, clbits = instruction.operation, instruction.qubits, instruction.clbits
            q_indices = [self.qc.find_bit(q).index for q in qubits]
            c_indices = [self.qc.find_bit(c).index for c in clbits]
            
            # Create gate box
            gate_box = Square().scale(0.5).move_to(qubit_lines[q_indices[0]].get_center() + RIGHT * x_offset)
            gate_label = Tex(gate.name.upper()).move_to(gate_box)
            gate_group = VGroup(gate_box, gate_label)
            
            # Handle controlled gates (e.g., CNOT)
            if gate.name == "cx":
                ctrl_dot = Dot().move_to(qubit_lines[q_indices[0]].get_center() + RIGHT * x_offset)
                target_circle = Circle().scale(0.3).move_to(qubit_lines[q_indices[1]].get_center() + RIGHT * x_offset)
                ctrl_line = Line(ctrl_dot.get_center(), target_circle.get_center())
                gate_group = VGroup(ctrl_dot, target_circle, ctrl_line)
            
            # Handle measurements
            if gate.name == "measure":
                measure_box = Square().scale(0.5).move_to(qubit_lines[q_indices[0]].get_right() + RIGHT * 0.5)
                measure_label = Tex("M").move_to(measure_box)
                arrow = Arrow(measure_box.get_bottom(), classical_lines.get_center(), buff=0.1, color=WHITE, stroke_width=2)
                gate_group = VGroup(measure_box, measure_label, arrow)
            
            gate_group.scale(0.8)
            operations.append(gate_group)
            x_offset += 1.5  # Shift for next gate
        
        self.play(*[FadeIn(op) for op in operations])
        self.wait(2)
        
        # Fade out everything
        self.play(FadeOut(circuit_diagram, all_lines, all_labels, *operations))
        self.wait(1)

if __name__ == "__main__":
    from manim import config
    config.output_file = "quantum_circuit"
