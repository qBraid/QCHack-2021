from qiskit import Aer
from src.main import battle
from stats.data import stats


class Game:
    def __init__(self):
        """Game begins."""
        # Init Qasm simulator backend
        qasm = Aer.get_backend("qasm_simulator")
        backend_sim = qasm

        # Init game parameters
        player1 = [False, "Player1"]
        player2 = [False, "Player2"]

        print(
            """
###################################################
# Welcome in the Quantum Nim Game - CLI
# Will you succeed to win against the Quantum AI ?
#
# Good Luck !!!
###################################################
        """
        )

        winner, looser = battle(player1, player2, backend_sim)

        stats(winner)

        print("The game is over !")
        actualize = str(input("Push enter to auto F5 the page") or "42")
