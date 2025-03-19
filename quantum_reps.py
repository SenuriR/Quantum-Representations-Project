from manim import *
from qiskit import QuantumCircuit
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
    
class QuantumReps(Scene):
    def __init__(self, qc=None, **kwargs):
        super().__init__(**kwargs)
        if qc is None:
            qc = QuantumCircuit(3, 3)
            qc.h(0)
            qc.cx(0, 1)
            qc.cx(1, 2)
            qc.measure([0, 1, 2], [0, 1, 2])
        self.qc = qc
        self.num_qubits = qc.num_qubits
        self.num_clbits = qc.num_clbits

        self.gates_dict = {
            "id": MathTex(r"I = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}"),  # Identity Gate
            "x": MathTex(r"X = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}"),  # Pauli-X Gate
            "y": MathTex(r"Y = \begin{bmatrix} 0 & -i \\ i & 0 \end{bmatrix}"),  # Pauli-Y Gate
            "z": MathTex(r"Z = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}"),  # Pauli-Z Gate
            "h": MathTex(r"H = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}"),  # Hadamard Gate
            "cx": MathTex(r"\text{CNOT} = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{bmatrix}")  # CNOT Gate
        }

    def construct(self):
        print(self.qc.draw(output='text'))  # Print circuit for debugging

        # Shift entire circuit up to avoid overlap with time axis
        circuit_shift = UP * 1.5

        # Properly position the time axis (t-axis) at the bottom
        t_axis = Line(LEFT * 6, RIGHT * 6, color=YELLOW).to_edge(DOWN, buff=1)
        t_label = Tex("t").next_to(t_axis, DOWN)
        self.play(Create(t_axis), Write(t_label))
        self.wait(1)

        # Initialize qubit labels on the left side
        qubit_labels = VGroup(*[Tex(f"$q_{i}$").to_edge(LEFT).shift(DOWN * i + circuit_shift) for i in range(self.num_qubits)])
        classical_label = Tex("$c$").to_edge(LEFT).shift(DOWN * self.num_qubits + circuit_shift)
        self.play(Write(qubit_labels), Write(classical_label))
        self.wait(1)

        # Initialize lines for qubits and classical bit
        qubit_lines = [Line(LEFT * 6, LEFT * 6, color=WHITE).shift(DOWN * i + circuit_shift) for i in range(self.num_qubits)]
        classical_line = DashedLine(LEFT * 6, LEFT * 6, color=GRAY).shift(DOWN * self.num_qubits + circuit_shift)
        all_lines = VGroup(*qubit_lines, classical_line)
        self.add(all_lines)

        # Initialize time label at the top
        time_label = Tex("t=0").to_edge(UP)
        self.add(time_label)

        # Iterate through time t, growing circuit from the left to the right
        # for t in range(len(self.qc.data)):
        for t in range(1):
            instruction = self.qc.data[t]
            gate, qubits, clbits = instruction.operation, instruction.qubits, instruction.clbits
            q_indices = [self.qc.find_bit(q).index for q in qubits]
            c_indices = [self.qc.find_bit(c).index for c in clbits] if clbits else []
            
            # Extend lines up to current time t, ensuring simultaneous growth
            new_end = LEFT * 6 + RIGHT * (t + 1.5)
            transformations = []
            for q_index in range(self.num_qubits):
                transformations.append(Transform(qubit_lines[q_index], Line(LEFT * 6, new_end, color=WHITE).shift(DOWN * q_index + circuit_shift)))
            if self.num_clbits > 0:
                transformations.append(Transform(classical_line, DashedLine(LEFT * 6, new_end, color=GRAY).shift(DOWN * self.num_clbits + circuit_shift)))
            self.play(AnimationGroup(*transformations, lag_ratio=0), run_time=0.5)
            
            gate_group = None
            
            # Controlled gates (CX, CCX, etc.)
            if gate.name in ["cx", "ccx"]:
                ctrl_dot = Dot().move_to(qubit_lines[q_indices[0]].get_end())
                target_circle = Circle().scale(0.3).move_to(qubit_lines[q_indices[1]].get_end())
                ctrl_line = Line(ctrl_dot.get_center(), target_circle.get_center())
                gate_group = VGroup(ctrl_dot, target_circle, ctrl_line)
            
            # Measurement operations
            elif gate.name in ["measure"]:
                measure_box = Square().scale(0.5).move_to(qubit_lines[q_indices[0]].get_end())
                measure_label = Tex(r"\textbf{M}").scale(0.7).move_to(measure_box)
                arrow = Arrow(measure_box.get_bottom(), measure_box.get_bottom() + DOWN * 0.5, buff=0.1, color=WHITE, stroke_width=2)
                collapse_line = Line(
                    measure_box.get_bottom(), 
                    np.array([measure_box.get_bottom()[0], classical_line.get_top()[1], 0]),
                    color=WHITE, stroke_width=2
                )
                gate_group = VGroup(measure_box, measure_label, arrow, collapse_line)
            
            # Single-qubit gates --> H, I, X, Y, Z
            elif gate.num_qubits == 1:
                buffer_distance = 0.5
                direction = RIGHT

                gate_box = Square().scale(0.5).move_to(qubit_lines[q_indices[0]].get_end() + buffer_distance * direction)

                # gate_box = Square().scale(0.5).move_to(qubit_lines[q_indices[0]].get_end())
                gate_label = Tex(gate.name.upper()).move_to(gate_box)
                gate_group = VGroup(gate_box, gate_label)
            
            if gate_group:
                self.play(FadeIn(gate_group), run_time=0.5)
                self.wait(0.5)
    
            scene_mobjects = self.mobjects.copy()
            self.play(FadeOut(*scene_mobjects), ruin_time=0.5)
            print(f"q_indicies: {q_indices}, {type(q_indices)}")
            print(f"q_index: {q_index}, {type(q_index)}")
            self.get_matrix_rep(gate.name, q_indices[0])
            self.play(FadeIn(*scene_mobjects), run_time=0.5)
            
            # Update time label at the top instead of multiple markers
            new_time_label = Tex(f"t={t + 1}").to_edge(UP)
            self.play(Transform(time_label, new_time_label), run_time=0.5)
            
        self.wait(2)
        # Fade out everything
        self.play(FadeOut(all_lines, qubit_labels, classical_label, t_axis, t_label, time_label))
        self.wait(1)


    # need to edit to show full matrix set, not just t = 1

    def get_matrix_rep(self, gate_name, qubit):
        if gate_name == "measure":
            square = Square().scale(0.5)
            letter_m = Tex("M").move_to(square.get_center())
            gate_group = VGroup(square, letter_m)
            square_group = gate_group
        else:
            script_1 = Tex(f"Applying the {gate_name} (Hadamard) gate is just a mathematical operation")
            script_1.scale_to_fit_width(config.frame_width - 1)  # Ensures text fits the screen
            self.play(FadeIn(script_1))
            self.wait(2)
            self.play(FadeOut(script_1))

            script_2 = Tex(f"This is a simple mathematical representation of the {gate_name} gate")
            script_2.scale_to_fit_width(config.frame_width - 1)
            self.play(FadeIn(script_2))

            matrix_tex = self.gates_dict[gate_name]
            gate_group = VGroup(matrix_tex)
            gate_group.to_corner(UR)

            self.play(FadeIn(gate_group))
            self.wait(2)
            self.play(FadeOut(script_2))

            script_3 = Tex(f"But for now, let's just represent it as a box")
            script_3.scale_to_fit_width(config.frame_width - 1)
            self.play(FadeIn(script_3))

            square = Square().scale(0.5)
            letter = Tex(gate_name).move_to(square.get_center())
            square_group = VGroup(square, letter)
            square_group.to_corner(UR)

            self.play(Transform(gate_group, square_group))
            self.play(FadeOut(script_3))
            self.play(FadeOut(square_group))
            self.play(FadeOut(gate_group))

            script_4 = Tex(f"This is qubit {qubit} represented as a Bloch sphere. Notice the yellow arrow.")
            script_4.scale_to_fit_width(config.frame_width - 1)
            self.play(FadeIn(script_4))
            

            bloch_sphere, state_vector_arrow = BlochSphereInset().get_bloch_sphere()
            bloch_sphere.to_corner(UR)
            self.play(FadeIn(bloch_sphere))
            self.wait(3)
            self.play(FadeOut(script_4))

            script_5 = Tex(f"This yellow arrow is called a \"vector\". It \"defines\" this qubit in a special way.")
            script_5.scale_to_fit_width(config.frame_width - 1)
            self.play(FadeIn(script_5))
            self.wait(3)
            self.play(FadeOut(script_5))

            script_6 = Tex(f"Applying the {gate_name} gate to this qubit is like making the arrow, the vector, point in a different direction.")
            script_6.scale_to_fit_width(config.frame_width - 1)
            self.play(FadeIn(script_6))
            square_group.move_to(bloch_sphere.get_center())
            self.play(FadeIn(square_group))
            self.wait(2)
            self.play(FadeOut(square_group))
            self.wait(2)

            # testing git

            self.play(FadeOut(script_6))

            # Grid transformation visualization
            grid = ThreeDAxes()
            grid.rotate(angle=PI/6, axis=[1, 1, 0])
            grid.scale(0.8)
            self.play(Create(grid))
            self.wait(1)

            script_7 = Tex(f"vector BEFORE applying {gate_name} gate")
            script_7.to_corner(UL)
            self.play(FadeIn(script_7))

            # Move the vector from Bloch Sphere to grid
            extrapolated_vector = Arrow(start=[-1, -1, 0], end=[1, 1, 0], color=YELLOW)
            self.play(Transform(state_vector_arrow, extrapolated_vector))
            self.wait(2)
            self.play(FadeOut(script_7))


            script_8 = Tex(f"vector AFTER applying {gate_name} gate")
            script_8.to_corner(UL)
            self.play(FadeIn(script_8))

            # Apply a matrix transformation to the grid
            transformation_matrix = [[2, 1], [-1, 3]]
            self.play(extrapolated_vector.animate.apply_matrix(transformation_matrix))
            self.wait(2)
            # Fade out elements
            self.play(FadeOut(bloch_sphere, grid, extrapolated_vector, script_8))
            self.wait(1)

        # next: show extrapolated vector back onto the bloch sphere?


    def play_script(self, script_tex):
        script_tex.move_to(UL)
        self.wait(1)
'''_
    def get_matrix_rep(self, gate_name):
        bloch_sphere, state_vector_arrow = BlochSphereInset().get_bloch_sphere()
        bloch_sphere.to_corner(UR)
        self.play(FadeIn(bloch_sphere))

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
        
        # show matrix representation of gate
        if gate_name == "measure":
            square = Square().scale(0.5)
            letter_m = Tex("M").move_to(square.get_center())
            gate_group = VGroup(square, letter_m).move_to(bloch_sphere.get_bottom())
            square_group = gate_group
        else:
            matrix_tex = self.gates_dict[gate_name]
            gate_label = Tex(gate_name).scale(1.2)
            gate_group = VGroup(gate_label, matrix_tex).move_to(bloch_sphere.get_bottom())
            
            square = Square().scale(0.5)
            letter = Tex(gate_name).move_to(square.get_center())
            square_group = VGroup(square, letter).move_to(bloch_sphere.get_bottom())
            
        self.play(FadeIn(gate_group))
        self.wait(2)
        self.play(Transform(gate_group, square_group))
        self.wait(1)
        self.play(FadeOut(square_group))
        # self.play(FadeOut(gate_group))

        transformation_matrix = [[2, 1], [-1, 3]] # this is just a simple example matrix
        self.play(extrapolated_vector.animate.apply_matrix(transformation_matrix))
        self.wait(2)
        
        # Fade out elements
        self.play(FadeOut(grid, extrapolated_vector))
        self.wait(1)
'''
if __name__ == "__main__":
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.measure([0, 1, 2], [0, 1, 2])
    
    scene = QuantumCircuitVisualization(qc)
    scene.render()
