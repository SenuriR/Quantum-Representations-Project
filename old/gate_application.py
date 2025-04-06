from manim import *
import numpy as np
from old.gates_def import gate_definitions  # Import the predefined gates

class QuantumGateApplication(Scene):
    def __init__(self, gate_name="hadamard_3", **kwargs):
        super().__init__(**kwargs)
        if gate_name not in gate_definitions:
            raise ValueError(f"Gate '{gate_name}' not found in predefined gates!")
        self.gate_name = gate_name
        self.gate_matrix = gate_definitions[gate_name]

    def construct(self):
        num_qubits = int(np.log2(len(self.gate_matrix)))  # Determine number of qubits

        # Initial State |000⟩
        initial_state = np.zeros(2**num_qubits)
        initial_state[0] = 1  # |000...0⟩ state

        # Title
        title = Tex(f"Application of {self.gate_name.replace('_', ' ').upper()} Gate").scale(0.8).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Initial Quantum State
        ket_notation = "0" * num_qubits  # |000⟩ for n-qubits
        state_label = Tex(rf"Initial State: $|{ket_notation}\rangle$").scale(0.8)
        self.play(Write(state_label))
        self.wait(1)

        # Gate Matrix
        gate_matrix_mobject = Matrix([[str(round(val, 2)) for val in row] for row in self.gate_matrix]).scale(0.5)
        self.play(Write(gate_matrix_mobject))
        self.wait(2)

        # Apply Gate
        final_state = np.dot(self.gate_matrix, initial_state)
        final_state_matrix = Matrix([[str(round(val, 2))] for val in final_state]).scale(0.7)
        final_label = Tex("Final State After Gate Application").scale(0.8).next_to(final_state_matrix, UP, buff=0.3)

        # Transition
        self.play(Transform(state_label, final_label), Transform(gate_matrix_mobject, final_state_matrix))
        self.wait(2)
        self.play(FadeOut(final_label), FadeOut(final_state_matrix))

# To render the scene with a selected gate
if __name__ == "__main__":
    scene = QuantumGateApplication(gate_name="cnot_3")  # Change to any gate defined in quantum_gates.py
    scene.render()
