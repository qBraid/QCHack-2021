# Modular Arithmetic and Shor's Algorithm Implementation
## Laura Lewis

## Motivation
In this project, my goal mainly was to provide fully general implementations of modular arithmetic circuits in Cirq, which can further be easily translated to Qiskit. I've found that modular arithmetic can be an extremely useful tool in implementing several quantum algorithms, including Shor's algorithm. However, I've found that Cirq and Qiskit do not have built-in functionality to support these operations yet, causing quantum developers to have to implement them from scratch if they want to use them. Hence, my project was an attempt to fill this gap and additionally to program Shor's algorithm as an application. The qBraid challenge was a great opportunity for this, especially in the introduction of code snippets to the Learn interface. I hope that my project could add to these code snippets and allow developers to use modular arithmetic circuits more easily.

Another big motivation behind this project was that, as reading through Shor's algorithm in the Qiskit textbook, although it works, I wanted to see a general algorithm fully programmed out. This is especially relvant, as in the Qiskit textbook, the modular arithmetic circuit is hard-coded in. Despite the decrease in depth that this may allow, I think it is important to have a general implementation available as well.

## Description
My references for this project (as referenced throughout the project notebook as well) are the following:

https://arxiv.org/pdf/quant-ph/9508027.pdf<br/>
https://arxiv.org/pdf/quant-ph/0205095.pdf<br/>
https://qiskit.org/textbook/ch-algorithms/shor.html<br/>
https://qiskit.org/textbook/ch-algorithms/quantum-fourier-transform.html<br/>
https://qiskit.org/textbook/ch-algorithms/quantum-phase-estimation.html<br/>

I heavily followed this second link (linked in the Qiskit textbook for Shor's algorithm as well) in my implementation of the modular arithmetic circuits. As stated before, in this project, I provide general modular arithmetic circuits, where the modulus can be any positive integer. The circuits can be greatly simplified for a modulus that is a power of two, but I have not included those here for sake of generality. I applied these circuits to a Shor's algorithm implementation. Although this implementation is far from optimal with high depth and many qubits, with some further work, it can be polished and keep this generality that I was searching for.
