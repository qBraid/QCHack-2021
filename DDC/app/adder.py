from numpy import pi
from qiskit import (Aer, ClassicalRegister, QuantumCircuit, QuantumRegister,
                    assemble, transpile)
from qiskit.visualization import plot_bloch_vector, plot_histogram


def binarize(num):
    return bin(num)[2:]


def bit_length_init(*num):
    bit_lenght = 0
    for n in num:
        bit_lenght = max(bit_lenght, len(binarize(n)))
    return bit_lenght


def create_register(*num):
    length = bit_length_init(*num)

    params = []
    params.append(QuantumRegister(length + int((len(num) + 1) / 2), 'qr'))
    params.append(ClassicalRegister(length + int((len(num) + 1) / 2), 'c'))
    for i in range(len(num)):
        params.append(QuantumRegister(length, 'q{}'.format(i)))
    return tuple(params)


def init_circuit(*num):
    params = create_register(*num)
    print(params)
    return QuantumCircuit(*params)


def adder(*num):
    qr, c, q1, q2 = create_register(*num)
    qc = init_circuit(*num)

    init_1 = [0 for _ in range(2**len(q1))]
    init_2 = [0 for _ in range(2**len(q1))]
    init_1[num[0]] = 1
    init_2[num[1]] = 1

    qc.initialize(init_1, q1)
    qc.initialize(init_2, q2)

    for i in range(len(q1)):
        qc.cx(q1[i], qr[i])
        qc.cx(q2[i], qr[i])
        qc.toffoli(q1[i], q2[i], qr[i + 1])

    qc.measure(qr, c)
    return qc


def simulate(qc):
    simulator = Aer.get_backend('aer_simulator')
    qc = transpile(qc, simulator)

    # Run and get counts
    result = simulator.run(qc).result()
    counts = result.get_counts(qc)
    plot_histogram(counts,
                   title='Bell-State counts',
                   number_to_keep=len(counts))
    return counts