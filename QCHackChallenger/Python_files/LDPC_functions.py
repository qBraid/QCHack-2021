import numpy as np
from math import exp, log
from numpy.random import randint
import random


def quasi_cyclic(n) :
    if n == 648 :
        I = np.eye(27, dtype = int)
        O = np.zeros((27, 27), dtype = int)
        Is = [np.roll(I, -p, 0) for p in range(27)]
        H = np.block([[Is[0], O, O, O, Is[0], Is[0], O, O, Is[0], O, O, Is[0], Is[1], Is[0], O, O, O, O, O, O, O, O, O, O], 
                     [Is[22], Is[0], O, O, Is[17], O, Is[0], Is[0], Is[12], O, O, O, O, Is[0], Is[0], O, O, O, O, O, O, O, O, O],
                     [Is[6], O, Is[0], O, Is[10], O, O, O, Is[24], O, Is[0], O, O, O, Is[0], Is[0], O, O, O, O, O, O, O, O],
                     [Is[2], O, O, Is[0], Is[20], O, O ,O, Is[25], Is[0], O, O, O, O, O, Is[0], Is[0], O, O, O, O, O, O, O],
                     [Is[23], O, O, O, Is[3], O, O, O, Is[0], O, Is[7], Is[11], O, O, O, O, Is[0], Is[0], O, O, O, O, O, O],
                     [Is[24], O, Is[23], Is[1], Is[17], O, Is[3], O, Is[10], O, O, O, O, O, O, O, O, Is[0], Is[0], O, O, O, O, O],
                     [Is[25], O, O, O, Is[8], O, O, O, Is[7], Is[18], O, O, O, O, O, O, O, O, Is[0], Is[0], O, O, O, O],
                     [Is[13], Is[24], O, Is[16], Is[0], O, Is[8], O, Is[6], O, O, O, O, O, O, O, O, O, O, Is[0], Is[0], O, O, O],
                     [Is[7], Is[20], O, O, Is[22], Is[10], O, O, Is[23], O, O, O, O, O, O, O, O, O, O, O, Is[0], Is[0], O, O],
                     [Is[11], O, O, O, Is[19], O, O, O, Is[13], O, Is[3], Is[17], O, O, O, O, O, O, O, O, O, Is[0], Is[0], O],
                     [Is[25], O, Is[8], O, Is[23], Is[18], O, Is[14], Is[9], O, O, O, O, O, O, O, O, O, O, O, O, O, Is[0], Is[0]],
                     [Is[3], O, O, O, Is[16], O, O, Is[2], Is[25], Is[5], O, O, O, O, O, O, O, O, O, O, O, O, O, Is[0]]])
    if n== 50 :
        I = np.eye(5, dtype = int)
        O = np.zeros((5, 5), dtype = int)
        Is = [np.roll(I, p, 1) for p in range(5)]
        H = np.block([[Is[3], Is[1], Is[2], Is[4], Is[0], O, O, O, O, O],
                      [Is[2], O, Is[2], O, Is[1], Is[0], O, O, O, O],
                      [Is[1], Is[0], Is[4], Is[3], O, Is[2], Is[4], O, O, O],
                      [Is[0], Is[2], O, Is[1], Is[3], Is[0], Is[1], Is[2], O, O],
                      [Is[1], O, Is[3], O, Is[0], O, O, Is[3], Is[1], O],
                      [Is[3], Is[1], Is[4], Is[0], O, Is[3], O, Is[0], O, Is[1]]])
    return H


def build_regular_matrix(m, n) :
    if n <= 100 :
        col = 4
    elif n <= 200 :
        col = 5
    elif n <= 300 :
        col = 6
    elif n <= 400 :
        col = 7
    elif n <= 500 :
        col = 8
    elif n <= 600 :
        col = 9
    else :
        col = 10
    row = col * (n // m) 
    cols_cnt = [0 for _ in range(n)]
    H = np.zeros((m, n), dtype = int)
    
    for i in range(m) :
        indices = random.sample(range(n), row)
        for index in indices :
            j = index
            while (cols_cnt[j] > col - 1) :
                j = (j + 1) % n
            cols_cnt[j] += 1
            H[i, j] = 1
    return H


def build_irregular_matrix(m, n) :
    cols = randint(4, 8, n)
    rows = randint(5, 10, m)
    cols_cnt = [0 for _ in range(n)]
    H = np.zeros((m, n), dtype = int)
    
    for i in range(m) :
        indices = randint(0, n, rows[i])
        for index in indices :
            j = index
            while (cols_cnt[j] > cols[j] - 1) :
                j = (j + 1) % n
            cols_cnt[j] += 1
            H[i, j] = 1
    return H


def parity_matrix(n, p, regular = True) :
    if n == 648 :
        return quasi_cyclic(n), 324
    
    if p <= 0.02 :
        m = n // 5
    elif p <= 0.04 :
        m = n // 3
    elif p <= 0.08 :
        m = n // 2
    else :
        m = 2 * n // 3
    
    if regular :
        H = build_regular_matrix(m, n)
    else :
        H = build_irregular_matrix(m, n)
    return H, m


def lookup_tables(H, m, n, k) :
    LL_index = []
    LL_groups = 0
    
    for row in np.transpose(H) :
        LL_index.append(LL_groups)
        LL_groups += sum(row)
    LL_index.append(k)
    
    cs_index = []
    cs_groups = 0
    
    for row in H :
        cs_index.append(cs_groups)
        cs_groups += sum(row)
    cs_index.append(k)
    
    cs_list = []
    bit_cs = [0 for _ in range(n)]
    
    for row in range(m) :
        for bit in range(n) :
            if H[row, bit] == 1 :
                cs_list.append([bit, LL_index[bit] + bit_cs[bit]])
                bit_cs[bit] += 1           
    
    return np.array(LL_index), np.array(cs_index), np.array(cs_list)


def non_zeros(M) :
    return sum([sum(row) for row in M])


def syndrome(M1, x) :
    return [i % 2 for i in np.matmul(M1, np.transpose(np.array(x)))]


def LL_init(k, p) :
    LL_reg = []
    f_init = (1-p)/p
    a_init = (1 - 2 * p)
    
    for i in range(k) :
        LL_reg.append(a_init)
    
    return f_init, LL_reg


def cs_msgs_2_bits(m, d, cs_index, cs_list, LL_reg) : 
    for i in range(m) :
        alpha = (-1) ** (d[i])
        j1 = cs_index[i]
        j2 = cs_index[i + 1]
        
        for j in range(j1, j2) :
            a1 = LL_reg[cs_list[j][1]]
            alpha *= a1 
        
        if 0 > alpha > -0.0001 :
            alpha = -0.0001
        
        if 0.0001 > alpha >= 0 :
            alpha = 0.0001
        
        for j in range(j1, j2) :
            a1 = LL_reg[cs_list[j][1]]
            f = (a1 + alpha) / (a1 - alpha)
            
            if f < 0.001 :
                f = 0.001
            if 0.999 < f < 1.0 :
                f = 0.999
            if 1.0 <= f < 1.0001 :
                f = 1.001
            if f > 1000 :
                f = 1000
            LL_reg[cs_list[j][1]] = f
    
    return LL_reg


def bit_msgs_2_cs(n, LL_reg, LL_index, f_init, y) :
    y1 = []
    for i in range(n) :
        j1, j2 = LL_index[i], LL_index[i + 1]
        f_tot = f_init
        
        for j in range(j1, j2) :
            f = LL_reg[j]
            f_tot *= f
            
        for j in range(j1, j2) :
            f = f_tot - LL_reg[j]
            a = (f_tot - f) / (f_tot + f)
            
            if a < 0 :
                if a > -0.001 :
                    a = -0.001
                if a < -0.999 :
                    a = -0.999
            else :
                if a < 0.001 :
                    a = 0.001
                if a > 0.999 :
                    a = 0.999
            LL_reg[j] = a
        
        if f_tot < 1.0 :
            y1.append(1 - y[i])
        else : 
            y1.append(y[i])
    
    return y1, LL_reg


def converged(m, cs_index, cs_list, C, y) :
    success = 1
    for i in range(m) :
        chksum = 0
        j1, j2 = cs_index[i], cs_index[i + 1]
        
        for j in range(j1, j2) :
            chksum = chksum ^ y[cs_list[j][0]]
        
        if chksum != C[i] :
            success = 0
    
    return success


def belief_prop(C, D, y, MAX_ITERS, p, H) :
    m, n, k = len(H), len(H[0]), non_zeros(H)
    f_init, LL_reg = LL_init(k, p)
    LL_index, cs_index, cs_list = lookup_tables(H, m, n, k)
    d = [C[i] ^ D[i] for i in range(len(C))]
    
    success = 0
    i = 0
    while (i < MAX_ITERS) :
        LL_reg = cs_msgs_2_bits(m, d, cs_index, cs_list, LL_reg)
        y, LL_reg = bit_msgs_2_cs(n, LL_reg, LL_index, f_init, y)
        success = converged(m, cs_index, cs_list, C, y)
        i += 1
        if success == 1 : 
            break
    
    return y, success, i
