from manim import *
import numpy as np

class BlochSphere(ThreeDScene):
    def get_bloch_sphere(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)

        # Bloch Sphere
        bloch_sphere = Sphere(radius=1, color=BLUE).set_opacity(0.5)

        # Axes: quantum Z = Manim Z (vertical/blue), X = green, Y = red
        x_axis = Arrow3D(start=[-1.5, 0, 0], end=[1.5, 0, 0], color=GREEN)  # X axis (|+>, |->)
        y_axis = Arrow3D(start=[0, -1.5, 0], end=[0, 1.5, 0], color=RED)    # Y axis (|+i>, |-i>)
        z_axis = Arrow3D(start=[0, 0, -1.5], end=[0, 0, 1.5], color=BLUE)   # Z axis (|0>, |1>)

        ket_0 = Tex(r"$\left|0\right\rangle$")
        ket_0.move_to(z_axis.get_end() + 0.3 * OUT)
        ket_0.rotate(PI/2, axis=RIGHT).rotate(PI - PI/2, axis=OUT)

        ket_1 = Tex(r"$\left|1\right\rangle$")
        ket_1.move_to(z_axis.get_start() + 0.3 * IN)
        ket_1.rotate(PI/2, axis=RIGHT).rotate(PI - PI/2, axis=OUT)

        ket_plus = Tex(r"$\left|+\right\rangle$")
        ket_plus.move_to(x_axis.get_end() + 0.3 * RIGHT)
        ket_plus.rotate(PI/2, axis=RIGHT).rotate(PI - PI/2, axis=OUT)

        ket_minus = Tex(r"$\left|-\right\rangle$")
        ket_minus.move_to(x_axis.get_start() + 0.3 * LEFT)
        ket_minus.rotate(PI/2, axis=RIGHT).rotate(PI - PI/2, axis=OUT)

        ket_plus_i = Tex(r"$\left|+i\right\rangle$")
        ket_plus_i.move_to(y_axis.get_end() + 0.3 * UP)
        ket_plus_i.rotate(PI/2, axis=RIGHT).rotate(PI - PI/2, axis=OUT)

        ket_minus_i = Tex(r"$\left|-i\right\rangle$")
        ket_minus_i.move_to(y_axis.get_start() + 0.3 * DOWN)
        ket_minus_i.rotate(PI/2, axis=RIGHT).rotate(PI - PI/2, axis=OUT)


        # State vector (optional)
        state_vector_arrow = Arrow3D(start=[0, 0, 0], end=[0.5, 0.5, 0.7], color=YELLOW)

        # Group everything
        axes_group = VGroup(x_axis, y_axis, z_axis)
        state_labels = VGroup(ket_0, ket_1, ket_plus, ket_minus, ket_plus_i, ket_minus_i)
        bloch_group = VGroup(bloch_sphere, axes_group, state_labels, state_vector_arrow)
        bloch_group.scale(1.2)

        return bloch_group, state_vector_arrow

    def construct(self):
        bloch_sphere, _ = self.get_bloch_sphere()
        self.add(bloch_sphere)
        self.wait(3)
