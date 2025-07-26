from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import numpy as np

# Create quantum and classical registers
qr = QuantumRegister(3, name='q')  # 3 qubits: Alice's qubit, entangled pair
cr = ClassicalRegister(2, name='c')  # 2 classical bits for measurements
circuit = QuantumCircuit(qr, cr)

# Step 1: Prepare a random state to teleport (on q0)
# For demo, apply arbitrary rotations to create a state
circuit.rx(np.pi/3, qr[0])
circuit.ry(np.pi/4, qr[0])

# Step 2: Create Bell pair between q1 and q2
circuit.h(qr[1])
circuit.cx(qr[1], qr[2])

# Step 3: Alice's operations
circuit.cx(qr[0], qr[1])
circuit.h(qr[0])

# Step 4: Measure Alice's qubits
circuit.measure(qr[0], cr[0])
circuit.measure(qr[1], cr[1])

# Step 5: Bob's corrections based on classical bits
with circuit.if_test((cr[1], 1)):
    circuit.x(qr[2])
with circuit.if_test((cr[0], 1)):
    circuit.z(qr[2])

# Simulate the circuit
simulator = AerSimulator()
job = simulator.run(circuit, shots=1024)
result = job.result()
counts = result.get_counts(circuit)

# Print results
print("Measurement outcomes:", counts)

# Optional: Visualize the circuit
print(circuit)
