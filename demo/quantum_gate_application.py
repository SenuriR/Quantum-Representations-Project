from manim import *
import numpy as np

class QuantumGateApplication(Scene):
    def construct(self):
        # Example Hadamard gate applied to |000⟩ state
        initial_state = [1, 0, 0, 0, 0, 0, 0, 0]  # |000⟩ state
        hadamard_3 = np.array([[1, 1, 1, 1, 1, 1, 1, 1],
                                [1, -1, 1, -1, 1, -1, 1, -1],
                                [1, 1, -1, -1, 1, 1, -1, -1],
                                [1, -1, -1, 1, 1, -1, -1, 1],
                                [1, 1, 1, 1, -1, -1, -1, -1],
                                [1, -1, 1, -1, -1, 1, -1, 1],
                                [1, 1, -1, -1, -1, -1, 1, 1],
                                [1, -1, -1, 1, -1, 1, 1, -1]]) / np.sqrt(8)

        gate_name = "Hadamard"
        num_qubits = 3

        # Title
        title = Tex(f"Application of {gate_name} Gate").scale(0.8).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Initial Quantum State
        initial_state_matrix = Matrix([[str(val)] for val in initial_state]).scale(0.7)
        ket_notation = "000"  # since initial state is |000⟩
        state_label = Tex(rf"Initial State: $|{ket_notation}\rangle$")

        self.play(Write(state_label), Write(initial_state_matrix))
        self.wait(2)
        self.play(FadeOut(state_label))

        # Quantum Gate Matrix
        gate_matrix_mobject = Matrix([[str(round(val, 2)) for val in row] for row in hadamard_3]).scale(0.5)
        gate_label = Tex(f"{gate_name} Gate").scale(0.8).next_to(gate_matrix_mobject, UP, buff=0.3)
        scalar = Tex(rf"$\frac{{1}}{{\sqrt{{{len(initial_state)}}}}}$").scale(0.8).next_to(gate_matrix_mobject, LEFT, buff=0.3)

        self.wait(2)
        self.play(FadeOut(gate_label))

        # Arrange multiplication layout
        initial_state_matrix.next_to(gate_matrix_mobject, RIGHT, buff=0.3)
        self.play(Write(scalar), Write(gate_matrix_mobject))
        self.play(Write(initial_state_matrix))
        self.wait(2)

        # Compute final state
        final_state_vector = np.dot(hadamard_3, np.array(initial_state).reshape(-1, 1))
        final_state_matrix = Matrix([[str(round(val[0], 2))] for val in final_state_vector]).scale(0.7)
        final_label = Tex("Final State: After Gate Application").scale(0.8).next_to(final_state_matrix, UP, buff=0.3)

        # Transition: Initial state → Gate Application → Final state
        self.play(Transform(initial_state_matrix, final_state_matrix))
        self.wait(2)
        self.play(FadeOut(gate_matrix_mobject), FadeOut(scalar))

        # Cleanup
        self.play(FadeOut(final_label), FadeOut(final_state_matrix))
        self.wait(1)
