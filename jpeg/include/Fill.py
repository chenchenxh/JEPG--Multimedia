# coding=utf-8 
def fill(matrix, size,newsize):
    newsize0 = size[0]
    newsize1 = size[1]
    fill_size1 = size[1]%16
    if fill_size1 != 0:
        newsize1 = size[1]+16-fill_size1

    fill_size0 = size[0]%16
    if fill_size0 != 0:
        newsize0 = size[0]+16-fill_size0
    newsize[0] = newsize0
    newsize[1] = newsize1
    new_matrix = []
    for i in range(0, newsize1):
        for j in range(0, newsize0):
            if i < size[1] and j < size[0]:
                new_matrix.append(matrix[i*size[0] + j])
            # elif i < size[1] and j >= size[0]:
            #     new_matrix.append(matrix[(i+1)*size[0]-1])
            # elif i >= size[1] and j < size[0]:
            #     new_matrix.append(matrix[(size[1]-2)*(size[0]-1) + j])
            # elif i >= size[1] and j >= size[0]:
            #     new_matrix.append(matrix[(size[1]-1) * (size[0] - 1)])
            else:
                new_matrix.append(0)
    return new_matrix

def De_fill(matrix, size):
    newsize0 = size[0]
    newsize1 = size[1]
    fill_size1 = size[1]%16
    if fill_size1 != 0:
        newsize1 = size[1]+16-fill_size1

    fill_size0 = size[0]%16
    if fill_size0 != 0:
        newsize0 = size[0]+16-fill_size0
    new_matrix = []
    # print newsize0,newsize1
    # print size
    for i in range(0, newsize1):
        for j in range(0, newsize0):
            if i < size[1] and j < size[0]:
                # if j == size[0]-1:
                #     print j,matrix[i*newsize0 +j]
                # if j == size[0]-2:
                #     print j,matrix[i*newsize0 +j]
                new_matrix.append(matrix[i*newsize0 + j])
    return new_matrix
