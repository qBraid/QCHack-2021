from qiskit import *
from numpy.random import randint, shuffle
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import numpy as np
from BB84_functions import *

n, N = 1000, 4200
EMPTY = QuantumCircuit(N, N)

def QCC(qubits) :
    return qubits


def CAC(bits) :
    return bits


def generate_and_send(N) :
    #Step 1 - Alice generates bits
    alice_bits = bit_string(N)

    #Step 2 - Alice generates the bases string
    alice_bases = bit_string(N)

    #Step 3 - Bob generates the bases string
    bob_bases = bit_string(N)
    
    #Step 4 - Alice encodes her bits in the chosen bases 
    alice_encode = encode_bits(alice_bits, alice_bases)

    #Step 5 - Alice sends her encoded bits to Bob and Eve tries to intercept over the Quantum channel
    received_encode = QCC(alice_encode)
    
    #Step 6 - Bob announces that he has received the encoding and measured it over CAC
    if received_encode == EMPTY :
        received = False
    else :
        received = True

    
    return alice_bits, alice_bases, bob_bases, received_encode, received


def sifting(alice_bases, bob_bases, received_encode) :
    #Step 7 - Bob measures Alice's bits in the chosen bases
    bob_circuit, bob_bits = measure_bits(received_encode, bob_bases)

    #Step 8 - Alice and Bob exchange their bases over CAC
    r2s = CAC(alice_bases)
    s2r = CAC(bob_bases)

    #Step 9 - Alice and Bob discard all the bits that correspond to disagreed bases
    agreed_base_indices = agreed_bases(alice_bases, bob_bases)
    #bob_circuit.draw(output = 'mpl')
    
    return bob_bits, agreed_base_indices


def qber(alice_bits, bob_bits, agreed_base_indices) :
    #Step 10 - Error rate checking 
    S2T = bit_string(len(agreed_base_indices))
    T = select_bits(agreed_base_indices, S2T, 0)

    #Step 11 - Alice tells T to bob over CAC
    bob_T = CAC(T)

    #Step 12 - Alice and Bob generate their test bits 
    alice_test_bits, bob_test_bits = [], []
    for i in T :
        alice_test_bits.append(alice_bits[i])
        bob_test_bits.append(bob_bits[i])

    #Step 12 - Alice and Bob announce their test bits to each other over the CAC
    rec_bob_test_bits = CAC(bob_test_bits)
    rec_alice_test_bits = CAC(alice_test_bits)

    #Step 13 - Alice and Bob compute the error rate
    error = error_rate(rec_alice_test_bits, rec_bob_test_bits)
    return error, S2T


def privacy_amplification(alice_pseudokey, bob_pseudokey) :
    n, k = len(alice_pseudokey), len(alice_pseudokey) // 2
    seed = bit_string(n + k - 1)
    alice_key = toeplitz(n, k, alice_pseudokey, seed)
    bob_key = toeplitz(n, k, bob_pseudokey, seed)
    return alice_key, bob_key, error_rate(alice_key, bob_key)


#Step 1 to Step 6
alice_bits, alice_bases, bob_bases, received_encode, received = generate_and_send(N)

if not received :
    print('Abort : Have not received qubits')

else :
    #Step 7 to Step 9
    bob_bits, agreed_base_indices = sifting(alice_bases, bob_bases, received_encode)

    #Step 10 to Step 13
    error, S2T = qber(alice_bits, bob_bits, agreed_base_indices)
    
    #Step 14 - Alice and Bob check over a threshold for error before proceeding ahead
    if error != 0 :
        print ("Abort")
    
    else :
        #Step 15 - Alice and Bob generate their pseudo keys
        SminusT = select_bits(agreed_base_indices, S2T, 1)
        alice_pseudokey, bob_pseudokey = [], []
        for i in SminusT :
            alice_pseudokey.append(alice_bits[i])
            bob_pseudokey.append(bob_bits[i])
        
        #Reconciliation not required
        
        #Step 16 - Alice and Bob perform privacy amplification (is not necessary in such an ideal condition)
        alice_key, bob_key, error = privacy_amplification(alice_pseudokey, bob_pseudokey)
        
        print("Alice's key : ", alice_key)
        print("Bob's key : ", bob_key)
        print("Final error rate in Bob's key : ", error)
