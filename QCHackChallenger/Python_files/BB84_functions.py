from qiskit import *
from numpy.random import randint, shuffle
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import numpy as np


def bit_string(n) :
    return randint(0, 2, n)


def encode_bits(bits, bases):
    l = len(bits)
    base_circuit = QuantumCircuit(l, l)
    for i in range(l):
        if bases[i] == 0:
            if bits[i] == 1:
                base_circuit.x(i)
        if bases[i] == 1:
            if bits[i] == 0:
                base_circuit.h(i)
            if bits[i] == 1:
                base_circuit.x(i)
                base_circuit.h(i)
    base_circuit.barrier()
    return base_circuit


def measure_bits(circuit, bases):
    backend = Aer.get_backend('qasm_simulator')
    for j in range(len(bases)):
        if bases[j] == 0:
            circuit.measure(j,j)
        if bases[j] == 1:
            circuit.h(j)
            circuit.measure(j,j)
    r = execute(circuit, backend, shots=1, memory = True).result().get_counts()
    return circuit, [int(ch) for ch in list(r.keys())[0]][::-1]


def agreed_bases(a, b):
    return [j for j in range(len(a)) if a[j] == b[j]]


def select_bits(bits, selection, choice):
    return [bits[i] for i in range(len(selection)) if selection[i] == choice]


def error_rate(atest, btest):
    W = len([j for j in range(len(atest)) if atest[j] != btest[j]])
    return W / len(atest)


def information_reconciliation(a, b):
    return a, b


def toeplitz(n, k, bits, seed):
    matrix = np.zeros((k, n), dtype = int)
    for i in range(k) :
        for j in range(n) :
            matrix[i,j] = seed[i - j + n - 1]
    key = np.matmul(matrix, np.transpose((np.array(bits))))
    return [bit%2 for bit in key]
