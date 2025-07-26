from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Create a quantum circuit with 2 qubits and 2 classical bits
qc = QuantumCircuit(2, 2)

# Apply Hadamard gate to the first qubit
qc.h(0)

# Apply CNOT gate with first qubit as control and second as target
qc.cx(0, 1)

# Measure both qubits
qc.measure([0, 1], [0, 1])

# Simulate the circuit
simulator = AerSimulator()
job = simulator.run(qc, shots=1000)
result = job.result()
counts = result.get_counts(qc)

# Print the circuit name and measurement results
print("Circuit Name: Bell Circuit")
print("Measurement results:", counts)

# Optional: Visualize the circuit and results
print("\nQuantum Circuit:")
print(qc.draw())

# Plot histogram 
plot_histogram(counts)
plt.show()  # Attempt to display the histogram interactively