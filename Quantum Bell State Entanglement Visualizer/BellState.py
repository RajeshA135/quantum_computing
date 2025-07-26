from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city
import matplotlib.pyplot as plt
from qiskit.exceptions import QiskitError

# Create a quantum circuit with 2 qubits (no classical bits for statevector)
qc_state = QuantumCircuit(2)

# Apply Hadamard gate to the first qubit
qc_state.h(0)

# Apply CNOT gate with first qubit as control and second as target
qc_state.cx(0, 1)

# Explicitly save the statevector
qc_state.save_statevector()

# Simulate the statevector to visualize entanglement
simulator_state = AerSimulator(method='statevector')
try:
    job_state = simulator_state.run(qc_state)
    result_state = job_state.result()
    statevector = result_state.get_statevector(qc_state, decimals=3)
except QiskitError as e:
    print(f"Error retrieving statevector: {e}")
    statevector = None

# Create a new circuit with measurements for histogram
qc_measure = QuantumCircuit(2, 2)
qc_measure.h(0)
qc_measure.cx(0, 1)
qc_measure.measure([0, 1], [0, 1])

# Simulate the circuit for measurement outcomes
simulator = AerSimulator()
job = simulator.run(qc_measure, shots=1000)
result = job.result()
counts = result.get_counts(qc_measure)

# Print the circuit name, statevector, and measurement results
print("Circuit Name: Bell Circuit")
if statevector is not None:
    print("Statevector (before measurement):", statevector)
else:
    print("Statevector: Not available due to simulation error")
print("Measurement results:", counts)

# Visualize the circuit
print("\nQuantum Circuit:")
print(qc_measure.draw())

# Plot statevector as a city plot if available
if statevector is not None:
    print("\nSaving statevector visualization as 'bell_state_city.png'")
    plot_state_city(statevector, title="Bell State City Plot")
    plt.savefig("bell_state_city.png")
    plt.close()

# Plot histogram and save to file
print("Saving measurement histogram as 'bell_circuit_histogram.png'")
plot_histogram(counts, title="Bell Circuit Measurement Outcomes")
plt.savefig("bell_circuit_histogram.png")
plt.show()  # Attempt to display the histogram interactively