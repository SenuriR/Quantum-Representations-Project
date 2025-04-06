from manim import *

class TwoEntangledQubits(Scene):
    def construct(self):
        # Titles
        title = Text("Two Entangled Qubits", font_size=40).to_edge(UP)

        # Create two Bloch spheres using 3D spheres
        qubit1 = Sphere(radius=1, resolution=(24, 48)).shift(LEFT * 3)
        qubit2 = Sphere(radius=1, resolution=(24, 48)).shift(RIGHT * 3)

        qubit1.set_fill(RED, opacity=0.3).set_stroke(WHITE, opacity=0.6)
        qubit2.set_fill(BLUE, opacity=0.3).set_stroke(WHITE, opacity=0.6)

        label1 = Tex(r"$Q_1$").next_to(qubit1, DOWN)
        label2 = Tex(r"$Q_2$").next_to(qubit2, DOWN)

        # Arrows representing Bloch vectors
        vec1 = Arrow3D(start=qubit1.get_center(), end=qubit1.get_center() + OUT, color=YELLOW)
        vec2 = Arrow3D(start=qubit2.get_center(), end=qubit2.get_center() + OUT, color=YELLOW)

        # A line indicating entanglement between the two qubits
        entangled_line = DashedLine(qubit1.get_center(), qubit2.get_center(), color=PURPLE)

        # Optional: State label
        entangled_state = Tex(r"$|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$", font_size=36)
        entangled_state.next_to(entangled_line, DOWN, buff=1)

        self.add(title)
        self.play(FadeIn(qubit1, qubit2), FadeIn(label1, label2))
        self.play(Create(vec1), Create(vec2))
        self.play(Create(entangled_line), Write(entangled_state))
        self.wait(2)
