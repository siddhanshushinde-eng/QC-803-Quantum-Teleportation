from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def prepare_state(circuit: QuantumCircuit, qubit, theta, phi):
    circuit.ry(theta, qubit)
    circuit.rz(phi, qubit)

def generate_bell_pairs():
    bell = QuantumCircuit(2)
    bell.h(0)
    bell.cx(0, 1)
    return bell

def build_teleportation_circuit(theta, phi, bell_pairs=None):
    q_in    = QuantumRegister(1, "psi")
    q_alice = QuantumRegister(1, "Bell pair_Alice")
    q_bob   = QuantumRegister(1, "Bell pair _Bob")
    c_bob   = ClassicalRegister(1, "c_bob")
    c_a0    = ClassicalRegister(1, "c_a0")
    c_a1    = ClassicalRegister(1, "c_a1")
    qc = QuantumCircuit(q_in, q_alice, q_bob, c_bob, c_a0, c_a1)
    prepare_state(qc, q_in[0], theta, phi)
    qc.barrier()
    
    if bell_pairs is None:
        bell_pairs = generate_bell_pairs()

    #If bell_pairs are provided, then compose
    qc = qc.compose(bell_pairs, qubits=[1, 2])
    qc.barrier()

    qc.cx(q_in[0], q_alice[0])
    qc.h(q_in[0])
    qc.measure(q_in[0], c_a0[0])
    qc.measure(q_alice[0], c_a1[0])
    qc.barrier()
    return qc, q_bob[0], c_a0[0], c_a1[0], c_bob[0]

def apply_feedforward(circuit: QuantumCircuit, bob_qubit, a0_bit, a1_bit):
    with circuit.if_test((a0_bit, 1)):
        circuit.z(bob_qubit)
    with circuit.if_test((a1_bit, 1)):
        circuit.x(bob_qubit)
    circuit.barrier()
