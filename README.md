# Quantum Teleportation Project (QC-803)

This repository contains a **quantum teleportation simulation** implemented in Python using **Qiskit**, demonstrating teleportation of single-qubit states, noise effects, and state tomography.

---

## Project Structure

```
QC-803-Quantum-Teleportation/
├─ src/quantum_teleportation/
│  ├─ __init__.py
│  ├─ teleport.py           # Quantum teleportation circuits and feedforward
│  ├─ tomography.py         # Measurement, state reconstruction, and postselection
│  ├─ noise.py              # Noise models, Bell-pair degradation, and dephasing
│  ├─ visualization.py      # Plotting and visualization utilities
├─ examples/
│  ├─ complete_teleportation.py  # Full teleportation workflow with noise and plots
├─ pyproject.toml           # Project metadata for installation
├─ README.md
```

---

## Installation

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# .venv\Scripts\activate    # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install the package in editable mode:

```bash
pip install -e .
```

---

## Modules Overview

### `teleport.py`

* `prepare_state(circuit, qubit, theta, phi)` – Prepares a single-qubit state |ψ⟩ = cos(θ/2)|0⟩ + e^{iφ}sin(θ/2)|1⟩
* `generate_bell_pairs()` – Returns a Bell state circuit.
* `build_teleportation_circuit(theta, phi, bell_pairs=None)` – Builds the teleportation circuit with optional custom Bell pairs.
* `apply_feedforward(circuit, bob_qubit, a0_bit, a1_bit)` – Implements Bob’s feed-forward corrections based on Alice’s measurement.

### `tomography.py`

* `measure_in_basis(circuit, bob_qubit, bob_cbit, basis, backend)` – Measures Bob’s qubit in X, Y, or Z basis.
* `marginalize_to_bob(counts)` – Reduces multi-qubit counts to Bob’s qubit.
* `reconstruct_density(counts_x, counts_y, counts_z)` – Reconstructs Bob’s density matrix from measurement results.
* `tomography_after_feedforward(circuit, bob_qubit, bob_cbit, backend)` – Full tomography after feedforward.
* `tomography_postselected(circuit, bob_qubit, a0_bit, a1_bit, backend, outcome)` – Postselects on Alice’s measurement outcomes.

### `noise.py`

* `add_delay_with_dephasing(circuit, bob_qubit, delay_time, t2_time)` – Adds pure dephasing (via thermal relaxation) to simulate dephasing noise after delay.
* `bellpair_depolarizing_noise(p)` – Depolarizing noise on Bell pairs.
* `bellpair_amplitude_damping_noise(p)` – Amplitude damping noise on Bell pairs.
* `degrade_bell_pair(bell_pairs)` – Inserts identity gates to prepare Bell pairs for noise application.

### `visualization.py`

* `plot_circuit(qc, filename, title)` – Plots the quantum circuit.
* `plot_bloch_state(statevector, filename, title)` – Plots single-qubit Bloch sphere.
* `plot_postselected_bob_blochs(rho_post_dict)` – Plots Bob’s Bloch spheres for each postselected outcome.
* `plot_bob_histograms(counts_X, counts_Y, counts_Z, prefix)` – Plots histograms of Bob’s qubit measurement.
* `plot_dephasing_noise(fidelities, delay_times)` – Plots fidelity vs dephasing delay.
* `plot_bellpair_noise(fidelities_dict, ps)` – Plots fidelity vs Bell-pair noise strength.

---

## Example Workflow

Run the **complete teleportation simulation** with:

```bash
python examples/complete_teleportation.py
```

This script performs the following:

1. Builds the teleportation circuit for a given qubit state |ψ⟩
2. Plots Alice’s initial Bloch sphere and density matrix
3. Performs postselected tomography of Bob’s qubit
4. Applies feedforward corrections and plots Bob’s Bloch sphere
5. Adds **dephasing noise** during feedforward delays and plots fidelity vs delay
6. Applies **depolarizing and amplitude damping noise** on Bell pairs and analyzes teleportation fidelity
7. Saves all results (circuits, Bloch spheres, histograms) as PNG files

**Note:** For amplitude damping, fidelity shows a characteristic U-shaped curve for input states with θ = 0 or π.

---

## Example Plots

After running `complete_teleportation.py`, the following plots are generated:

| Plot                                | Description                         | Filename                                                        |
| ----------------------------------- | ----------------------------------- | --------------------------------------------------------------- |
| Alice’s initial state Bloch sphere  | Initial qubit                       | `alice_initial.png`                                             |
| Circuit till Bell measurement       | Circuit before Alice’s measurement  | `circuit_till_bell_measurement.png`                             |
| Circuit after feedforward           | Full teleportation with corrections | `circuit_after_feedforward.png`                                 |
| Bob’s final teleported Bloch sphere | State after feedforward corrections | `Bob_final.png`                                                 |
| Bob’s qubit histograms              | Measurement in X, Y, Z basis        | `bob_final_X.png`, `bob_final_Y.png`, `bob_final_Z.png`         |
| Postselected Bob Bloch spheres      | For Alice’s measurement outcomes    | `bob_bloch_post_00.png`, `bob_bloch_post_01.png`, etc.          |
| Fidelity vs dephasing               | Effect of feedforward delay         | `dephasing_fidelity.png`                                        |
| Fidelity vs Bell-pair noise         | Depolarizing / amplitude damping    | `bellpair_noise_fidelity.png`                                   |
| Bell pair distribution              | Effect of noise on Bell pairs       | `Bell_pair_Amplitude_Damping.png`, `Bell_pair_Depolarizing.png` |

---

## Requirements

* Python ≥ 3.10
* Qiskit ≥ 0.44
* NumPy, Matplotlib

---
