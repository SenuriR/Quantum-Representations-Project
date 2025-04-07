from manim import *
from bloch_sphere import BlochSphere
from circuit import Circuit
from entangled_qubits import TwoEntangledQubits
from vector import EPRPairMatrixWalkthrough

class QuantumReps(Scene):
    def construct(self):
        # scene 1
        text = Text("EPR Pair Example")
        self.play(FadeIn(text))
        self.wait(2)
        self.play(FadeOut(text))

