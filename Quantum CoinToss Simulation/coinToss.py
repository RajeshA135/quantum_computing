
from qiskit import QuantumCircuit
# Import the simulator from the new location
from qiskit.providers.basic_provider import BasicSimulator
import matplotlib.pyplot as plt

# Create a quantum circuit with 1 qubit and 1 classical bit
qc = QuantumCircuit(1, 1)

# Apply a Hadamard gate to put the qubit in superposition
qc.h(0)

# Measure the qubit
qc.measure(0, 0)

# Use the new simulator
simulator = BasicSimulator()

# Execute the quantum circuit using the run method
job = simulator.run(qc, shots=10000) # Changed execute to simulator.run()

# Get the results
result = job.result()
counts = result.get_counts(qc)

# Print and plot the results
print("Quantum Coin Toss Result:", counts)
plt.bar(counts.keys(), counts.values())
plt.title("Quantum Coin Toss Simulation")
plt.xlabel("Result")
plt.ylabel("Counts")
plt.show()
