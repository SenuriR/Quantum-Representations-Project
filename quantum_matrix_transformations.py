from manim import *
import numpy as np

class QuantumGateMatrices(Scene):
    def construct(self):
        title = Tex("Matrix Representations of Quantum Gates").to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Define explicit matrix representations of quantum gates
        gates = {
            "Hadamard (H)": Matrix([["1", "1"], ["1", "-1"]]),
            "Pauli-X (X)": Matrix([[0, 1], [1, 0]]),
            "Pauli-Y (Y)": Matrix([["0", "-i"], ["i", "0"]]),
            "Pauli-Z (Z)": Matrix([["1", "0"], ["0", "-1"]]),
            "CNOT": Matrix([["1", "0", "0", "0"],
                             ["0", "1", "0", "0"],
                             ["0", "0", "0", "1"],
                             ["0", "0", "1", "0"]]),
            "T Gate": Matrix([["1", "0"], ["0", "e^{i\pi/4}"]]),
            "S Gate": Matrix([["1", "0"], ["0", "i"]])
        }
        
        y_offset = 2.5
        for gate_name, matrix in gates.items():
            gate_label = Tex(gate_name).move_to(ORIGIN + UP * y_offset)
            unitary_matrix = matrix.scale(1.0).next_to(gate_label, DOWN, buff=1.2)
            
            if gate_name == "Hadamard (H)":
                scalar = Tex("$\\frac{1}{\\sqrt{2}}$").next_to(unitary_matrix, LEFT, buff=0.7)
                self.play(Write(gate_label), Write(scalar), Write(unitary_matrix))
                self.wait(2)
                self.play(FadeOut(scalar))
            else:
                self.play(Write(gate_label), Write(unitary_matrix))
            
            self.wait(2)
            
            self.play(FadeOut(gate_label, unitary_matrix))
            self.wait(1)
        
        self.play(FadeOut(title))
        self.wait(1)

if __name__ == "__main__":
    scene = QuantumGateMatrices()
    scene.render()
