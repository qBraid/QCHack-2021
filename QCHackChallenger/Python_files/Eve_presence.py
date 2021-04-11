from qiskit import *
from numpy.random import randint, shuffle
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import numpy as np
from BB84_functions import *
from LDPC_functions import *


n, N = 648 ,2800
#if n == 648 or n == 50 :
#    MAX_ERROR_RATE = 1
#else :
MAX_ERROR_RATE = 1  
EMPTY = QuantumCircuit(N, N)
MAX_ITERS = 30


#All the Eve's information is stored using global variables
eve_bits = bit_string(N)
#encoded qubits


def eavesdropping(qubits, N) :
    #e = randint((2 * MAX_ERROR_RATE * N) // 100 + 1)
    e = int((2 * MAX_ERROR_RATE * N) // 100) + 1
    print("Induces errors : ", e)
    
    circ = qubits.copy()
    rand_pos = sorted(random.sample(range(N), e))
   
    #Eve measures selected signal with a randomly chosen basis
    for pos in rand_pos :
        random_gate = randint(2)
        if random_gate == 0:
            circ.measure(pos, pos)
        else :
            circ.h(pos)
            circ.measure(pos, pos)
    backend = Aer.get_backend('qasm_simulator')
    m = execute(circ, backend, shots=1, memory = True).result().get_counts()
    bits = [int(ch) for ch in list(m.keys())[0]][::-1]
    
    for pos in rand_pos :
        eve_bits[pos] = bits[pos]
    
    return circ


def QCC(qubits, N) :
    attack = randint(2)
    return eavesdropping(qubits, N) if attack else EMPTY
    #return eavesdropping(qubits, N)


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
    received_encode = QCC(alice_encode, N)
    
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
    a2b = CAC(alice_bases)
    b2a = CAC(bob_bases)

    #Step 9 - Alice and Bob discard all the bits that correspond to disagreed bases
    agreed_base_indices = agreed_bases(alice_bases, bob_bases)
    #bob_circuit.draw(output = 'mpl')
    
    return bob_bits, agreed_base_indices


def qber(alice_bits, bob_bits, agreed_base_indices) :
    #Step 10 - Error rate checking 
    S2T = bit_string(len(agreed_base_indices))
    T = select_bits(agreed_base_indices, S2T, 0)

    #Step 11 - Alice tells T to Bob over CAC
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


def reconciliation(alice_bits, bob_bits, qber) :
    p = qber
    n = len(alice_bits)
    #Step1 : Produce parity check matrix(M1) of dimension m*n, n is length of bitstring and m is no. of parity check equations
    H, m = parity_matrix(n, p)

    #Step2 : Alice produces the syndrome and hash values
    C = syndrome(H, alice_bits)

    #Step3 : Alice sends syndrome via CAC

    #Step4 : Bob produces the syndrome
    D = syndrome(H, bob_bits)

    #Step5 : Alice performs belief propagation algorithm
    y, success, i = belief_prop(C, D, bob_bits, MAX_ITERS, p, H)
    
    #Step6 : Bob sends success of reconciliation
    
    return y, success


def privacy_amplification(alice_pseudokey, bob_pseudokey) :
    n, k = len(alice_pseudokey), len(alice_pseudokey) // 2
    seed = bit_string(n + k - 1)
    alice_key = toeplitz(n, k, alice_pseudokey, seed)
    bob_key = toeplitz(n, k, bob_pseudokey, seed)
    return alice_key, bob_key, error_rate(alice_key, bob_key)


alice_bits, alice_bases, bob_bases, received_encode, received = generate_and_send(N)
if not received :
    print('Abort : Eve is imitating Bob')

else:
    #Step 7 to Step 9
    bob_bits, agreed_base_indices = sifting(alice_bases, bob_bases, received_encode)
    
    
    #Step 10 to Step 13
    error, S2T = qber(alice_bits, bob_bits, agreed_base_indices)
    print("QBER : ", error)
    
    #Step 14 - Alice and Bob check over a threshold for error before proceeding ahead
    if error > 0.03 :
        print ("Abort : Eavesdropping detected")
    
    else :
        #Step 15 - Alice and Bob generate their pseudo keys
        SminusT = select_bits(agreed_base_indices, S2T, 1)
        alice_pseudokey, bob_pseudokey = [], []
        for i in SminusT :
            alice_pseudokey.append(alice_bits[i])
            bob_pseudokey.append(bob_bits[i])
        
        if error != 0 :
            #Step 16 - Information Reconciliation
            if 648 <= len(alice_pseudokey) <= 700 :
                alice_pseudokey = alice_pseudokey[:648]
                bob_pseudokey = bob_pseudokey[:648]
            bob_corrected_key, success = reconciliation(alice_pseudokey, bob_pseudokey, error) if error != 0 else (bob_pseudokey, 1)
        
            if not success :
                print("Abort : Reconcilation not succeeded")
        
            else :
                #Step 17 - alice and bob perform privacy amplification
                alice_key, bob_key, error = privacy_amplification(alice_pseudokey, bob_corrected_key)
                print("Alice's key : ", alice_key)
                print("Bob's key : ", bob_key)
                print("Final error rate in Bob's key : ", error)
            
    
        else :
            #Step 17 - alice and bob perform privacy amplification
            alice_key, bob_key, error = privacy_amplification(alice_pseudokey, bob_pseudokey)
            print("Alice's key : ", alice_key)
            print("Bob's key : ", bob_key)
            print("Final error rate in Bob's key : ", error)
