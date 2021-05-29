from multiprocessing import Process, Manager
import numpy as np


""" Написать программу, перемножающую две матрицы поэлементно. 
Элементы матрицы-произведения должны вычисляться в несколько потоков.
Сама генерирует матрицы, записывает в файл, считывает и записывает результат перемножения в другой файл"""


def matrix_multi(A, B, i, j, k, manager_list):
    global result
    multi = A[i][k] * B[k][j]
    manager_list.append(multi)
    print(A[i][k], B[k][j])

def matrix_random(nrows, ncols):
    a = np.random.randint(100, size=(nrows, ncols))
    return a

def write_matrix(path, matrix):
    with open(path, "wt") as file:
        for row in matrix:
            file.write(" ".join(str(item) for item in row) + "\n")

def read_matrix(path):
    return [[int(token) for token in row.split()]  for row in open(path) if row.strip()]

if __name__ == '__main__':

    #Записываю каждый раз новые матрицы
    m1 = matrix_random(2, 3)
    m2 = matrix_random(3, 2)
    write_matrix("matrix1.txt", m1)
    write_matrix("matrix2.txt", m2)

    M_A = read_matrix("matrix1.txt")
    M_B = read_matrix("matrix2.txt")


    manager = Manager()
    manager = manager.list()
    result = []
    for i in range(len(M_A)):
        for j in range(len(M_B[0])):
            for k in range(len(M_A[0])):
                p1 = Process(target=matrix_multi, args=(M_A, M_B, i, j, k, manager))
                p1.start()
                p1.join()
    manager_sort = [sum(manager[i: i + len(M_A[0])]) for i in range(0, len(manager), len(M_A[0]))]
    M_A = [manager_sort[i: i + len(M_A)] for i in range(0, len(manager_sort), len(M_A))]
    write_matrix("matrix_result.txt", M_A) #записываю результат в файл


