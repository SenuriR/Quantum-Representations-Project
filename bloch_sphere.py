from manim import *
import numpy as np

class BlochSphereMatchingReference(ThreeDScene):
    def get_bloch_sphere(self):
        # Match reference image: slight overhead, diagonal view
        self.set_camera_orientation(phi=70 * DEGREES, theta=-135 * DEGREES)

        # Sphere
        bloch_sphere = Sphere(radius=1, color=BLUE).set_opacity(0.5)

        # Axes (matching directions in image)
        z_axis = Arrow3D(start=[-1.5, 0, 0], end=[1.5, 0, 0], color=RED)     # X → →
        x_axis = Arrow3D(start=[0, -1.5, 0], end=[0, 1.5, 0], color=GREEN)   # Y ↑ ↑
        y_axis = Arrow3D(start=[0, 0, -1.5], end=[0, 0, 1.5], color=BLUE)    # Z ⊙ (blue, like in image)

        # Labels (positioned clearly away from ends)
        z_label = Tex("Z", color=RED).move_to(x_axis.get_end() + 0.2 * RIGHT)
        x_label = Tex("X", color=GREEN).move_to(y_axis.get_end() + 0.2 * UP)
        y_label = Tex("Y", color=BLUE).move_to(z_axis.get_end() + 0.2 * OUT)

        # State vector (optional)
        state_vector_arrow = Arrow3D(start=[0, 0, 0], end=[0.5, 0.5, 0.7], color=YELLOW)

        # Group
        axes_group = VGroup(x_axis, y_axis, z_axis, x_label, y_label, z_label)
        bloch_group = VGroup(bloch_sphere, axes_group, state_vector_arrow)
        bloch_group.scale(1.2)

        return bloch_group, state_vector_arrow

    def construct(self):
        bloch_sphere, _ = self.get_bloch_sphere()
        self.add(bloch_sphere)
        self.wait(3)
