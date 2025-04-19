from manim import *

class BlochSphereFromImage(Scene):
    def construct(self):
        # Title text
        title = Text("Bloch Sphere of a Qubit in |+⟩ State", font_size=36)
        title.to_edge(UP)

        # Load image
        bloch_image = ImageMobject("images/bloch_plus_state.png")
        bloch_image.scale(0.5)

        # Add padding with a surrounding rectangle
        padded_container = SurroundingRectangle(bloch_image, buff=0.3, color=WHITE, stroke_opacity=0.2)

        # Use Group instead of VGroup since ImageMobject is not a VMobject
        group = Group(bloch_image, padded_container)
        group.move_to(DOWN)

        # Animate
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(group, shift=UP), run_time=1.5)
        self.wait(2)

# next step: combine manim_bloch with qiskit_bloch to (1) generate bloch image via qiskit and (2) save, obtain, and display that image via qiskit