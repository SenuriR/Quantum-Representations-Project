from manim import *

class CleanGrowingEPR(Scene):
    def construct(self):
        # Setup parameters
        qubit_labels = ["|0⟩", "|0⟩"]
        qubit_ys = [1, -1]
        gate_width = 0.6
        gate_spacing = 2.0
        x_start = -4.0
        time_steps = [x_start + i * gate_spacing for i in range(4)]  # t=0 to t=3

        # Define gates per time step: {time_step: {qubit_index: gate_type}}
        gates = {
            1: {0: "H"},           # Hadamard on qubit 0 at t=1
            2: {0: "C", 1: "X"},   # CNOT (control on 0, target on 1) at t=2
        }

        # Draw qubit labels
        for i, y in enumerate(qubit_ys):
            label = MathTex(qubit_labels[i]).next_to([x_start, y, 0], LEFT)
            self.play(Write(label))

        # Track current X position of the wire tips per qubit
        current_xs = {i: x_start for i in range(2)}

        # Go through each time step and build the circuit
        for t in range(1, len(time_steps)):
            x_prev = time_steps[t - 1]
            x_curr = time_steps[t]

            # Check if this step is a CNOT
            is_cnot = (
                t in gates and 
                0 in gates[t] and gates[t][0] == "C" and 
                1 in gates[t] and gates[t][1] == "X"
            )

            if is_cnot:
                # === Draw wires around CNOT ===
                for i, y in enumerate(qubit_ys):
                    wire_left = Line([current_xs[i], y, 0], [x_curr - gate_width / 2, y, 0])
                    wire_right = Line([x_curr + gate_width / 2, y, 0], [x_curr + gate_spacing, y, 0])
                    self.play(Create(wire_left))
                    current_xs[i] = x_curr + gate_spacing  # update tracker
                    # defer right side wire until after gate for better animation timing

                # === CNOT construction ===
                control_y = qubit_ys[0]
                target_y = qubit_ys[1]
                control_dot = Dot(point=[x_curr, control_y, 0])
                target_circle = Circle(radius=0.2).move_to([x_curr, target_y, 0])
                target_line = Line([x_curr, target_y - 0.2, 0], [x_curr, target_y + 0.2, 0])
                connector = Line([x_curr, control_y, 0], [x_curr, target_y, 0])

                self.play(Create(connector), FadeIn(control_dot), Create(target_circle), Create(target_line))
                self.bring_to_front(control_dot, target_circle, target_line)

                # Now draw right-side wires
                for i, y in enumerate(qubit_ys):
                    wire_right = Line([x_curr + gate_width / 2, y, 0], [x_curr + gate_spacing, y, 0])
                    self.play(Create(wire_right))

                continue  # skip individual gate drawing logic for this step

            # === Regular gate or no gate ===
            for i, y in enumerate(qubit_ys):
                has_gate = (t in gates) and (i in gates[t])

                if has_gate:
                    # Wire → gate → wire
                    wire_left = Line([current_xs[i], y, 0], [x_curr - gate_width / 2, y, 0])
                    self.play(Create(wire_left))

                    gate_type = gates[t][i]
                    if gate_type == "H":
                        gate = Square(gate_width).move_to([x_curr, y, 0])
                        label = MathTex("H").move_to(gate)
                        self.play(Create(gate), Write(label))
                        self.bring_to_front(gate, label)

                    wire_right = Line([x_curr + gate_width / 2, y, 0], [x_curr + gate_spacing, y, 0])
                    self.play(Create(wire_right))
                    current_xs[i] = x_curr + gate_spacing

                else:
                    # No gate → uninterrupted wire
                    wire = Line([current_xs[i], y, 0], [x_curr + gate_spacing, y, 0])
                    self.play(Create(wire))
                    current_xs[i] = x_curr + gate_spacing

        self.wait(2)
