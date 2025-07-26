## Grover's Search Simulation

## Project Overview

This project implements a simulation of Grover's quantum search algorithm using Python, Qiskit, and Matplotlib. Grover's algorithm offers a quadratic speedup for searching an unsorted database compared to classical algorithms, achieving (O(\sqrt{N})) complexity for a database of size (N). The implementation simulates searching for a specific item (target state) in an unsorted quantum database of size (2^n), where (n) is the number of qubits.

## Key Features

Quantum Simulation: Uses Qiskit and qiskit-aer to simulate a quantum circuit on a classical computer.
Visualization: Generates a clear Matplotlib bar chart to display the probability distribution of measured states.
Default Configuration: Searches a 4-item database ((n=2) qubits) for the target state (|11\rangle).

## Output:
The script produces a Matplotlib bar chart and console output for the Grover's algorithm simulation.

Matplotlib Bar Chart:
X-axis: States (00, 01, 10, 11).
Y-axis: Probability (0 to 1).
Colors: Target state (11) in orange; others in blue.
Labels: Probabilities shown on top of bars (e.g., 0.93).
Saved: As grover_search_results.png in the working directory.
Description: Visualizes probabilities for states 00, 01, 10, 11 ((n=2) qubits).
## Example (your result):
Search results for target state '11':
State 11: 1024 counts (100.00% probability)

Explanation: State 11 was measured 1024/1024 times, showing perfect amplification. Other states (00, 01, 10) have 0% probability due to ideal simulation with 1024 shots. Typical runs may show small probabilities (2–5%) for non-target states.