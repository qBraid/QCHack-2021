# **BB84 Protocol**
#### **A simulation of the first Quantum Key Distribution Protocol**

The BB84 Protocol was proposed by Bennett and Brassard in 1984. It is a method for producing a private key <br> to be further used in one-time pad encryption.

### **Description**

The protocol is comprised of four main stages :

- **Stage 1** is where the transmission of randomly encoded qubits occurs over the lossy quantum channel and <br> also the measurement of these qubits by the receiver

- **Stage 2** involves exchange of information over the classical channel between the parties to *sift* their bits <br> sequences to achieve a common sequence to work with but the sequence may have some errors

- **Stage 3** is where the parties exchange information over the classical channel to reconcile, correct errors, <br> between their bit sequences without exposing the value of their bits

- **Stage 4** is where the parties privacy amplify their now identical bit sequences to shrink the possible exposed <br> information over the quantum channel and the classical channel to almost zero, yielding a securely shared secret key.

### **The Implementation**

The project uses Qiskit and Python as the major frameworks. The first two stages involve the building of quantum <br> circuits for the qubits and their encoding in a particular basis using **Qiskit**. In stage 3 which is "Information Reconciliation", <br> we adapted the **Low Density Parity Check** (LDPC)  forward error correction algorithm. We used some standard matrices <br> for the purpose defined by the IEEE standards organizations. The final stage, "Privacy Amplification" is implemented using <br> family of two universal hash functions. Here we used the **Toeplitz matrices**.

### **A peek into the Directory**

We have demonstrated the Key-Distribution Protocol in three different scenarios :
- An ideal case where the channels are assumed to be noise-free and there is no eavesdropping
- A case with noisy channels and without eavesdropping
- A practical case with noisy channels and eavesdropping

Each scenario in the folder can be executed given the "Functions" directory which includes all the required functions. <br>  Both the Jupyter Notebooks and Python files are present. The technical requirements are the installation of Qiskit and Python.

### **Team Members**

Lakshika Rathi, IIT Delhi & Shreya Ilindra, IIT Bombay
