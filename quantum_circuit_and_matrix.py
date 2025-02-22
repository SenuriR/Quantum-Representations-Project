from manim import *
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
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
        print(self.qc.draw(output='text'))  # Print circuit to terminal for debugging

        # Initialize quantum and classical lines
        qubit_lines = VGroup(*[Line(LEFT * 4, RIGHT * 4) for _ in range(self.num_qubits)]).arrange(DOWN, buff=1)
        classical_line = DashedLine(LEFT * 4, RIGHT * 4, color=GRAY).next_to(qubit_lines, DOWN, buff=1)
        all_lines = VGroup(qubit_lines, classical_line)
        self.play(Create(all_lines))

        # Add qubit labels
        qubit_labels = VGroup(*[Tex(f"$q_{i}$").next_to(qubit_lines[i], LEFT) for i in range(self.num_qubits)])
        classical_label = Tex("$c$").next_to(classical_line, LEFT)
        all_labels = VGroup(qubit_labels, classical_label)
        self.play(Write(all_labels))
        self.wait(1)

class QuantumCircuitAndMatrix(Scene):
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
        # Run Quantum Circuit Visualization
        circuit_scene = QuantumCircuitVisualization(self.qc)
        circuit_scene.construct()
        self.wait(2)

        # Move to the Matrix Representation
        self.clear()
        title = Tex("Matrix Representation of Quantum Circuit").to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Remove measurements before computing the unitary matrix
        qc_no_measure = QuantumCircuit(self.qc.num_qubits)
        for instr, qargs, cargs in self.qc.data:
            if instr.name != "measure":
                qc_no_measure.append(instr, qargs)
        unitary = Operator(qc_no_measure).data  # Compute unitary of modified circuit

        # Convert unitary matrix to a Manim Matrix object
        matrix_obj = Matrix(np.round(unitary, 2))
        matrix_obj.scale(0.7).next_to(title, DOWN, buff=1)
        
        self.play(Write(matrix_obj))
        self.wait(2)

        self.play(FadeOut(matrix_obj, title))
        self.wait(1)

if __name__ == "__main__":
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.measure([0, 1, 2], [0, 1, 2])
    
    scene = QuantumCircuitAndMatrix(qc)
    scene.render()
