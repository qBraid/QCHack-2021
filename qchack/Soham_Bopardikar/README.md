GUESS THE NUMBER
I have made this project with the help of Qiskit and qBraid.

-->The Bernstein-Vazirani Algorithm : Let's say if you were given an n-digit number inside a black box. Our classical computers would take a maximum of n attempts to guess the correct number. So, the time complexity of the classical computer is O(n). But, quantum computers with the help of this algorithm can guess the answer correctly in one shot. Time complexity of quantum computer O(1).

-->Based on quantum interference : Bernstein-Vazirani (BV) is a great example for illustrating the power of constructive and destructive interference in quantum algorithms. In my project the correct guess of the number is analogous to constructive interference and the wrong guess of the number is analogous to destructive interference. 

-->Why do we use this algorithm ? The Bernstein Vazirani algorithm is one of the several algorithms that have proven that quantum computers surpass classical computers in certain domains. Although it is an algorithm with no applications thought of at the moment, this is the first step to surpass classical computers in certain aspects.

-->How will we use it ? In order to implement this algorithm, we will ask a user to enter a decimal number. After entering, the decimal number is converted to a binary number for the algorithm to function. The quantum computer undergoes a number of gate operations and finally recognizes the number and return's the number in binary form. This binary number is converted to decimal and the user number is guessed correctly.

-->Role of classical bits : To convey the measurements of the quantum operations in a classical computer.


-->Applications - There was a research paper which explains how the Bernstein Vazirani Algorithm can be used to attack block ciphers. Basic games like Quantum-Man (Quantum Hangman) can be created.


-->A unique example to understand the algorithm : Alice challenges Bob for a number guessing game. Alice has a number in her mind. Now, Bob's job is too use the right approach to guess Alice's number. If Bob uses the Bernstein Vazirani algorithm he will never get a wrong answer.