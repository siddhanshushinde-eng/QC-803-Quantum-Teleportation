import matplotlib.pyplot as plt
from qiskit.visualization import plot_bloch_multivector, plot_histogram

def plot_circuit(qc, filename, title="Quantum Circuit"):
    fig = qc.draw(output='mpl')
    fig.suptitle(title)
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close(fig)

def plot_bloch_state(statevector, filename, title="Bloch Sphere"):
    fig = plot_bloch_multivector(statevector)
    fig.suptitle(title)
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close(fig)

def plot_postselected_bob_blochs(rho_post_dict):
    for outcome, rho in rho_post_dict.items():
        fig = plot_bloch_state(rho.data, f"bob_bloch_post_{outcome}.png", f"Bob's Bloch - Postselected {outcome}")

def plot_bob_histograms(counts_X, counts_Y, counts_Z, prefix="bob_final"):
    for counts, basis in zip([counts_X, counts_Y, counts_Z], ["X","Y","Z"]):
        fig = plot_histogram(counts, title=f"Bob's qubit - {basis} basis")
        fig.savefig(f"{prefix}_{basis}.png", dpi=300, bbox_inches='tight')
        plt.close(fig)

def plot_dephasing_noise(fidelities, ps):
    plt.figure()
    plt.plot(ps, fidelities, marker='o')
    plt.xlabel("Dephasing probability p during delay")
    plt.ylabel("Teleportation fidelity")
    plt.title("Effect of dephasing noise during feed-forward delay")
    plt.grid(True)
    plt.ylim(0, 1.05)
    plt.savefig("dephasing_fidelity.png", dpi=300, bbox_inches='tight')
    plt.close()

def plot_bellpair_noise(fidelities_dict, ps):
    plt.figure()
    for noise_type, fidelities in fidelities_dict.items():
        plt.plot(ps, fidelities, marker='o', label=noise_type)
    plt.xlabel("Noise strength p on Bell pair + input qubit")
    plt.ylabel("Teleportation fidelity")
    plt.title("Effect of Bell-pair + input noise on teleportation fidelity")
    plt.legend()
    plt.grid(True)
    plt.ylim(0, 1.05)
    plt.savefig("bellpair_noise_fidelity.png", dpi=300, bbox_inches='tight')
    plt.close()
