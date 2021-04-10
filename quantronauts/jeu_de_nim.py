import draw
from qiskit import Aer, QuantumCircuit, QuantumRegister, execute

# Init Qasm simulator backend
qasm = Aer.get_backend('qasm_simulator')

backend_sim = qasm

player1 = [False, "Player1"]
player2 = [False, "Player2"]

play = True

begin = str(input("Player1 start ? y/n : "))
if begin == 'y':
    player1[0] = True
else:
    player2[0] = True

while play:
    stick = 3
    nb_qubit = stick
    draw.draw(stick)

    stick_qubit = QuantumRegister(nb_qubit, 'stick')
    qc_board = QuantumCircuit(stick_qubit)

    # Jeu
    while stick > 0:
        if player1[0]:
            player_name = player1[1]
        else:
            player_name = player2[1]

        print(player_name, "- You take : ")
        nbstick = int(input())
        lessstick = 0
        for i in range(nbstick):
            print(player_name, "- Which gate do you want to use on stick[", i+1, "] ?")
            if stick-lessstick == 1:
                gate = str(input("x : "))
            elif stick-lessstick == nb_qubit:
                gate = str(input("h, x : "))
            elif stick-lessstick > 1:
                gate = str(input("h, x, cx : "))

            if gate == 'h':
                qc_board.h(stick-(1+lessstick))
                lessstick += 1
            if gate == 'x':
                qc_board.x(stick-(1+lessstick))
                lessstick += 1
            if gate == 'cx':
                qc_board.cx(stick-i, stick-(1+i))
                lessstick += 1
        stick -= lessstick

        if stick < 1:
            qc_board.measure_all()
            print(qc_board.draw())
            job = execute(qc_board, backend_sim, shots=1, memory=True)
            result_memory = job.result().get_memory()
            result = result_memory[0]
            for i in range(len(result)-1):
                if result[i] == '0':
                    stick += 1
            print("stick left : ", stick)

            if stick < 1:
                if player1[0]:
                    print("\n\n##################\n  Player 2 win !\n##################")
                if player2[0]:
                    print("\n\n##################\n  Player 1 win !\n##################")
            else:
                nb_qubit = stick
                stick_qubit = QuantumRegister(nb_qubit, 'stick')
                qc_board = QuantumCircuit(stick_qubit)

        if stick > 0:
            draw.draw(stick)
            player2[0] = not player2[0]
            player1[0] = not player1[0]

    # Nouvelle partie ?
    again = str(input("Play again ? (y/n) --> "))
    if again == 'n':
        play = False
    else:
        clear = "\n" * 10
        print(clear)
