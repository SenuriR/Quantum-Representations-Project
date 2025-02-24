from manim import *
import numpy as np

class QuantumGateMatrices(Scene):
    def construct(self):
        title = Tex("Matrix Representations of Quantum Gates and State Evolution").scale(0.8).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        
        # Initial 3-qubit state |000⟩
        initial_state = Matrix(["1", "0", "0", "0", "0", "0", "0", "0"]).scale(0.7)
        state_label = Tex(r"Initial State: $|000\rangle$").scale(0.8).next_to(initial_state, UP, buff=0.3)
        
        self.play(Write(state_label), Write(initial_state))
        self.wait(1)
        self.play(FadeOut(state_label))
        
        # Hadamard gate H^{\otimes 3}
        hadamard_3 = Matrix([
            ["1", "1", "1", "1", "1", "1", "1", "1"],
            ["1", "-1", "1", "-1", "1", "-1", "1", "-1"],
            ["1", "1", "-1", "-1", "1", "1", "-1", "-1"],
            ["1", "-1", "-1", "1", "1", "-1", "-1", "1"],
            ["1", "1", "1", "1", "-1", "-1", "-1", "-1"],
            ["1", "-1", "1", "-1", "-1", "1", "-1", "1"],
            ["1", "1", "-1", "-1", "-1", "-1", "1", "1"],
            ["1", "-1", "-1", "1", "-1", "1", "1", "-1"]
        ]).scale(0.5)
        hadamard_label = Tex("Hadamard Gate $H^{\otimes 3}$").scale(0.8).next_to(hadamard_3, UP, buff=0.5)
        scalar = Tex(r"$\frac{1}{\sqrt{8}}$").scale(0.8).next_to(hadamard_3, LEFT, buff=0.3)
        
        initial_state.next_to(hadamard_3, RIGHT, buff=0.3)
        
        multiply_label = Tex("Apply Hadamard gate to intial state").scale(0.8).next_to(hadamard_3, UP, buff=0.3)
        self.play(Write(multiply_label), Write(scalar), Write(hadamard_3), Write(initial_state))
        self.wait(1)
        
        # Remove Hadamard matrix and scalar before showing transformation
        self.play(FadeOut(hadamard_3), FadeOut(scalar), FadeOut(multiply_label))
        
        # Resulting superposition state
        final_state = Matrix([
            ["1"], ["1"], ["1"], ["1"], ["1"], ["1"], ["1"], ["1"]]
        ).scale(0.7)
        final_label = Tex("Final State: Superposition").scale(0.8).next_to(final_state, UP, buff=0.3)
        
        self.play(Transform(initial_state, final_state))
        self.wait(1)
        
        # Cleanup
        self.play(FadeOut(final_label), FadeOut(final_state))
        self.wait(1)

if __name__ == "__main__":
    scene = QuantumGateMatrices()
    scene.render()
