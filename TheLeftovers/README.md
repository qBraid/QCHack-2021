# Shor's Algorithm

Shor’s algorithm is famous for factoring integers in polynomial time. Since the best-known classical algorithm requires superpolynomial time to factor the product of two primes, the widely used cryptosystem, RSA, relies on factoring being impossible for large enough integers.

In 2001, Shor's algorithm was demonstrated by a group at IBM, who factored 15 into 3x5, using an NMR implementation of a quantum computer with 7 qubits. After IBM's implementation, two independent groups implemented Shor's algorithm using photonic qubits, emphasizing that multi-qubit entanglement was observed when running the Shor's algorithm circuits. In 2012, the factorization of 15 was performed with solid-state qubits.

The problem that we are trying to solve is, given a composite number N, to find a non-trivial divisor of N (a divisor strictly between 1 and N). Before attempting to find such a divisor, one can use relatively quick primality-testing algorithms to verify that N is indeed composite.

## What we added:

We upgraded the existing function to dynamically return a boolean whether the input number is a prime or not. This is run on the `qasm_simulator` with 1000 shots for better accuracy. The factorization is done by GCD to find the nearest factors to eliminate edge cases. We have edited it to a more understandable format with easy access and definite results.

## Contributors:

[Prashanth Umapathy](github.com/prashanth-up)

[Kashish Goel](https://github.com/kashish-goel)
