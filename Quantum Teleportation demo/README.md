## Quantum Teleportation Demo
## Overview

This project demonstrates the quantum teleportation protocol using Qiskit, a Python library for quantum computing. Quantum teleportation transfers a quantum state from one qubit to another using entanglement and classical communication. The script creates a 3-qubit circuit, prepares a random quantum state, teleports it, and simulates the results.
## Working:
Initialization: Sets up a 3-qubit quantum circuit (q0: Alice's qubit to teleport, q1 and q2: entangled pair) and 2 classical bits.
State Preparation: Applies arbitrary rotations (Rx, Ry) to q0 to create a random quantum state.
Entanglement: Creates a Bell pair between q1 and q2 using Hadamard and CNOT gates.
Alice's Operations: Applies CNOT (q0, q1) and Hadamard (q0), then measures q0 and q1.
Bob's Corrections: Applies X and Z gates to q2 based on classical measurement outcomes using conditional operations.
Simulation: Runs the circuit on the AerSimulator and prints results.