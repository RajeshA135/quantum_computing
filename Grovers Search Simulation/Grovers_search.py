from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib.pyplot as plt

# Number of qubits (n = 2 for a database of size 2^2 = 4)
n_qubits = 2
# Target state to search for (e.g., '11' in binary)
target = '11'

# Create the quantum circuit
qc = QuantumCircuit(n_qubits, n_qubits)

# Step 1: Initialize qubits in superposition using Hadamard gates
for qubit in range(n_qubits):
    qc.h(qubit)

# Step 2: Define the oracle for the target state
def oracle(qc, n_qubits, target):
    # Apply X gates to flip qubits where target has '0'
    for i, bit in enumerate(reversed(target)):
        if bit == '0':
            qc.x(i)
    # Apply multi-controlled Z gate (equivalent to phase flip for target state)
    qc.h(n_qubits-1)
    qc.mcx(list(range(n_qubits-1)), n_qubits-1)
    qc.h(n_qubits-1)
    # Undo X gates
    for i, bit in enumerate(reversed(target)):
        if bit == '0':
            qc.x(i)

# Step 3: Define the diffusion operator (Grover's amplitude amplification)
def diffuser(qc, n_qubits):
    # Apply Hadamard gates
    for qubit in range(n_qubits):
        qc.h(qubit)
    # Apply X gates
    for qubit in range(n_qubits):
        qc.x(qubit)
    # Apply multi-controlled Z gate
    qc.h(n_qubits-1)
    qc.mcx(list(range(n_qubits-1)), n_qubits-1)
    qc.h(n_qubits-1)
    # Undo X gates
    for qubit in range(n_qubits):
        qc.x(qubit)
    # Undo Hadamard gates
    for qubit in range(n_qubits):
        qc.h(qubit)

# Step 4: Apply Grover iterations
# Optimal number of iterations is approximately sqrt(2^n)
iterations = int(np.pi/4 * np.sqrt(2**n_qubits))
for _ in range(iterations):
    oracle(qc, n_qubits, target)
    diffuser(qc, n_qubits)

# Step 5: Measure the qubits
qc.measure(range(n_qubits), range(n_qubits))

# Step 6: Execute the circuit on a simulator
simulator = AerSimulator()
job = simulator.run(qc, shots=1024)
result = job.result()
counts = result.get_counts()

# Step 7: Prepare data for plotting
states = [format(i, f'0{n_qubits}b') for i in range(2**n_qubits)]
probabilities = [counts.get(state, 0) / 1024 for state in states]

# Step 8: Plot the results using Matplotlib
plt.figure(figsize=(8, 6))
bars = plt.bar(states, probabilities, color=['#1f77b4' if state != target else '#ff7f0e' for state in states])
plt.xlabel('States', fontsize=12)
plt.ylabel('Probability', fontsize=12)
plt.title(f"Grover's Search Results (Target: {target})", fontsize=14)
plt.ylim(0, 1)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add value labels on top of bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.02, f'{yval:.2f}', ha='center', fontsize=10)

# Save the plot to a file
plt.savefig('grover_search_results.png')
print("Plot saved as 'grover_search_results.png'")

# Ensure interactive backend (optional, for troubleshooting)
print("Matplotlib backend:", plt.get_backend())
plt.tight_layout()
plt.show()

# Print numerical results
print(f"Search results for target state '{target}':")
for state, count in counts.items():
    print(f"State {state}: {count} counts ({count/1024:.2%} probability)")