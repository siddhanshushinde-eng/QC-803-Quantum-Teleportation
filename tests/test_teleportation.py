import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, state_fidelity
from quantum_teleportation.teleport import prepare_state, build_teleportation_circuit, apply_feedforward
from quantum_teleportation.tomography import tomography_after_feedforward
from qiskit_aer import AerSimulator

backend = AerSimulator(shots=1000)  # smaller shots for tests

def test_prepare_and_teleport():
    theta, phi = 0.5, 1.0
    qc, bob_qubit, a0_bit, a1_bit, bob_cbit = build_teleportation_circuit(theta, phi)
    apply_feedforward(qc, bob_qubit, a0_bit, a1_bit)
    
    # Perform tomography to get Bob's final state
    rho_bob = tomography_after_feedforward(qc, bob_qubit, bob_cbit, backend, shots=1000)
    
    # Build the ideal statevector for Alice's initial qubit
    qc_alice = QuantumCircuit(1)
    prepare_state(qc_alice, 0, theta, phi)
    ideal_state = Statevector.from_label("0").evolve(qc_alice)

    # Now compute fidelity with Bob's density matrix
    fid = state_fidelity(rho_bob, ideal_state)
    # Fidelity should be high
    assert fid > 0.9
