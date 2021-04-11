# Qchack 2021 qBraid Challenge | Stanford x Yale 

This is a submission from Team 33 for the qBraid Challenge that is based on Google Cirq Challenge at QC Hack 2021 by Stanford and Yale University

Team members:

Ryan hill @ryanhill1
Mathias Goncalves @mtgo007
Vishal Sharathchandra Bajpe @mrvee-qC
For our project we adapted, modified, and refactored non-optimal functionality from the quantum_decomp open-source library. This library approximately implements the two-level decomposition procedures specified in [1] via a modulare, object-oriented approach. Its implementation decomposes a unitary through creation and manipulation of global gate objects using external scripts. Their procedure contains bugs, and when it executes, produces non-optimal solutions. We adapted stand-alone functions from their procedure to more closely implement [1] in a scripted approach that depends only on the NumPy and Math libaries. We then completely reworked conversion of the resulting two-level decomposition to cirq in a way that vastly reduces the number of CNOT gates and ultimately gives a near-optimal solution in the form of quantum operations. Our project represents a comprehensive refactorization and optimization (and debug) of selected functionality from the quantum_decomp code base, along with orignial matrix to quantum circuit translation in cirq.

Papers referenced for the solution:
[1] Decomposition of unitary matrices and quantum gates C.K. Li, R. Roberts, X. Yin, 2013.
[2] Decomposition of unitary matrix into quantum gates D. Fedoriaka, 2019.
[3] Efficient decomposition of unitary matrices in quantum circuit compilers A. M. Krol, A. Sarkar, I. Ashraf, Z. Al-Ars, K. Bertels, 2021.
