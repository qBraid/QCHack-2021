# The Ising Model
The Ising model describes a chain of spins that act like magnetic dipoles. The ferromagnetic interactions between neighboring spins create a system that tries to settle on the lowest energy state. Therefore, the energy of the system is described by a Hamiltonian.

## Transverse field Ising Model

[The transverse field Ising Model](https://en.wikipedia.org/wiki/Transverse-field_Ising_model) can be described by a two-state system where each state corresponds to the value of the spin. Due to non-commuting observables when the transverse field is introduced, a quantum approach is needed in order to calculate the Hamiltonian of the system. We can therefore match the number of the spins that create the Ising chain to qubits, and use a two-qubit circuit (since only two neighboring spins interact) to perform the non-commuting matrices calculations. Then the unitary matrix of the circuit is returned, that is used in the calculation of the Hamiltonian of the whole system, which looks like this

![Transverse Field Ising Model Hamiltonian Formula](https://i.imgur.com/7FKY93c.png)

Then we use the eigenvectors of the Hamiltonian to calculate the groundstate of the system, which can give a statevector that shows the probability of measuring the system in each one of the basic states.
The Hamiltonian is written as a function with input n, the number of spins or qubits and h, the strength of the transverse field. The strength of the transverse field is is important, because when looking at the formula of the Hamiltonian above, we can see that it controls how much “influence” the non-commuting factor has on the neighboring spins interactions. To test our algorithm, we run two extreme tests, one for h=0 which would give something that looks like 

![Classical Ising Model Hamiltonian Formula]( https://i.imgur.com/YonjrJO.png)

And is essentially the formula of the Hamiltonian for the Classical Ising model, since there is no transverse field. The second one is for h=100, in which the field is so strong that the neighboring spins interactions are negligible. The Hamiltonian in this case would look like

![Transverse Field Ising Model Hamiltonian Formula for h=100](https://i.imgur.com/pTnJc9n.png)

And the statevector would be in the equal superposition, because of interactions on the z axis being completely absent.

