from manim import *
from qiskit import QuantumCircuit
from qiskit.visualization import circuit_drawer
import numpy as np

class QuantumCircuitVisualization(Scene):
    def construct(self):
        # Define a simple quantum circuit
        qc = QuantumCircuit(2, 2)  # 2 qubits, 2 classical bits
        qc.h(0)  # Apply Hadamard gate to qubit 0
        qc.cx(0, 1)  # Apply CNOT gate (entanglement)
        qc.measure([0, 1], [0, 1])  # Measure both qubits
        
        # Convert the circuit to an image
        circuit_img = circuit_drawer(qc, output='mpl')
        circuit_img.savefig("quantum_circuit.png")
        
        # Load and display the quantum circuit image in Manim
        circuit_diagram = ImageMobject("quantum_circuit.png")
        circuit_diagram.scale(1.2)
        circuit_diagram.to_edge(DOWN).shift(UP * 0.5)
        self.play(FadeIn(circuit_diagram))
        self.wait(2)
        
        # Create qubit lines
        qubit_lines = VGroup(
            Line(LEFT * 4, RIGHT * 4),
            Line(LEFT * 4, RIGHT * 4)
        ).arrange(DOWN, buff=1)
        self.play(Create(qubit_lines))
        
        # Add qubit labels
        qubit_labels = VGroup(
            Tex("$q_0$").next_to(qubit_lines[0], LEFT),
            Tex("$q_1$").next_to(qubit_lines[1], LEFT)
        )
        self.play(Write(qubit_labels))
        self.wait(1)
        
        # Hadamard gate animation
        hadamard = Square().scale(0.5).move_to(qubit_lines[0].get_center())
        h_label = Tex("H").move_to(hadamard)
        h_gate = VGroup(hadamard, h_label)
        self.play(FadeIn(h_gate))
        self.wait(1)
        
        # CNOT gate animation
        cnot_ctrl = Dot().move_to(qubit_lines[0].get_right() + LEFT * 2)
        cnot_target = Circle().scale(0.3).move_to(qubit_lines[1].get_right() + LEFT * 2)
        cnot_line = Line(cnot_ctrl.get_center(), cnot_target.get_center())
        cnot_gate = VGroup(cnot_ctrl, cnot_target, cnot_line)
        self.play(FadeIn(cnot_gate))
        self.wait(1)
        
        # Measurement animation
        measure_boxes = VGroup(
            Square().scale(0.5).move_to(qubit_lines[0].get_right()),
            Square().scale(0.5).move_to(qubit_lines[1].get_right())
        )
        measure_labels = VGroup(
            Tex("M").move_to(measure_boxes[0]),
            Tex("M").move_to(measure_boxes[1])
        )
        measurements = VGroup(measure_boxes, measure_labels)
        self.play(FadeIn(measurements))
        self.wait(2)
        
        # Fade out everything
        self.play(FadeOut(circuit_diagram, qubit_lines, qubit_labels, h_gate, cnot_gate, measurements))
        self.wait(1)

if __name__ == "__main__":
    scene = QuantumCircuitVisualization()
    scene.render()
