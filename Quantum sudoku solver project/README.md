#  Quantum Sudoku Solver using Grover's Algorithm

A beginner-friendly quantum computing project that uses **Grover’s Algorithm** to simulate solving a **3x3 Sudoku puzzle**, wrapped in a beautiful **Flask + HTML/CSS** web interface. Ideal for demonstrating the application of quantum search to constraint satisfaction problems.

---

## 📁 Project Structure

```
Quantum suduko solver project/
├── app.py                  # Flask backend with quantum logic (simulated)
├── requirements.txt        # Python dependencies
├── static/
│   └── style.css           # Modern, responsive UI styling
├── templates/
│   └── index.html          # Sudoku grid and button-based UI
```

---

## 🚀 How to Run Locally

1. **Clone the repository**:

```bash
git clone https://github.com/your-username/quantum-sudoku-solver.git
cd quantum-sudoku-solver
```

2. **Create a virtual environment (optional but recommended)**:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Run the app**:

```bash
python app.py
```

5. **Open in browser**:

```
http://127.0.0.1:5000
```

---

## 🧮 About the Quantum Logic

This version uses a **mock Grover’s algorithm** to demonstrate conceptually how quantum computing can speed up search-based problems like Sudoku. Real quantum simulation for even 3x3 Sudoku is complex due to combinatorial encoding, but this project sets a foundation for further research or presentation.

---

## 🎨 Features

* 3x3 Sudoku grid input
* "Quantum Solve" button (simulated solution)
* "Reset" button
* Responsive and modern UI with soft gradients
* Easy-to-understand Flask backend

---

## 🛠️ Technologies Used

* Python 
* Flask 
* HTML/CSS (Responsive UI)
* Qiskit (Quantum backend simulation placeholder)



