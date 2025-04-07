from manim import *
import numpy as np

class TwoQubitColoredBlochSpheres(ThreeDScene):
    def get_bloch_sphere(self, sphere_color=BLUE, state_vector_endpoint=[0, 0, 1.5]):
        # Ensure correct type for vector arithmetic
        state_vector_endpoint = np.array(state_vector_endpoint, dtype=float)

        # Bloch Sphere
        bloch_sphere = Sphere(radius=1)
        bloch_sphere.set_fill(color=sphere_color, opacity=0.5)
        bloch_sphere.set_stroke(color=sphere_color, opacity=0.6)

        # Axes
        x_axis = Arrow3D(start=[-1.5, 0, 0], end=[1.5, 0, 0], color=WHITE)
        y_axis = Arrow3D(start=[0, -1.5, 0], end=[0, 1.5, 0], color=WHITE)
        z_axis = Arrow3D(start=[0, 0, -1.5], end=[0, 0, 1.5], color=WHITE)

        # State vector
        state_vector_arrow = Arrow3D(start=[0, 0, 0], end=state_vector_endpoint, color=RED)

        # Helper for state labels
        def state_label(tex_str, pos):
            return Tex(tex_str, color=WHITE).move_to(pos).rotate(PI / 2, axis=RIGHT).rotate(PI - PI / 6, axis=OUT)

        # Labels
        ket_0 = state_label(r"$\left|0\right\rangle$", z_axis.get_end() + 0.3 * OUT)
        ket_1 = state_label(r"$\left|1\right\rangle$", z_axis.get_start() + 0.3 * IN)
        ket_plus = state_label(r"$\left|+\right\rangle$", x_axis.get_end() + 0.3 * RIGHT)
        ket_minus = state_label(r"$\left|-\right\rangle$", x_axis.get_start() + 0.3 * LEFT)
        ket_plus_i = state_label(r"$\left|+i\right\rangle$", y_axis.get_end() + 0.3 * UP)
        ket_minus_i = state_label(r"$\left|-i\right\rangle$", y_axis.get_start() + 0.3 * DOWN)

        # Grouping
        axes_group = VGroup(x_axis, y_axis, z_axis)
        state_labels = VGroup(ket_0, ket_1, ket_plus, ket_minus, ket_plus_i, ket_minus_i)
        bloch_group = VGroup(bloch_sphere, axes_group, state_labels, state_vector_arrow)
        bloch_group.scale(1.2)

        return bloch_group

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)

        red_qubit = self.get_bloch_sphere(
            sphere_color=YELLOW,
            state_vector_endpoint=[1, 0, 0]
        ).shift(RIGHT * 3 + DOWN * 0.5 + IN * 1.5)

        blue_qubit = self.get_bloch_sphere(
            sphere_color=YELLOW,
            state_vector_endpoint=[0, 1, 0]
        ).shift(LEFT * 3 + UP * 0.2 + OUT * 0.5)

        # Group both Bloch spheres and scale to fit frame
        both_spheres = VGroup(red_qubit, blue_qubit)
        both_spheres.scale(0.6)  # Adjust this value as needed
        self.add(both_spheres)

        self.wait(3)
