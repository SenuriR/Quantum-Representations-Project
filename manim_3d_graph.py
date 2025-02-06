from manim import *
import numpy as np

class Graph3DVisualization(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # Define node positions
        node_positions = {
            "A": np.array([-2, 1, 0]),
            "B": np.array([0, 2, 1]),
            "C": np.array([2, 1, -1]),
            "D": np.array([1, -1, 0]),
            "E": np.array([-1, -2, 1])
        }
        
        # Create nodes (spheres)
        nodes = {name: Sphere(radius=0.2).move_to(pos) for name, pos in node_positions.items()}
        
        # Time tracker for oscillation
        time_tracker = ValueTracker(0)
        
        # Function to create a smoothly oscillating edge with correct start and end positions
        def get_wiggling_edge(start, end, phase=0, amplitude=0.3, speed=2):
            edge_vector = end - start  # Direction of the edge
            edge_length = np.linalg.norm(edge_vector)
            unit_edge = edge_vector / edge_length  # Normalize
            
            # Perpendicular direction for oscillation
            perpendicular = np.cross(unit_edge, [0, 1, 0])  # Choose a perpendicular direction
            perpendicular = normalize(perpendicular)  
            
            return always_redraw(lambda: ParametricFunction(
                lambda t: start + t * edge_vector + 
                          amplitude * np.sin(speed * time_tracker.get_value() + phase + t * PI) * perpendicular,
                t_range=[0, 1],
                color=WHITE
            ))
        
        # Create edges with flowing sine wave effect
        edges = [
            get_wiggling_edge(node_positions["A"], node_positions["B"], phase=0),
            get_wiggling_edge(node_positions["B"], node_positions["C"], phase=PI / 3),
            get_wiggling_edge(node_positions["C"], node_positions["D"], phase=2 * PI / 3),
            get_wiggling_edge(node_positions["D"], node_positions["E"], phase=PI),
            get_wiggling_edge(node_positions["E"], node_positions["A"], phase=4 * PI / 3),
            get_wiggling_edge(node_positions["A"], node_positions["C"], phase=5 * PI / 3),
        ]
        
        # Add nodes and edges to scene
        self.add(*nodes.values(), *edges)
        
        # Animate oscillation
        self.play(time_tracker.animate.set_value(2 * PI), run_time=4, rate_func=linear)
        
        # Camera movements
        self.wait(1)
        self.move_camera(phi=90 * DEGREES, theta=0 * DEGREES, run_time=2)  # Bird's eye view
        self.wait(1)
        self.move_camera(phi=60 * DEGREES, theta=45 * DEGREES, run_time=2)  # High angle view
        self.wait(1)
        self.move_camera(phi=0 * DEGREES, theta=30 * DEGREES, run_time=2)  # Eye level view
        self.wait(1)
        
        # Zoom into a specific node (e.g., node "B")
        self.move_camera(frame_center=node_positions["B"], zoom=2, run_time=2)
        self.wait(2)
        
        # Reset camera
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=2)
        self.wait(2)

class SineWaveVisualization(Scene):
    def construct(self):
        axes = Axes( # Define graph parameters
            x_range=[-PI, PI, PI/4],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": BLUE}
        )

        labels = axes.get_axis_labels(x_label="x", y_label="sin(x)")
        
        time_tracker = ValueTracker(0) # needed to show function movement
        
        moving_sine_wave = always_redraw(lambda: FunctionGraph(
            lambda x: np.sin(x - time_tracker.get_value()),
            color=YELLOW,
            x_range=[-PI, PI]
        ))
        
        self.add(axes, labels, moving_sine_wave)
        self.play(time_tracker.animate.set_value(2 * PI), run_time=4, rate_func=linear)
        self.wait(3)
