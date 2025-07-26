from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt
from qiskit.visualization import plot_bloch_multivector

# Create a quantum circuit with one qubit
qc = QuantumCircuit(1)

# Apply a Hadamard gate to create superposition
qc.h(0)

# Get the statevector of the circuit
state = Statevector.from_instruction(qc)

# Create a figure for the Bloch sphere
plt.figure(figsize=(6, 6))

# Plot the Bloch sphere representation
plot_bloch_multivector(state)

# Save the plot to a file
plt.savefig('bloch_sphere_qubit.png')