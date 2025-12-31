# Standard imports
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Qiskit imports
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import DensityMatrix, Statevector, state_fidelity
from qiskit.visualization import plot_histogram
# Noise model imports
from qiskit_aer.noise import NoiseModel, phase_damping_error, depolarizing_error, amplitude_damping_error

# Import your modules from src
from quantum_teleportation.teleport import prepare_state, generate_bell_pairs, build_teleportation_circuit, apply_feedforward
from quantum_teleportation.tomography import tomography_after_feedforward, tomography_postselected, marginalize_to_bob, measure_in_basis
from quantum_teleportation.noise import add_delay_with_dephasing, bellpair_depolarizing_noise, bellpair_amplitude_damping_noise, degrade_bell_pair
from quantum_teleportation.visualization import (
    plot_circuit, plot_bloch_state, plot_postselected_bob_blochs, plot_bob_histograms,
    plot_dephasing_noise, plot_bellpair_noise
)

# 0️⃣ Parameters
theta, phi = np.pi / 3, np.pi / 2
backend = AerSimulator(shots=5000)

# 1️⃣ Build teleportation circuit
qc, bob_qubit, a0_bit, a1_bit, bob_bit = build_teleportation_circuit(theta, phi)

# 2️⃣ Circuit till Bell measurement
plot_circuit(qc, "circuit_till_bell_measurement.png", title="Circuit till Bell measurement")

# 3️⃣ Alice initial state Bloch sphere and Density matrix
alice_state = Statevector.from_label("0")
qc_alice = QuantumCircuit(1)
prepare_state(qc_alice, 0, theta, phi)
alice_state = alice_state.evolve(qc_alice)
rho_alice = DensityMatrix(alice_state)
print("Alice's Density Matrix:\n")
print(rho_alice)
plot_bloch_state(alice_state.data, "alice_initial.png", title="Alice's initial state")

# 4️⃣ Bob postselected Bloch spheres
rho_posts = {outcome: tomography_postselected(qc, bob_qubit, a0_bit, a1_bit, backend, outcome=outcome)
             for outcome in ["00","01","10","11"]}
plot_postselected_bob_blochs(rho_posts)

# 5️⃣ Circuit after feed-forward
qc_ff = qc.copy()
apply_feedforward(qc_ff, bob_qubit, a0_bit, a1_bit)
plot_circuit(qc_ff, "circuit_after_feedforward.png", title="Circuit after feed-forward")

# 6️⃣ Bob final histograms
counts_X = measure_in_basis(qc_ff, bob_qubit, bob_bit, "X", backend)
counts_Y = measure_in_basis(qc_ff, bob_qubit, bob_bit, "Y", backend)
counts_Z = measure_in_basis(qc_ff, bob_qubit, bob_bit, "Z", backend)
counts_X_bob = marginalize_to_bob(counts_X)
counts_Y_bob = marginalize_to_bob(counts_Y)
counts_Z_bob = marginalize_to_bob(counts_Z)
plot_bob_histograms(counts_X_bob, counts_Y_bob, counts_Z_bob, prefix="bob_final")

# 7️⃣ Bob's qubit Bloch sphere after feed forward corrections

rho_bob = tomography_after_feedforward(qc_ff, bob_qubit, bob_bit, backend)
print("Bob's Density Matrix:\n")
print(rho_bob)
plot_bloch_state(rho_bob, "Bob_final.png", title="Bob's teleported state")

# 8️⃣ Dephasing noise fidelity graphs
delay_times = np.linspace(0, 1000, 13)
fidelities_relax = []
T2 = 150.0 

for tau in delay_times:
    qc_tmp, bob, a0, a1, bob_cbit = build_teleportation_circuit(theta, phi)

    # Add delay + dephasing noise on ALL qubits
    backend_noise = add_delay_with_dephasing(qc_tmp, bob_qubit=bob, delay_time=int(tau), t2_time=T2)

    # Apply feedforward
    apply_feedforward(qc_tmp, bob, a0, a1)
    rho_bob = tomography_after_feedforward(qc_tmp, bob, bob_cbit, backend_noise)

    # Fidelity with ideal teleported state
    rho_ideal = DensityMatrix(alice_state)
    fid = state_fidelity(rho_bob, rho_ideal)
    fidelities_relax.append(fid)
plot_dephasing_noise(fidelities_relax, delay_times)

# 9️⃣ Effect of depolarizing and amplitude damping on bell pair
noise_models = [("Amplitude Damping", bellpair_amplitude_damping_noise),("Depolarizing", bellpair_depolarizing_noise)]

p = 1  # Noise probability

for label, noise_fn in noise_models:
    # Generate and degrade Bell pair
    bell = generate_bell_pairs()
    degraded_bell = degrade_bell_pair(bell)
    degraded_bell.measure_all()

    # Apply noise model
    noise_model = noise_fn(p)
    backend = AerSimulator(noise_model=noise_model)

    # Transpile and run
    tqc = transpile(degraded_bell, backend, optimization_level=0)
    result = backend.run(tqc, shots=2000).result()
    counts = result.get_counts()
    fig = plot_histogram(counts)
    fig.savefig(f"Bell_pair_{label.replace(' ', '_')}.png", dpi=300, bbox_inches='tight')

# 🔟 Depolarizind and amplitude damping noise fidelity graphs
ps = np.linspace(0, 1, 11)
fidelities_dict = {"depolarizing": [], "amplitude_damping": []}

for noise_type in ["depolarizing", "amplitude_damping"]:
    for p in ps:
        # Generate ideal Bell pair
        bell = generate_bell_pairs()
        degraded_bell = degrade_bell_pair(bell)

        if noise_type == "depolarizing":
            noise_model = bellpair_depolarizing_noise(p)
        else:
            noise_model = bellpair_amplitude_damping_noise(p)

        qc_tmp, bob, a0, a1, bob_cbit = build_teleportation_circuit(theta, phi, bell_pairs=degraded_bell)
        apply_feedforward(qc_tmp, bob, a0, a1)

        backend = AerSimulator(noise_model=noise_model)
        rho_bob = tomography_after_feedforward(qc_tmp, bob, bob_cbit, backend)

        rho_ideal = DensityMatrix(alice_state)
        fid = state_fidelity(rho_bob, rho_ideal)
        fidelities_dict[noise_type].append(fid)
plot_bellpair_noise(fidelities_dict, ps)

print("✅ Complete teleportation example run finished! All visualizations generated.")