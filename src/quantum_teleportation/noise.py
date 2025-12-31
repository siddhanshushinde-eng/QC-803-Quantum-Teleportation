from qiskit_aer.noise import NoiseModel, phase_damping_error, depolarizing_error, amplitude_damping_error
from qiskit_aer import AerSimulator

from qiskit_aer.noise import NoiseModel, thermal_relaxation_error
from qiskit_aer import AerSimulator

def add_delay_with_dephasing(circuit, bob_qubit, delay_time, t2_time):
    if delay_time > 0:
        circuit.delay(delay_time, bob_qubit)
        circuit.barrier()

    noise_model = NoiseModel()

    dephase_error = thermal_relaxation_error(t1=float('inf'), t2=t2_time, time=delay_time)
    noise_model.add_all_qubit_quantum_error(dephase_error, ["delay"])
    backend = AerSimulator(noise_model=noise_model)

    return backend

def bellpair_depolarizing_noise(p):
    noise_model = NoiseModel()
    err = depolarizing_error(p, 1)
    noise_model.add_all_qubit_quantum_error(err, ["id"])
    return noise_model

def bellpair_amplitude_damping_noise(p):
    noise_model = NoiseModel()
    err = amplitude_damping_error(p)
    noise_model.add_all_qubit_quantum_error(err, ["id"])
    return noise_model

def degrade_bell_pair(bell_pairs):
    degraded = bell_pairs.copy()
    degraded.id(0)
    degraded.id(1)
    return degraded
