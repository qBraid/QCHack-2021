import draw
from qiskit import Aer, QuantumCircuit, QuantumRegister, execute

# Init Qasm simulator backend
qasm = Aer.get_backend('qasm_simulator')

backend_sim = qasm

# Init game parameters
player1 = [False, "Player1"]
player2 = [False, "Player2"]

play = True

begin = str(input("Player1 start ? y/n : "))
if begin == 'y':
    player1[0] = True
else:
    player2[0] = True

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
        
        # Rule choice
        print(player_name, "- You take : ")
        nbstick = int(input())
        for i in range(nbstick):
            print(player_name, "- Which gate do you want to use on stick[", i+1, "] ?")
            if stick-i == 1 and nb_qubit == 1:
                gate = str(input("x : "))
            elif stick-i == 1:
                gate = str(input("x, cx : "))
            elif stick-i == nb_qubit:
                gate = str(input("h, x : "))
            elif stick-i > 1:
                gate = str(input("h, x, cx : "))

            if gate == 'h':
                qc_board.h(stick-(1+i))
                drawing_add = "/ " + drawing_add
            if gate == 'x':
                qc_board.x(stick-(1+i))
                drawing_add = ""
            if gate == 'cx':
                qc_board.cx(stick-i, stick-(1+i))
                drawing_add = "¬ " + drawing_add
        stick -= nbstick
        
        # Check if board is clean
        if stick < 1:
            # Run circuit
            qc_board.measure_all()
            print(qc_board.draw())
            job = execute(qc_board, backend_sim, shots=1, memory=True)
            result_memory = job.result().get_memory()
            result = result_memory[0]
            print("Result : ", result)
            for i in range(len(result)):
                print("[", i, "]:", result[i])
                if result[i] == '0':
                    stick += 1
            print("stick left : ", stick)
            
            # Check circuit result
            if stick < 1:
                if player1[0]:
                    print("\n\n##################\n  Player 2 win !\n##################")
                if player2[0]:
                    print("\n\n##################\n  Player 1 win !\n##################")
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

    # New game ?
    again = str(input("Play again ? (y/n) --> "))
    if again == 'n':
        play = False
    else:
        clear = "\n" * 10
        print(clear)
