import sys
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from flask import Flask, render_template, request, jsonify, send_file
import os
import io
import matplotlib.pyplot as plt
from collections import Counter

app = Flask(__name__)

def is_valid_sudoku(grid, check_filled_only=False):
    for i in range(2):
        row = [x for x in grid[i] if x != 0]
        if len(row) != len(set(row)):
            return False
    for j in range(2):
        col = [grid[i][j] for i in range(2) if grid[i][j] != 0]
        if len(col) != len(set(col)):
            return False
    return True

def create_oracle(grid, circuit, qubits):
    aux_qubit = qubits - 1
    circuit.x(aux_qubit)
    circuit.h(aux_qubit)
    
    # Mark pre-filled cells
    for i in range(2):
        for j in range(2):
            if grid[i][j] != 0:
                val = grid[i][j] - 1  # 0 for 1, 1 for 2
                base = (i * 2 + j) * 2
                if val == 1:  # Only need 1 bit for 1/2 (00=1, 01=2)
                    circuit.x(base)
    
    # Enforce uniqueness in rows
    for i in range(2):
        for j1 in range(2):
            for j2 in range(j1 + 1, 2):
                base1 = (i * 2 + j1) * 2
                base2 = (i * 2 + j2) * 2
                circuit.cx(base1, aux_qubit)
                circuit.cx(base2, aux_qubit)
                circuit.ccx(base1, base2, aux_qubit)
                circuit.cx(base2, aux_qubit)
                circuit.cx(base1, aux_qubit)
    
    # Enforce uniqueness in columns
    for j in range(2):
        for i1 in range(2):
            for i2 in range(i1 + 1, 2):
                base1 = (i1 * 2 + j) * 2
                base2 = (i2 * 2 + j) * 2
                circuit.cx(base1, aux_qubit)
                circuit.cx(base2, aux_qubit)
                circuit.ccx(base1, base2, aux_qubit)
                circuit.cx(base2, aux_qubit)
                circuit.cx(base1, aux_qubit)
    
    # Uncompute pre-filled cells and apply phase
    for i in range(2):
        for j in range(2):
            if grid[i][j] != 0:
                val = grid[i][j] - 1
                base = (i * 2 + j) * 2
                if val == 1:
                    circuit.x(base)
    circuit.x(aux_qubit)
    circuit.h(aux_qubit)
    circuit.z(aux_qubit)
    circuit.h(aux_qubit)
    circuit.x(aux_qubit)
    print("Oracle applied")  # Debug

def grover_algorithm(grid):
    qubits = 2 * 2 * 2 + 1  # 8 qubits + 1 auxiliary (using 1 bit per cell for simplicity)
    qc = QuantumCircuit(qubits, qubits - 1)
    for q in range(qubits):
        qc.h(q)
    iterations = 2  # Optimized for ~2 solutions in 256 states
    for _ in range(iterations):
        create_oracle(grid, qc, qubits)
        # Diffuser
        for q in range(qubits):
            qc.h(q)
            qc.x(q)
        qc.h(qubits - 1)
        qc.mcx(list(range(qubits - 1)), qubits - 1)
        qc.h(qubits - 1)
        for q in range(qubits):
            qc.x(q)
            qc.h(q)
    qc.measure(range(qubits - 1), range(qubits - 1))
    return qc

def solve_sudoku(grid):
    print("Input grid:", grid)  # Debug input
    # Check if pre-filled cells are valid
    if not is_valid_sudoku(grid, check_filled_only=True):
        print("Wrong input: duplicates in pre-filled cells")  # Debug
        return None
    backend = AerSimulator(method="statevector")
    circuit = grover_algorithm(grid)
    job = backend.run(circuit, shots=1500)  # Increased for better sampling
    result = job.result()
    counts = result.get_counts()
    if not counts:
        print("No counts returned from simulation")  # Debug
        return None
    
    solutions = []
    for solution, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:2]:  # Top 2 by count
        print("Raw solution string:", solution, "Count:", count)  # Debug
        solution_grid = [[0] * 2 for _ in range(2)]
        for i in range(2):
            for j in range(2):
                base = (i * 2 + j) * 2
                val = int(solution[base], 2) + 1  # Use first bit only (00=1, 01=2)
                if val > 2:  # Cap at 2
                    val = 2
                # Respect pre-filled cells
                if grid[i][j] != 0:
                    val = grid[i][j]
                solution_grid[i][j] = val
        print("Extracted solution grid:", solution_grid)  # Debug
        if is_valid_sudoku(solution_grid):
            print("Valid solution found:", solution_grid)  # Debug
            solutions.append(solution_grid)
        else:
            print("Invalid solution grid detected")  # Debug
    
    return solutions if solutions else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    grid = []
    for i in range(2):
        row = []
        for j in range(2):
            val = data[str(i)][str(j)]
            row.append(int(val) if val and val.isdigit() else 0)
        grid.append(row)
    print("Parsed grid:", grid)  # Debug
    solutions = solve_sudoku(grid)
    if solutions:
        return jsonify({'success': True, 'solutions': solutions})
    # Check if input is wrong (duplicates in pre-filled)
    if not is_valid_sudoku(grid, check_filled_only=True):
        return jsonify({'success': False, 'message': 'Wrong input: duplicates in pre-filled cells.'})
    return jsonify({'success': False, 'message': 'No solution found or invalid puzzle.'})

@app.route('/reset', methods=['POST'])
def reset():
    return jsonify({'success': True, 'grid': [[0, 0], [0, 0]]})

@app.route('/circuit')
def get_circuit_image():
    grid = [[0, 0], [0, 0]]  # Default grid for circuit generation
    qubits = 2 * 2 * 2 + 1
    qc = QuantumCircuit(qubits, qubits - 1)
    for q in range(qubits):
        qc.h(q)
    create_oracle(grid, qc, qubits)
    for q in range(qubits):
        qc.h(q)
        qc.x(q)
    qc.h(qubits - 1)
    qc.mcx(list(range(qubits - 1)), qubits - 1)
    qc.h(qubits - 1)
    for q in range(qubits):
        qc.x(q)
        qc.h(q)
    qc.measure(range(qubits - 1), range(qubits - 1))
    
    fig = qc.draw(output='mpl', scale=0.7)
    img_data = io.BytesIO()
    fig.savefig(img_data, format='png', bbox_inches='tight')
    plt.close(fig)
    img_data.seek(0)
    return send_file(img_data, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)