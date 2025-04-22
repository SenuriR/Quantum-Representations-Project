# === IMPORTS ===
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector, DensityMatrix, Pauli
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_bloch_vector

import numpy as np
import matplotlib.pyplot as plt
import os
import uuid

from manim import *

# === UTILS ===
def generate_bloch_image(bloch_vector, label="Bloch Sphere", output_dir="images"):
    os.makedirs(output_dir, exist_ok=True)
    filename = f"bloch_{uuid.uuid4().hex[:8]}.png"
    save_path = os.path.join(output_dir, filename)

    fig = plot_bloch_vector(bloch_vector, title=label)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    return save_path

from qiskit.quantum_info import partial_trace

def get_single_qubit_bloch_vector(dm, qubit_index):
    paulis = [Pauli("X"), Pauli("Y"), Pauli("Z")]
    reduced_dm = partial_trace(dm, [qubit_index])
    return [np.real(reduced_dm.expectation_value(p)) for p in paulis]


def simulate_circuit(qc):
    simulator = AerSimulator()
    qc.save_statevector()
    t_qc = transpile(qc, simulator)
    result = simulator.run(t_qc).result()
    return Statevector(result.get_statevector())

# === MANIM SCENE ===
class EPRBlochEvolution(Scene):
    def construct(self):
        steps = [
            ("Initial State |00⟩", lambda qc: qc),
            ("After Hadamard on q0", lambda qc: qc.h(0)),
            ("After CNOT (Entangled)", lambda qc: qc.cx(0, 1)),
        ]

        qc = QuantumCircuit(2)
        bloch_images = []

        for step_name, apply_gate in steps:
            step_qc = qc.copy()
            apply_gate(step_qc)

            state = simulate_circuit(step_qc)
            dm = DensityMatrix(state)

            # Generate Bloch vectors and images
            vec0 = get_single_qubit_bloch_vector(dm, 0)
            vec1 = get_single_qubit_bloch_vector(dm, 1)
            img0 = generate_bloch_image(vec0, label=f"{step_name} — Qubit 0")
            img1 = generate_bloch_image(vec1, label=f"{step_name} — Qubit 1")

            bloch_images.append((step_name, img0, img1))

        # Animate each step
        for step_name, img0_path, img1_path in bloch_images:
            title = Text(step_name, font_size=36).to_edge(UP)

            q0_img = ImageMobject(img0_path).scale(0.4).to_edge(LEFT).shift(DOWN * 0.5)
            q1_img = ImageMobject(img1_path).scale(0.4).to_edge(RIGHT).shift(DOWN * 0.5)

            q0_label = Text("Qubit 0", font_size=24).next_to(q0_img, DOWN)
            q1_label = Text("Qubit 1", font_size=24).next_to(q1_img, DOWN)

            group = Group(q0_img, q1_img, q0_label, q1_label)

            self.play(Write(title))
            self.wait(0.5)
            self.play(FadeIn(group, shift=UP), run_time=1.5)
            self.wait(2)
            self.play(FadeOut(title), FadeOut(group))

        self.wait(1)
