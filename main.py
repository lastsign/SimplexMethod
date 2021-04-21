import numpy as np
from scipy.optimize import linprog

"""
нужно указать путь до файла в котором будут такие данные
3
3
3 6 5 4 9 2 3 6 2
58 60 40
30 50 20
"""
# with open("untitled.txt", "r") as file:
#     n = file.readline()
#     m = file.readline()
#     c = np.array(file.readline().split(), float)
#     a = np.array(file.readline().split(), float)
#     b = np.array(file.readline().split(), float)
#     A_1 = [[1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1]]
#     b_1 = a
#     A_2 = [[1, 0, 0, 1, 0, 0, 1, 0, 0], [0, 1, 0, 0, 1, 0, 0, 1, 0], [0, 0, 1, 0, 0, 1, 0, 0, 1]]
#     b_2 = b
#     # print(A_2)
# print(c)
# res = linprog(c, A_1, b_1, A_2, b_2)
# print(res)
# P = np.dot(res.x, c)
# P1 = np.dot(c, res.x)
# stop = time.time()
# print("Time:", stop - start)

# print(res)


def check_delta(delta):
    for i in range(len(delta)):
        if delta[i] > 0:
            return 1
    return 0


def check_sb(sb, i):
    for j in range(len(sb)):
        if sb[j] == i:
            return 0
    return 1


def max_by_abc(delta, irrelevant, sb):
    max_on_j = 1
    len_d = len(delta) - 2
    for i in range(len_d):
        for j in range(len(irrelevant)):
            if delta[i + 2] == delta[irrelevant[j]]:
                return -1, irrelevant
            if delta[max_on_j] == delta[irrelevant[j]]:
                i += 1
                max_on_j += 1
        if i < len_d and max_on_j < len_d:
            if delta[max_on_j] <= delta[i + 2] and check_sb(sb, i + 2):
                        max_on_j = i + 2
    return max_on_j, irrelevant


def min_tetta(a, m, irrelevant, max_j, min_i):
    count = 0
    i = 0
    r_min = 0
    if max_j == 2:
        max_j = 2
    while i < m - 1:
        if a[i + 1][max_j] > 0 and a[min_i][max_j] > 0:
            r_min = min_i
            if a[i][0] / a[min_i][max_j] > a[i][0] / a[i + 1][max_j]:
                r_min = i + 1
            i += 1
        elif min_i < m and a[min_i][max_j] <= 0:
            min_i += 1
            count += 1
        else:
            count += 1
            i += 1
    if count == m:
        irrelevant.append(max_j)
        return r_min, irrelevant, -1
    return r_min, irrelevant, 0


def find_optimal_aij(delta, a, m, sb):
    irrelevant = []
    max_j, irrelevant = max_by_abc(delta, irrelevant, sb)
    if max_j == 2:
        max_j = 2
    min_i, irrelevant, f = min_tetta(a, m, irrelevant, max_j, min_i=0)
    while f < 0:
        max_j, irrelevant = max_by_abc(delta, irrelevant, sb)
        min_i, irrelevant, f = min_tetta(a, m, irrelevant, max_j, min_i=0)
    return max_j, min_i


def simplex_method():
    a = []
    with open("untitled.txt", "r") as file:
        n = int(file.readline())
        m = int(file.readline())
        c = np.array(file.readline().split(), float)
        for i in range(m):
            a.append(np.array(file.readline().split(), float))
        b = np.array(file.readline().split(), float)
    c = -c
    s = np.zeros((n + m + 1) * m).reshape(m, n + m + 1)
    s[0][5] = 1
    s[1][6] = 1
    s[2][7] = 1
    for i in range(m):
        for j in range(n):
            s[i][j + 1] += a[i][j]
        s[i][0] = b[i]
    a = s
    for i in range(m):
        a[i] = np.array(a[i])
    s = np.zeros(n + m)
    for j in range(n):
        s[j] = c[j]
    c = s
    s = np.zeros(n + m + 1)
    for j in range(n):
        s[j + 1] = c[j]
    cj = s
    sb = np.zeros(3, int)
    for i in range(m):
        sb[i] = i + 5
    bp = b
    delta = np.ones(m + n + 1)
    print(cj)
    print(a)
    while check_delta(delta):
        delta = np.zeros(m + n + 1)
        for j in range(m + n + 1):
            sum = 0
            for i in range(m):
                sum += cj[sb[i]] * a[i][j]
            delta[j] = sum - cj[j]
        if not check_delta(delta):
            break
        max_j, min_i = find_optimal_aij(delta, a, m, sb)
        if min_i == 1 and max_j == 2:
            min_i = 1
        a[min_i] = a[min_i] / a[min_i][max_j]
        for i in range(m):
            k = a[i][max_j]
            if i != min_i:
                a[i] -= (k * a[min_i])
        sb[min_i] = max_j
        for i in range(m):
            if a[i][0] < 0:
                print('degenerate solution')
                exit(0)
        print(sb)
        print(a)
        print(delta, delta[max_j], '\n')
        if min_i == 2:
            min_i = 2
        # print(sb)

    # print(a[0:1])
    # print(a[1:2])
    # print(a[2:])
    # print(a)


    answer = 0
    print(sb)
    print(delta)
    print(cj)
    for i in range(len(sb)):
        answer += a[i][0] * cj[sb[i]]
    print(answer)
    # print(-14./3.)

if __name__ == '__main__':
    simplex_method()
