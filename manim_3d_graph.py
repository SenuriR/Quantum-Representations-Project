from manim import *
import numpy as np

class Graph3DVisualization(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        num_nodes = 6  # Change this value to set the number of nodes
        radius = 3  # Radius of the circular arrangement of nodes
        
        # Generate evenly spaced node positions in 3D space
        node_positions = {
            f"N{i}": np.array([
                radius * np.cos(2 * np.pi * i / num_nodes),
                radius * np.sin(2 * np.pi * i / num_nodes),
                np.sin(2 * np.pi * i / num_nodes)
            ]) for i in range(num_nodes)
        }
        
        # Create nodes (spheres)
        nodes = {name: Sphere(radius=0.2).move_to(pos) for name, pos in node_positions.items()}
        
        # Create edges to form a cycle graph
        edges = [
            Line(node_positions[f"N{i}"], node_positions[f"N{(i+1) % num_nodes}"]) for i in range(num_nodes)
        ]
        
        graph_group = VGroup(*nodes.values(), *edges)
        
        # Add nodes and edges to scene
        self.add(graph_group)
        
        # Camera movements
        self.wait(1)
        self.move_camera(phi=90 * DEGREES, theta=0 * DEGREES, run_time=2)  # Bird's eye view
        self.wait(1)
        self.move_camera(phi=60 * DEGREES, theta=45 * DEGREES, run_time=2)  # High angle view
        self.wait(1)
        self.move_camera(phi=0 * DEGREES, theta=30 * DEGREES, run_time=2)  # Eye level view
        self.wait(1)
        
        # Zoom into a specific node (e.g., node "N0") and set correct Bloch Sphere perspective
        focus_node = "N0"
        self.move_camera(frame_center=node_positions[focus_node], zoom=2, phi=0 * DEGREES, theta=0 * DEGREES, run_time=2)
        self.wait(1)
        
        # Make the entire graph disappear
        self.play(FadeOut(graph_group))
        
        # Display Bloch Sphere at the position of the node
        bloch_sphere = BlochSphere().move_to(node_positions[focus_node])
        self.play(FadeIn(bloch_sphere))
        self.wait(2)
        
        # Remove Bloch Sphere
        self.play(FadeOut(bloch_sphere))
        
        # Make the original graph reappear
        self.play(FadeIn(graph_group))
        self.wait(1)
        
        # Zoom out to original view
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=2)
        self.wait(2)

class BlochSphere(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create Bloch Sphere
        sphere = Sphere(radius=1, color=BLUE)
        sphere.set_opacity(0.5)  # Set opacity separately
        
        # Axes
        x_axis = Arrow3D(start=[-1.5, 0, 0], end=[1.5, 0, 0], color=RED)
        y_axis = Arrow3D(start=[0, -1.5, 0], end=[0, 1.5, 0], color=GREEN)
        z_axis = Arrow3D(start=[0, 0, -1.5], end=[0, 0, 1.5], color=WHITE)
        
        # Labels aligned with Bloch Sphere perspective
        x_label = Tex("X").next_to(x_axis.get_end(), RIGHT)
        y_label = Tex("Y").next_to(y_axis.get_end(), UP)
        z_label = Tex("Z").next_to(z_axis.get_end(), OUT)
        
        # Rotate entire Bloch Sphere to match reference perspective
        self.rotate(PI / 2, axis=Y_AXIS)
        
        # Qubit State Vector
        state_vector = Arrow3D(start=[0, 0, 0], end=[0.7, 0.5, 0.5], color=YELLOW)
        
        # Add elements to VGroup
        self.add(sphere, x_axis, y_axis, z_axis, x_label, y_label, z_label, state_vector)

class SineWaveVisualization(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-PI, PI, PI/4],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": BLUE}
        )
        
        time_tracker = ValueTracker(0)
        
        moving_sine_wave = always_redraw(lambda: FunctionGraph(
            lambda x: np.sin(x - time_tracker.get_value()),
            color=YELLOW,
            x_range=[-PI, PI]
        ))
        
        labels = axes.get_axis_labels(x_label="x", y_label="sin(x)")
        
        self.add(axes, labels, moving_sine_wave)
        self.play(time_tracker.animate.set_value(2 * PI), run_time=4, rate_func=linear)
        self.wait(3)
