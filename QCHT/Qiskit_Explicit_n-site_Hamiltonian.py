from qiskit import *
import numpy as np

def Hamiltonian(n,h):
    pow_n=2**n
    qc = np.empty(2*n-1, dtype=object)
    #Creating the quantum circuits that are used in the calculation of the Hamiltonian based on the number of qubits
    for i in range(0, 2*n-1): #2n-1 is the number of factors on the n-site Hamiltonian
        qr = QuantumRegister(n) 
        qc[i] = QuantumCircuit(qr) #create quantum circuits for each factor of the Hamiltonian
        #print(i)
        if (i<=n-2): #for the first sum of the Hamiltonian
            qc[i].z(i) #value of current spin
            qc[i].z(i+1) #and value of its neighboring spin
        else: #for the second sum of the Hamiltonian
            qc[i].x(2*n-2-i) #2*n-2 gives the proper index since counting starts at 0
    #Run each circuit in the simulator        
    simulator = Aer.get_backend('unitary_simulator')
    result = np.empty(2*n-1, dtype=object) 
    unitary = np.empty(2*n-1, dtype=object) 
    Hamiltonian_Matrix=0
    #Get the results for each circuit in unitary form
    for i in range(0, 2*n-1):
        result[i] = execute(qc[i], backend=simulator).result()
        unitary[i] = result[i].get_unitary()
        #print(unitary[i])
        #And calculate the Hamiltonian matrix according to the formula
        if (i<=n-2):
            Hamiltonian_Matrix=np.add(Hamiltonian_Matrix,-unitary[i])
        else:
            Hamiltonian_Matrix=np.add(Hamiltonian_Matrix,-h*unitary[i])
    print("The",pow_n,"x",pow_n, "Hamiltonian Matrix is:")
    print(Hamiltonian_Matrix)
    #Now that we have the Hamiltonian
    
    #find the eigenvalues and eigenvectors
    w, v = np.linalg.eig(Hamiltonian_Matrix)
    #first column of the eigenvectors is the groundstate of the system
    groundstate = v[:,1]
    #the probability to measure each basic state of n qubits
    probability = np.square(groundstate).real
    print("The probability for each of the",pow_n,"base states is:")
    print(probability)
    print("The probabilities for each of the",pow_n,"base states add up to:")
    print ("%.2f" % np.sum(probability))
    
Hamiltonian(8,1)

#To test the algorithm, we should run the Hamiltonian for the two extreme cases where h=0 and h>>1, h being the intensity of the transverse field (check readme for math details)

#for h=0, the transverse field is completely gone and therefore there is 100% chance that we measure the spin were all spins point down (basis state)
print("The Hamiltonian for h=0 is")
Hamiltonian(8,0)
#as described by the results, the probability matrix has 0 all its elements, except one

#for h=100 the transverse field is strong enough to push every spin into equal superposition, meaning that there is an equal probability to measure the system in each one of the basic states
print("The Hamiltonian for h=100 is")
Hamiltonian(8,100)
#as described by the results, the probability matrix elements are very close in value
