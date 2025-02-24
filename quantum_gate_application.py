from manim import *
import numpy as np

class QuantumGateApplication(Scene):
    def __init__(self, initial_state, gate_matrix, gate_name, **kwargs):
        super().__init__(**kwargs)
        self.initial_state = initial_state
        self.gate_matrix = gate_matrix
        self.gate_name = gate_name
        self.num_qubits = int(np.log2(len(initial_state)))

    def construct(self):
        title = Tex(f"Application of {self.gate_name} Gate").scale(0.8).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        
        # Display Initial Quantum State
        initial_state_matrix = Matrix([[str(val)] for val in self.initial_state]).scale(0.7)
        
        # Generate the ket notation for the state
        binary_state = bin(self.initial_state.index(1))[2:].zfill(self.num_qubits)
        ket_notation = ''.join(['0' if x == '0' else '1' for x in binary_state])
        
        # Create the state label with proper LaTeX formatting
        state_label = Tex(rf"Initial State: $\ket{{{ket_notation}}}$") \
            .scale(0.8) \
            .next_to(initial_state_matrix, UP, buff=0.3)
        
        self.play(Write(state_label), Write(initial_state_matrix))
        self.wait(2)
        self.play(FadeOut(state_label))
        
        # Display Quantum Gate Matrix
        gate_matrix_mobject = Matrix([[str(val) for val in row] for row in self.gate_matrix]).scale(0.5)
        gate_label = Tex(f"{self.gate_name} Gate").scale(0.8).next_to(gate_matrix_mobject, UP, buff=0.3)
        scalar = Tex(rf"$\frac{{1}}{{\sqrt{{{len(self.initial_state)}}}}}$").scale(0.8).next_to(gate_matrix_mobject, LEFT, buff=0.3)
        self.wait(2)
        self.play(FadeOut(gate_label))
        
        # Arrange multiplication layout
        initial_state_matrix.next_to(gate_matrix_mobject, RIGHT, buff=0.3)
        self.play(Write(scalar), Write(gate_matrix_mobject))
        self.play(Write(initial_state_matrix))
        self.wait(2)
        
        # Compute final state
        final_state_vector = np.dot(self.gate_matrix, np.array(self.initial_state).reshape(-1, 1))
        final_state_matrix = Matrix([[str(round(val[0], 2))] for val in final_state_vector]).scale(0.7)
        final_label = Tex("Final State: After Gate Application").scale(0.8).next_to(final_state_matrix, UP, buff=0.3)
        
        # Transition: Initial state → Gate Application → Final state
        self.play(Transform(initial_state_matrix, final_state_matrix))
        self.wait(2)
        self.play(FadeOut(gate_matrix_mobject), FadeOut(scalar))
        
        # Cleanup
        self.play(FadeOut(final_label), FadeOut(final_state_matrix))
        self.wait(1)

if __name__ == "__main__":
    # Example usage with Hadamard gate and |000⟩ state
    initial_state = [1, 0, 0, 0, 0, 0, 0, 0]  # |000⟩ state
    hadamard_3 = [[1, 1, 1, 1, 1, 1, 1, 1],
                  [1, -1, 1, -1, 1, -1, 1, -1],
                  [1, 1, -1, -1, 1, 1, -1, -1],
                  [1, -1, -1, 1, 1, -1, -1, 1],
                  [1, 1, 1, 1, -1, -1, -1, -1],
                  [1, -1, 1, -1, -1, 1, -1, 1],
                  [1, 1, -1, -1, -1, -1, 1, 1],
                  [1, -1, -1, 1, -1, 1, 1, -1]]
    scene = QuantumGateApplication(initial_state, hadamard_3, "Hadamard")
    scene.render()
