from manim import *
import numpy as np

class EPRPairGeneration(ThreeDScene):
    def construct(self):
        self.camera.background_color = DARK_GRAY

        # Set initial camera orientation
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        # Create two Bloch spheres
        bloch_radius = 1.5
        bloch1 = self.create_bloch_sphere(label="")
        bloch2 = self.create_bloch_sphere(label="")

        bloch1.move_to(LEFT * 3)
        bloch2.move_to(RIGHT * 3)

        self.play(FadeIn(bloch1, bloch2))
        self.wait(1)

        # Show initial states |0>
        arrow_a = self.add_bloch_vector(bloch1, direction=UP)
        arrow_b = self.add_bloch_vector(bloch2, direction=UP)
        self.wait(1)

        # Rotate camera slightly for better 3D visibility during state manipulation
        # self.move_camera(phi=65 * DEGREES, theta=-60 * DEGREES, run_time=2)
        # self.wait(1)

        # Apply Hadamard to Qubit A (rotate vector to X axis)
        self.play(Rotate(arrow_a, angle=-PI/2, axis=RIGHT, about_point=bloch1.get_center()))
        self.wait(1)

        # Return camera to original position
        # self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES, run_time=2)
        # self.wait(1)

        # Apply CNOT --> Entanglement
        # Rotate camera again for 3D effect during collapse
        # self.move_camera(phi=60 * DEGREES, theta=-50 * DEGREES, run_time=2)
        # self.wait(1)

        # Shrink only the sphere parts to simulate loss of individual state info
        shrink_factor = 0.2 # used to be 0.5
        sphere1, axes1, label1 = bloch1
        sphere2, axes2, label2 = bloch2

        self.play(
            sphere1.animate.scale(shrink_factor),
            sphere2.animate.scale(shrink_factor),
            arrow_a.animate.scale(0),
            arrow_b.animate.scale(0),
            run_time=2
        )
        self.wait(1)

        # Draw entanglement line
        entanglement_line = Line(bloch1.get_center(), bloch2.get_center(), color=YELLOW)
        self.play(Create(entanglement_line))
        self.wait(1)

        # Return camera to original position again for text
        # self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES, run_time=2)
        # self.wait(1)

        # Show final EPR state text
        # epr_text = MathTex(r"|\text{EPR}\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)").scale(0.9).to_edge(DOWN)
        # self.play(Write(epr_text))
        # self.wait(3)

    def create_bloch_sphere(self, label=""):
        sphere = Sphere(radius=1.5, resolution=(30, 30), fill_opacity=0.1, stroke_color=WHITE)
        axes = ThreeDAxes(x_range=[-1.8,1.8], y_range=[-1.8,1.8], z_range=[-1.8,1.8], stroke_color=GRAY)
        label_mob = Text(label).next_to(sphere, UP)
        return VGroup(sphere, axes, label_mob)    

    def add_bloch_vector(self, bloch_group, direction=UP):
        origin = bloch_group.get_center()
        vec = Arrow3D(start=origin, end=origin + direction*1.5, color=RED, thickness=0.03)
        self.add(vec)
        return vec
