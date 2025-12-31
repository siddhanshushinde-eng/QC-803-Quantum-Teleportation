from qiskit import transpile
from qiskit.quantum_info import DensityMatrix
from collections import Counter
import numpy as np

def measure_in_basis(circuit, bob_qubit, bob_cbit, basis, backend, shots=4096):
    qc_measure = circuit.copy()
    if basis == "X":
        qc_measure.h(bob_qubit)
    elif basis == "Y":
        qc_measure.sdg(bob_qubit)
        qc_measure.h(bob_qubit)
    qc_measure.measure(bob_qubit, bob_cbit)
    tqc = transpile(qc_measure, backend, optimization_level=0)
    job = backend.run(tqc, shots=shots)
    result = job.result()
    return result.get_counts()

def marginalize_to_bob(counts):
    reduced = Counter()
    for bitstring, count in counts.items():
        bits = bitstring.replace(" ", "")
        bob_val = bits[2]
        reduced[bob_val] += count
    return reduced

def reconstruct_density(counts_x, counts_y, counts_z):
    def expectation(counts):
        total = sum(counts.values())
        if total == 0:
            return 0.0
        return (counts.get("0", 0) - counts.get("1", 0)) / total
    ex = expectation(counts_x)
    ey = expectation(counts_y)
    ez = expectation(counts_z)
    r = np.array([ex, ey, ez])
    norm = np.linalg.norm(r)
    if norm > 1.0:
        r /= norm
    ex, ey, ez = r
    rho = 0.5 * np.array([[1 + ez, ex - 1j*ey], [ex + 1j*ey, 1 - ez]])
    return DensityMatrix(rho)

def tomography_after_feedforward(circuit, bob_qubit, bob_cbit, backend, shots=4096):
    counts_X_raw = measure_in_basis(circuit, bob_qubit, bob_cbit, "X", backend, shots)
    counts_Y_raw = measure_in_basis(circuit, bob_qubit, bob_cbit, "Y", backend, shots)
    counts_Z_raw = measure_in_basis(circuit, bob_qubit, bob_cbit, "Z", backend, shots)

    counts_X_bob = marginalize_to_bob(counts_X_raw)
    counts_Y_bob = marginalize_to_bob(counts_Y_raw)
    counts_Z_bob = marginalize_to_bob(counts_Z_raw)

    return reconstruct_density(counts_X_bob, counts_Y_bob, counts_Z_bob)

def tomography_postselected(circuit, bob_qubit, a0_bit, a1_bit, backend, shots=4096, outcome="00"):
    target_a0, target_a1 = int(outcome[0]), int(outcome[1])
    def select_bell_outcome(counts):
        selected = Counter()
        for bitstring, count in counts.items():
            bits = bitstring.replace(" ", "")
            bob_bit = bits[0]
            a0_val = int(bits[1])
            a1_val = int(bits[2])
            if a0_val == target_a0 and a1_val == target_a1:
                selected[bob_bit] += count
        return selected
    counts_x_raw = measure_in_basis(circuit, bob_qubit, 0, "X", backend, shots)
    counts_y_raw = measure_in_basis(circuit, bob_qubit, 0, "Y", backend, shots)
    counts_z_raw = measure_in_basis(circuit, bob_qubit, 0, "Z", backend, shots)
    counts_x_post = select_bell_outcome(counts_x_raw)
    counts_y_post = select_bell_outcome(counts_y_raw)
    counts_z_post = select_bell_outcome(counts_z_raw)
    return reconstruct_density(counts_x_post, counts_y_post, counts_z_post)
