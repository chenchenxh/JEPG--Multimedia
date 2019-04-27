# coding=utf-8 
def Sample(matrix, size):
    temp_matrix = []
    for Y in range(0, size[1] / 2):
        for X in range(0, size[0] / 2):
            start_point = Y * 2 * size[0] + X * 2
            temp_matrix.append(matrix[start_point])
    return temp_matrix

def De_Sample(matrix, size):
    temp_matrix = []
    for Y in range(0, size[1]):
        for i in range(0, 2):
            for X in range(0, size[0]):
                temp_matrix.append(matrix[X + Y*size[0]])
                temp_matrix.append(matrix[X + Y*size[0]])
    return temp_matrix