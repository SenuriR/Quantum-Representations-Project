from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, DensityMatrix, Pauli
from qiskit.visualization import plot_bloch_vector
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs("images", exist_ok=True)

# === Path to save the image ===
save_path = "images/bloch_plus_state.png"  # Change this as needed (e.g. "output/bloch.png")

# Create a single-qubit quantum circuit
qc = QuantumCircuit(1)
qc.h(0)  # Apply Hadamard gate

# Save the statevector
qc.save_statevector()

# Transpile and simulate
simulator = AerSimulator()
t_qc = transpile(qc, simulator)
result = simulator.run(t_qc).result()
state = Statevector(result.get_statevector())

# Convert to density matrix
dm = DensityMatrix(state)

# Compute Bloch vector
paulis = [Pauli("X"), Pauli("Y"), Pauli("Z")]
bloch_vector = [np.real(dm.expectation_value(p)) for p in paulis]

# Plot Bloch vector
fig = plot_bloch_vector(bloch_vector, title="Bloch Sphere: |+⟩ State")

# Save the figure to the specified path
plt.savefig(save_path, dpi=300, bbox_inches='tight')  # Adjust DPI for quality

# Show plot (optional, can be commented out in headless environments)
plt.show()
