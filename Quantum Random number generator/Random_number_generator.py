from qiskit import QuantumCircuit
from qiskit_aer import Aer
import matplotlib.pyplot as plt

def generate_quantum_random_number(num_bits=8):
    # Create a quantum circuit with `num_bits` qubits and classical bits
    qc = QuantumCircuit(num_bits, num_bits)

    # Apply Hadamard gate to each qubit to create superposition
    for i in range(num_bits):
        qc.h(i)

    # Measure each qubit
    qc.measure(range(num_bits), range(num_bits))

    # Use Aer simulator backend
    simulator = Aer.get_backend('qasm_simulator')

    # Run the circuit (1 shot = 1 random number)
    result = simulator.run(qc, shots=1).result()
    counts = result.get_counts()

    # Get the single binary string
    random_bitstring = list(counts.keys())[0]
    random_number = int(random_bitstring, 2)

    return random_bitstring, random_number

# Generate a random number of 8 bits
bits, number = generate_quantum_random_number(8)

print(f"Quantum Random Bitstring: {bits}")
print(f"Random Number (Decimal): {number}")

# Plot result
plt.bar([number], [1], color='green')
plt.xlabel("Random Number (Decimal)")
plt.ylabel("Frequency")
plt.title("Quantum Random Number Generated")
plt.xticks([number], [f"{number} ({bits})"])
plt.show()