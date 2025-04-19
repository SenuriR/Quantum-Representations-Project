# === QISKIT: Generate Bloch sphere and save ===
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, DensityMatrix, Pauli
from qiskit.visualization import plot_bloch_vector
import numpy as np
import matplotlib.pyplot as plt
import os

# Create output folder if it doesn't exist
os.makedirs("images", exist_ok=True)
save_path = "images/bloch_plus_state.png"

# Create quantum circuit and apply Hadamard to generate |+⟩
qc = QuantumCircuit(1)
qc.h(0)
qc.save_statevector()

# Simulate
simulator = AerSimulator()
t_qc = transpile(qc, simulator)
result = simulator.run(t_qc).result()
state = Statevector(result.get_statevector())

# Convert to density matrix and compute Bloch vector
dm = DensityMatrix(state)
paulis = [Pauli("X"), Pauli("Y"), Pauli("Z")]
bloch_vector = [np.real(dm.expectation_value(p)) for p in paulis]

# Plot and save Bloch sphere image
fig = plot_bloch_vector(bloch_vector, title="Bloch Sphere: |+⟩ State")
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close(fig)  # Close the figure to free up resources

# === MANIM: Load and display the saved image ===
from manim import *

class BlochSphereFromImage(Scene):
    def construct(self):
        # Title text
        title = Text("Bloch Sphere of a Qubit in |+⟩ State", font_size=36)
        title.to_edge(UP)

        # Load the saved Bloch image
        bloch_image = ImageMobject("images/bloch_plus_state.png")
        bloch_image.scale(0.5)

        # Add padding
        padded_container = SurroundingRectangle(bloch_image, buff=0.3, color=WHITE, stroke_opacity=0.2)
        group = Group(bloch_image, padded_container)
        group.move_to(DOWN)

        # Animate
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(group, shift=UP), run_time=1.5)
        self.wait(2)
