# this is going to end up being the main driver code for the program
from manim import *
from qiskit import QuantumCircuit
import numpy as np

class BlochSphereInset(ThreeDScene):
    def get_bloch_sphere(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=0 * DEGREES)  # looking slightly down, centered on Z-axis

        bloch_sphere = Sphere(radius=1, color=BLUE).set_opacity(0.5)
        
        bloch_axes = VGroup(
            Arrow3D([-1.5, 0, 0], [1.5, 0, 0], color=RED),    # X-axis
            Arrow3D([0, -1.5, 0], [0, 1.5, 0], color=GREEN),  # Y-axis
            Arrow3D([0, 0, -1.5], [0, 0, 1.5], color=WHITE)   # Z-axis
        )
        
        bloch_labels = VGroup(
            Tex("X").next_to(bloch_axes[0].get_end(), RIGHT),
            Tex("Y").next_to(bloch_axes[1].get_end(), UP),
            Tex("Z").next_to(bloch_axes[2].get_end(), OUT)
        )
        
        state_vector_arrow = Arrow3D(start=[0, 0, 0], end=[0.7, 0.5, 0.5], color=YELLOW)
        
        bloch_group = VGroup(bloch_sphere, bloch_axes, bloch_labels, state_vector_arrow)
        bloch_group.scale(0.8)

        # Rotate so Z-axis points toward the camera
        bloch_group.rotate(angle=PI/2, axis=UP)

        return bloch_group, state_vector_arrow

    def construct(self):
        bloch_sphere, state_vector_arrow = BlochSphereInset().get_bloch_sphere()
        bloch_sphere.to_corner(UR)
        self.play(FadeIn(bloch_sphere))
        self.wait(3)
        self.play(FadeOut(bloch_sphere))