import numpy as np

def hadamard(n):
    """Returns the Hadamard gate for n qubits"""
    H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    H_n = H
    for _ in range(n - 1):
        H_n = np.kron(H_n, H)
    return H_n

def not_gate(n, target):
    """Returns the NOT (Pauli-X) gate for n qubits applied to the target qubit (0-indexed)"""
    I = np.eye(2)  # Identity matrix
    X = np.array([[0, 1], [1, 0]])  # Pauli-X gate
    gate = 1  # Start with scalar identity

    for i in range(n):
        gate = np.kron(gate, X if i == target else I)

    return gate

def cnot(n, control, target):
    """Returns the CNOT gate for n qubits where 'control' and 'target' are qubit indices (0-indexed)"""
    dim = 2**n
    CNOT = np.eye(dim)

    for i in range(dim):
        binary = list(format(i, f"0{n}b"))  # Get binary representation of the index
        if binary[control] == '1':  # If control qubit is 1, flip the target qubit
            binary[target] = '1' if binary[target] == '0' else '0'
            new_index = int("".join(binary), 2)  # Convert back to integer index
            CNOT[i, i] = 0
            CNOT[i, new_index] = 1

    return CNOT

# Define common gates for quick lookup
gate_definitions = {
    "hadamard_1": hadamard(1),
    "hadamard_2": hadamard(2),
    "hadamard_3": hadamard(3),
    "not_1": not_gate(1, 0),
    "not_2": not_gate(2, 1),
    "not_3": not_gate(3, 2),
    "cnot_2": cnot(2, 0, 1),
    "cnot_3": cnot(3, 0, 2),
}
