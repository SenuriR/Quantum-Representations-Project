from manim import *
import numpy as np

class BlochSphereInset(ThreeDScene):
    def get_bloch_sphere(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        # Bloch Sphere Representation
        bloch_sphere = Sphere(radius=1, color=BLUE)
        bloch_sphere.set_opacity(0.5)
        bloch_axes = VGroup(
            Arrow3D([-1.5, 0, 0], [1.5, 0, 0], color=RED),  # X-axis
            Arrow3D([0, -1.5, 0], [0, 1.5, 0], color=GREEN),  # Y-axis
            Arrow3D([0, 0, -1.5], [0, 0, 1.5], color=WHITE)   # Z-axis
        )
        bloch_labels = VGroup(
            Tex("X").next_to(bloch_axes[0].get_end(), RIGHT),
            Tex("Y").next_to(bloch_axes[1].get_end(), UP),
            Tex("Z").next_to(bloch_axes[2].get_end(), OUT)
        )
        state_vector_arrow = Arrow3D(start=[0, 0, 0], end=[0.7, 0.5, 0.5], color=YELLOW)
        bloch_group = VGroup(bloch_sphere, bloch_axes, bloch_labels, state_vector_arrow).scale(0.8).rotate(angle=PI/6, axis=[1, 1, 0])
        return bloch_group, state_vector_arrow

class MatrixTransformation(Scene):
    def construct(self):
        # Define a matrix
        matrix = Matrix([[2, 1], [-1, 3]])
        matrix_label = Tex("A = ").next_to(matrix, LEFT)
        matrix_group = VGroup(matrix_label, matrix).scale(0.8).to_edge(LEFT)
        
        # Display the matrix
        self.play(Write(matrix_group))
        self.wait(2)
        
        # Define a vector
        vector = Matrix([[1], [2]])
        vector_label = Tex("v = ").next_to(vector, LEFT)
        vector_group = VGroup(vector_label, vector).scale(0.8).next_to(matrix_group, RIGHT, buff=1.5)
        
        # Display the vector
        self.play(Write(vector_group))
        self.wait(2)
        
        # Show matrix-vector multiplication
        result_vector = Matrix([[4], [5]])  # Computed result of A * v
        result_label = Tex("A v = ").next_to(result_vector, LEFT)
        result_group = VGroup(result_label, result_vector).scale(0.8).next_to(vector_group, RIGHT, buff=1.5)
        
        transformation_arrow = Arrow(vector_group.get_right(), result_group.get_left(), buff=0.1)
        
        self.play(GrowArrow(transformation_arrow))
        self.play(Write(result_group))
        self.wait(2)
        
        # Fade out mathematical elements
        self.play(FadeOut(matrix_group, vector_group, transformation_arrow, result_group))
        self.wait(1)
        
        # Show quantum representation
        bloch_sphere, state_vector_arrow = BlochSphereInset().get_bloch_sphere()
        bloch_sphere.to_corner(UR)
        self.play(FadeIn(bloch_sphere))
        
        state_label = Tex(r"$|\psi\rangle = \alpha |0\rangle + \beta |1\rangle$").scale(0.8).to_edge(UP)
        prob_chart = BarChart([0.7, 0.3], bar_names=["$|0\rangle$", "$|1\rangle$"], color=[BLUE, RED]).scale(0.8).shift(RIGHT*2)
        
        self.play(Write(state_label), Create(prob_chart))
        self.wait(2)
        
        # Transition from quantum to classical representation
        self.play(FadeOut(prob_chart, state_label))
        
        # Grid transformation visualization
        grid = ThreeDAxes()
        # Adjust grid position for better 3D visualization
        grid.rotate(angle=PI/6, axis=[1, 1, 0])
        grid.scale(0.8)
        self.play(Create(grid))
        self.wait(1)
        
        # Move the vector from Bloch Sphere to grid
        extrapolated_vector = Arrow(start=[-1, -1, 0], end=[1, 1, 0], color=YELLOW)
        self.play(Transform(state_vector_arrow, extrapolated_vector))
        self.wait(2)
        
        # Fade out Bloch Sphere
        self.play(FadeOut(bloch_sphere))
        
        # Apply a matrix transformation to the grid
        transformation_matrix = [[2, 1], [-1, 3]]
        self.play(extrapolated_vector.animate.apply_matrix(transformation_matrix))
        self.wait(2)
        
        # Fade out elements
        self.play(FadeOut(grid, extrapolated_vector))
        self.wait(1)

if __name__ == "__main__":
    scene = MatrixTransformation()
    scene.render()
