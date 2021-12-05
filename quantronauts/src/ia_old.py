from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer


def quantum_ia(sticks_root: int, backend_sim: Aer) -> int:
    """Grover.
    Args:
        sticks_root: past
        backend_sim: backend for quantum
    Return: Gate to use
    """

    def diffuser(qc: QuantumCircuit):
        qc.h(qram_q)
        qc.z(qram_q)
        qc.cz(qram_q[0], qram_q[1])
        qc.h(qram_q)

    def qram(qc: QuantumCircuit):
        # 01
        qc.x(qram_q[0])
        qc.ccx(qram_q[0], qram_q[1], sticks_q[0])
        qc.x(qram_q[0])
        # 10
        qc.x(qram_q[1])
        qc.ccx(qram_q[0], qram_q[1], sticks_q[0])
        qc.ccx(qram_q[0], qram_q[1], sticks_q[1])
        qc.x(qram_q[1])
        # 11
        qc.ccx(qram_q[0], qram_q[1], sticks_q[0])
        qc.ccx(qram_q[0], qram_q[1], sticks_q[1])
        qc.ccx(qram_q[0], qram_q[1], sticks_q[2])

    qram_q = QuantumRegister(2, "possibility")
    sticks_q = QuantumRegister(4, "sticks")
    out_q = QuantumRegister(1, "flag")
    c = ClassicalRegister(2, "c")
    qc = QuantumCircuit(qram_q, sticks_q, out_q, c)

    qc.h(qram_q)
    qc.x(out_q)
    qc.h(out_q)
    qc.barrier()

    for i in range(1):
        # Compute
        # Init board
        if sticks_root == 0:
            qc.x(sticks_q[3])
        for v in range(sticks_root):
            qc.x(sticks_q[sticks_root - v])
        # Qram
        qram(qc)

        # Flag
        qc.mcx(sticks_q, out_q)

        # Uncompute
        # Qram
        qram(qc)
        # Init board
        if sticks_root == 0:
            qc.x(sticks_q[3])
        for v in range(sticks_root):
            qc.x(sticks_q[sticks_root - v])

        # Apply generic diffuser
        diffuser(qc)

    qc.measure(qram_q, c)
    # Interprete result
    job = execute(qc, backend_sim, shots=512, memory=True)
    result_job = job.result().get_counts()
    result_memory = job.result().get_memory()
    # print("Memory ", result_memory)
    if len(result_job) == 1:
        to_return = int(result_memory[0], 2)
        # print("Return : ", to_return)
    else:
        to_return = 4

    return to_return
