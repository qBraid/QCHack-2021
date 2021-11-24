import numpy as np
import math
import itertools
import qiskit
from qiskit import Aer, QuantumCircuit, execute, IBMQ, QuantumRegister, ClassicalRegister
from qiskit.algorithms import QAOA
from qiskit.utils import QuantumInstance, algorithm_globals
from qiskit.circuit.library import MCMT

from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.converters import QuadraticProgramToQubo


def quantum_ia(nb_stick: int, past: list, backend_sim: Aer) -> list:
	"""Quantum IA.
	Args:
		nb_stick: nb of stick left
		past: past turn
		backend_sim: backend for quantum
	Return: Prediction to use
	"""
	def quadratibot(nb_stick: int, past: list, backend_sim: Aer) -> list:
		"""Quadratic + QAOA function
		Args:
			nb_stick: nb of stick left
			past: past turn
			backend_sim: backend for quantum
		Return: Gates to use
		"""
		def get_quantum_solution_for(
		    quadprog: QuadraticProgram, quantumInstance: QuantumInstance, optimizer=None):
		    _eval_count = 0

		    def callback(eval_count, parameters, mean, std):
		        nonlocal _eval_count
		        _eval_count = eval_count
		    
		    # Create solver and optimizer
		    solver = QAOA(optimizer=optimizer, quantum_instance=quantumInstance, callback=callback,)

		    # Create optimizer for solver
		    optimizer = MinimumEigenOptimizer(solver)

		    # Get result from optimizer
		    result = optimizer.solve(quadprog)
		    return result, _eval_count


		# Check number of stick max
		if nb_stick >= 3:
		    max_stick = 3
		else:
		    max_stick = nb_stick

		# Check the past
		# |||||||| ## /¬/¬¬/
		past.reverse()
		poten_stick = nb_stick
		for i in range(len(past)):
		    if past[i] == "/":
		        poten_stick += 0.5
		    if past[i] == "¬":
		        u = 1
		        while past[i+u] == "¬":
		            u += 1
		        if past[i+u] == "/":
		            poten_stick += 0.5

		# Check last turn
		last_st = 0
		if past[0] == "¬":
		    u = 1
		    while past[0+u] == "¬":
		        u += 1
		        if past[0+u] == "/":
		            last_st = 0.5
		if past[0] == "/":
		        last_st = 0.5

		quadprog = QuadraticProgram(name="qnim")
		quadprog.integer_var(name="x", lowerbound=0, upperbound=max_stick)
		quadprog.integer_var(name="sup", lowerbound=0, upperbound=max_stick)
		quadprog.integer_var(name="intric", lowerbound=0, upperbound=max_stick)
		quadprog.maximize(
		    linear={"x":1, "sup":0.5, "intric":last_st},
		    quadratic={("sup", "intric"):0.5}
		)
		# General constraints
		quadprog.linear_constraint(linear={"x":1, "sup":1, "intric":1}, sense=">", rhs=0, name="gen_min")
		quadprog.linear_constraint(linear={"x":1, "sup":1, "intric":1}, sense="<=", rhs=max_stick, name="gen_max")

		#quadprog.quadratic_constraint(quadratic={("sup", "intric"):1, ("x", "sup"):1}, sense="<=", rhs=poten_stick%4-1, name=qvers)

		# Mod4 constraints
		if math.ceil(poten_stick%4)-1 > 0:
		    quadprog.linear_constraint(linear={"x":1, "sup":1}, sense="<=", rhs=math.ceil(poten_stick%4)-1, name="qua_mod4")
		if nb_stick%4-1 > 0:
		    quadprog.linear_constraint(linear={"x":1, "sup":1, "intric":1}, sense="<=", rhs=nb_stick%4-1, name="cla_mod4")

		# Get QAOA result
		final_result = []
		qaoa_result, qaoa_eval_count = get_quantum_solution_for(quadprog, simulator_instance)

		# Format and print result
		for cropHectares, cropName in zip(qaoa_result.x, qaoa_result.variable_names):
		    if cropHectares >= 1:
		        final_result.append(cropName)

		return final_result


	def gronim(output: list, backend_sim: Aer) -> list:
		"""Grover for best predict.
		Args:
			output: every possible prediction
			backend_sim: backend for quantum
		Return: best predict
		"""
		def diffuser(nqubits):
		    qc = QuantumCircuit(nqubits)
		    for qubit in range(nqubits):
		        qc.h(qubit)
		    for qubit in range(nqubits):
		        qc.x(qubit)
		    qc.h(nqubits - 1)
		    qc.mct(list(range(nqubits - 1)), nqubits - 1)
		    qc.h(nqubits - 1)
		    for qubit in range(nqubits):
		        qc.x(qubit)
		    for qubit in range(nqubits):
		        qc.h(qubit)
		    U_s = qc.to_gate()
		    U_s.name = "$Diff$"
		    return U_s


		def ram(nqubits, lists_final):
		    list_qram = [i for i in range(nqubits)]
		    qram = QuantumRegister(nqubits, 'qram')
		    qalgo = QuantumRegister(nqubits, 'algo')
		    qc = QuantumCircuit(qram, qalgo)
		    
		    control_h = MCMT('h',nqubits, 1).to_gate()
		    
		    map_ram_2 = [['x', 'x'], ['o', 'x'], ['x', 'o'], ['o', 'o']]
		    map_ram_3 = [['x', 'x', 'x'], ['o', 'x', 'x'], ['x', 'o', 'x'], ['o', 'o', 'x'], 
		                 ['x', 'x', 'o'], ['o', 'x', 'o'], ['x', 'o', 'o'], ['o', 'o', 'o']]
		    if len(bin(len(lists_final))[2:]) == 3:
		        map_ram = map_ram_3
		    if len(bin(len(lists_final))[2:]) == 2:
		        map_ram = map_ram_2
		    
		    for i, m_ram in zip(range(len(lists_final)), map_ram):
		        #qc.barrier()
		        for index, gate in enumerate(m_ram):
		            if gate == 'x':
		                qc.x(qram[index])
		        
		        if lists_final[i][0] == 'x' or lists_final[i][0] == 'sup':
		            qc.mcx(qram, qalgo[0])
		        else:
		            qc.append(control_h, [*list_qram, qalgo[0]])
		        
		        if len(lists_final[i]) == 3:
		            if lists_final[i][1] == 'x':
		                qc.mcx(qram, qalgo[1])
		            elif lists_final[i][1] == 'intric':
		                qc.mcx([qram[0], qram[1], qram[2], qalgo[0]], qalgo[1])
		            else:
		                qc.append(control_h, [*list_qram, qalgo[1]])
		            
		        if lists_final[i][-1] == 'x':
		            qc.mcx(qram, qalgo[-1])
		        elif lists_final[i][-1] == 'intric':
		            if len(lists_final[i]) == 3:
		                qc.mcx([qram[0], qram[1], qram[2], qalgo[1]], qalgo[-1])
		            else:
		                qc.mcx([qram[0], qram[1], qalgo[0]], qalgo[-1])
		        else:
		            qc.append(control_h, [*list_qram, qalgo[-1]])
		        
		        for index, gate in enumerate(m_ram):
		            if gate == 'x':
		                qc.x(qram[index])
    
		    #print(qc.draw())
		    U_s = qc.to_gate()
		    U_s.name = "$Qram$"
		    return U_s


		def algo(nqubits):
		    qc = QuantumCircuit(nqubits)
		    qc.h(0)
		    qc.x(0)
		    U_s = qc.to_gate()
		    U_s.name = "$Algo$"
		    return U_s


		lists_final = []
		lists_full = list(itertools.permutations(output, len(output)))
		for u in lists_full:
		    if u not in lists_final:
		        lists_final.append(u)

		len_qram = len(bin(len(lists_final))[2:])
		qram = QuantumRegister(len_qram, 'qram')
		qalgo = QuantumRegister(len_qram, 'algo')
		oracle = QuantumRegister(1, 'oracle')
		c = ClassicalRegister(len_qram, 'measurement')

		qc = QuantumCircuit(qram, qalgo, oracle, c)

		# Init
		qc.h(qram)
		qc.x(oracle)
		qc.h(oracle)
		qc.barrier()

		# Qram
		qc.append(ram(len_qram, lists_final), [*[i for i in range(len_qram*2)]])
		qc.barrier()
		# Algorithm
		qc.append(algo(len_qram), [*[i for i in range(len_qram, len_qram*2)]])
		qc.barrier()

		# Oracle
		qc.mcx([qalgo[0], qalgo[-1]], oracle)
		qc.barrier()

		# Revert Algo + Qram
		qc.append(algo(len_qram).inverse(), [*[i for i in range(len_qram, len_qram*2)]])
		qc.append(ram(len_qram, lists_final).inverse(), [*[i for i in range(len_qram*2)]])
		qc.barrier()

		# Diffuser
		qc.append(diffuser(len_qram), [*[i for i in range(len_qram)]])

		# Measure of the ouputs
		qc.barrier()
		qc.measure(qram, c)

		job = execute(qc, backend_sim, shots=512, memory=True)
		result_job = job.result()
		result_count = result_job.get_counts()
		result_memory = job.result().get_memory()

		if len(result_count) == 1:
		        final_result = int(result_memory[0], 2)
		else:
		    final_result = max(result_count, key=result_count.get)
		    final_result = int(final_result, 2)

		to_return = lists_final[final_result]

		return to_return


	output = quadratibot(nb_stick, past, backend_sim)
	if len(output) < 2:
		predict = output
	else:
		predict = gronim(output, backend_sim)

	return predict
