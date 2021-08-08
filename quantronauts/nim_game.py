import draw
import ia
import stats
from qiskit import Aer, QuantumCircuit, QuantumRegister, execute

# Init Qasm simulator backend
qasm = Aer.get_backend('qasm_simulator')
backend_sim = qasm

# Init game parameters
player1 = [False, "Player1"]
player2 = [False, "Player2"]

print("""
###################################################
# Welcome in the Quantum Nim Game - CLI
# Will you succeed to win against the Quantum AI ?
#
# Good Luck !!!
###################################################
""")

play = True

computer = [False, False]
nb_player = str(input("How many player ? 1/2 : "))
if nb_player == '1':
    computer[1] = True


begin = str(input("Player1 start ? y/n : "))
if begin == 'y':
    player1[0] = True
else:
    player2[0] = True
    computer[0] = True

while play:
    # Generation of the first circuit with 11 qubits
    stick = 11
    nb_qubit = stick
    drawing_add = ""
    draw.draw(stick, drawing_add)

    stick_qubit = QuantumRegister(nb_qubit, 'stick')
    qc_board = QuantumCircuit(stick_qubit)

    # Game
    while stick > 0:
        if player1[0]:
            player_name = player1[1]
        else:
            player_name = player2[1]

        # Player choice
        if computer[1] is False or player1[0] is True:
            print(player_name, "- You take : ")
            nbstick = int(input())
            for i in range(nbstick):
                print(player_name, "- Which gate do you want to use on stick[", i + 1, "] ?")
                if stick - i == 1 and nb_qubit == 1:
                    gate = str(input("x : "))
                elif stick - i == 1:
                    gate = str(input("x, cx : "))
                elif stick - i == nb_qubit:
                    gate = str(input("h, x : "))
                elif stick - i > 1:
                    gate = str(input("h, x, cx : "))

                if gate == 'h':
                    qc_board.h(stick - (1 + i))
                    drawing_add = "/ " + drawing_add
                if gate == 'x':
                    qc_board.x(stick - (1 + i))
                    drawing_add = ""
                if gate == 'cx':
                    qc_board.cx(stick - i, stick - (1 + i))
                    drawing_add = "¬ " + drawing_add

        # Computer choice
        if computer[0] is True and computer[1] is True:
            nbstick = 0
            if stick == 1:
                qc_board.x(stick - 1)
                drawing_add = ""
                nbstick = 1
            else:
                result_analyse = ia.quantum_ia(stick % 4, backend_sim)
                if result_analyse == 4:
                    for i in range(3):
                        qc_board.h(stick - (1 + i))
                        qc_board.cx(stick - i, stick - (1 + i))
                        qc_board.x(stick - (1 + i))
                        drawing_add = ""
                        nbstick = 3
                else:
                    for i in range(result_analyse):
                        qc_board.x(stick - (1 + i))
                    nbstick = result_analyse

        stick -= nbstick

        # Check if board is clean
        if stick < 1:
            # Run circuit
            qc_board.measure_all()
            print(qc_board.draw())
            job = execute(qc_board, backend_sim, shots=1, memory=True)
            result_memory = job.result().get_memory()
            result = result_memory[0]
            for i in range(len(result)):
                if result[i] == '0':
                    stick += 1
            print("stick left : ", stick)

            # Check circuit result
            if stick < 1:
                if player1[0]:
                    print("\n\n##################\n  Player 2 win !\n##################")
                if player2[0]:
                    stats.stats("human")
                    print("\n\n##################\n  Player 1 win !\n##################")
                if computer[0] is False and computer[1] is True:
                    stats.stats("robot")
                    print("\n\n##################\n  Machine win !\n##################")
            else:
                # Generation of new circuit with qubits left
                nb_qubit = stick
                drawing_add = ""
                stick_qubit = QuantumRegister(nb_qubit, 'stick')
                qc_board = QuantumCircuit(stick_qubit)

        # Inverse turn
        if stick > 0:
            draw.draw(stick, drawing_add)
            player2[0] = not player2[0]
            player1[0] = not player1[0]
            if computer[1]:
                computer[0] = not computer[0]

    # New game ?
    again = str(input("Play again ? (y/n) --> "))
    if again == 'n':
        play = False
    else:
        clear = "\n" * 10
        print(clear)
