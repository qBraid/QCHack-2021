from qiskit import *
import numpy as np

def Hamiltonian(n,h):
    qc = np.empty(2*n-1, dtype=object) 
    for i in range(0, 2*n-1): #2n-1 is the number of factors on the n-site Hamiltonian
        qr = QuantumRegister(n) 
        qc[i] = QuantumCircuit(qr) #create quantum circuits for each factor of the Hamiltonian
        #print(i)
        if (i<=n-2): #for the first sum of the Hamiltonian
            qc[i].z(i) #value of current spin
            qc[i].z(i+1) #and value of its neighboring spin
        else: #for the second sum of the Hamiltonian
            qc[i].x(2*n-2-i) #2*n-2 gives the proper index since counting starts at 0
            
    simulator = Aer.get_backend('unitary_simulator')
    result = np.empty(2*n-1, dtype=object) 
    unitary = np.empty(2*n-1, dtype=object) 
    Hamiltonian_Matrix=0
    for i in range(0, 2*n-1):
        result[i] = execute(qc[i], backend=simulator).result()
        unitary[i] = result[i].get_unitary()
        #print(unitary[i])
        if (i<=n-2):
            Hamiltonian_Matrix=np.add(Hamiltonian_Matrix,-unitary[i])
        else:
            Hamiltonian_Matrix=np.add(Hamiltonian_Matrix,-h*unitary[i])
    print(Hamiltonian_Matrix)
    
Hamiltonian(3,1)

