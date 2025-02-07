from manim import *
import numpy as np
import sys
from typing import List

class Graph3DVisualization(ThreeDScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num_graphs = 3
        self.num_nodes = [3, 4, 5]
        self.radius = 2.5  # Adjusted for better fit
        self.graph_spacing = 6  # Adjusted spacing
        self.graph_centers = []
        self.graph_vgroups = []
        self.node_positions = {}
        self.connection_lines = []
    
    def create_graphs(self):
        self.graph_centers = []
        self.graph_vgroups = []
        self.node_positions = {}
        all_graphs = []
        
        for g in range(self.num_graphs):
            center_position = np.array([g * self.graph_spacing, 0, 0])
            self.graph_centers.append(center_position)
            
            node_positions = {
                f"G{g}_N{i}": center_position + np.array([
                    self.radius * np.cos(2 * np.pi * i / self.num_nodes[g]),
                    self.radius * np.sin(2 * np.pi * i / self.num_nodes[g]),
                    0  # Keep all graphs in the same plane
                ]) for i in range(self.num_nodes[g])
            }
            self.node_positions.update(node_positions)
            
            nodes = {name: Sphere(radius=0.2).move_to(pos) for name, pos in node_positions.items()}
            edges = [
                DashedLine(node_positions[f"G{g}_N{i}"], node_positions[f"G{g}_N{(i+1) % self.num_nodes[g]}"], stroke_width=2) 
                for i in range(self.num_nodes[g])
            ]
            
            graph_group = VGroup(*nodes.values(), *edges)
            all_graphs.append(graph_group)
            self.graph_vgroups.append(graph_group)
        
        self.connection_lines = [
            Line(self.graph_centers[i], self.graph_centers[i+1], color=WHITE, stroke_width=3) 
            for i in range(self.num_graphs - 1)
        ]
        
        self.add(*all_graphs, *self.connection_lines)
    
    def show_all_graphs(self):
        """Set camera to a high-angle view to see all graphs."""
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, frame_center=np.mean(self.graph_centers, axis=0), run_time=2)
        self.wait(2)
    
    def inspect_node(self, graph_num: int, node_num: int):
        focus_node = f"G{graph_num}_N{node_num}"
        if focus_node not in self.node_positions:
            return
        
        self.move_camera(frame_center=self.node_positions[focus_node], zoom=2, run_time=2)
        self.wait(1)
        
        self.play(FadeOut(*self.graph_vgroups, *self.connection_lines))
        bloch_sphere = BlochSphere().move_to(self.node_positions[focus_node])
        self.play(FadeIn(bloch_sphere))
        self.wait(2)
        
        self.play(FadeOut(bloch_sphere))
        self.play(FadeIn(*self.graph_vgroups, *self.connection_lines))
        self.show_all_graphs()
    
    def delete_node(self, graph_num: int, node_num: int):
        focus_node = f"G{graph_num}_N{node_num}"
        if focus_node in self.node_positions:
            node_mobject = next((m for m in self.graph_vgroups[graph_num].submobjects if isinstance(m, Sphere) and np.allclose(m.get_center(), self.node_positions[focus_node])), None)
            if node_mobject:
                self.play(FadeOut(node_mobject))
            del self.node_positions[focus_node]
            self.num_nodes[graph_num] -= 1  # Update node count dynamically
        
        self.clear()  # Remove existing elements
        self.create_graphs()  # Re-create graphs reflecting the deletion
        self.show_all_graphs()  # Ensure the updated visualization is visible

    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.create_graphs()
        self.wait(2)
        
        # Show all graphs
        self.show_all_graphs()
        
        # Inspect a node
        self.inspect_node(graph_num=0, node_num=1)
        self.wait(2)

        # Show all graphs
        self.show_all_graphs()
        
        # Delete a node and update the visualization
        self.delete_node(graph_num=1, node_num=2)
        self.wait(2)

class BlochSphere(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        sphere = Sphere(radius=1, color=BLUE)
        sphere.set_opacity(0.5)
        
        x_axis = Arrow3D(start=[-1.5, 0, 0], end=[1.5, 0, 0], color=RED)
        y_axis = Arrow3D(start=[0, -1.5, 0], end=[0, 1.5, 0], color=GREEN)
        z_axis = Arrow3D(start=[0, 0, -1.5], end=[0, 0, 1.5], color=WHITE)
        
        x_label = Tex("X").next_to(x_axis.get_end(), RIGHT)
        y_label = Tex("Y").next_to(y_axis.get_end(), UP)
        z_label = Tex("Z").next_to(z_axis.get_end(), OUT)
        
        state_vector = Arrow3D(start=[0, 0, 0], end=[0.7, 0.5, 0.5], color=YELLOW)
        
        self.add(sphere, x_axis, y_axis, z_axis, x_label, y_label, z_label, state_vector)

if __name__ == "__main__":
    scene = Graph3DVisualization()
    scene.render()
