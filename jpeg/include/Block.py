# coding=utf-8 
#DCT中的M和N参数，此处设置为8
MN = 8;

def Block(matrix, sizeX,sizeY):
    little_matrix = []
    #start_point是每个8*8矩阵的第一个点
    for Y in range(0, sizeY / MN):
        for X in range(0, sizeX / MN):
            start_point = Y * sizeX * 8 + X * 8
            #初始化中间矩阵
            mid_matrix = []
            #生成中间矩阵
            for i in range(0, MN):
                for j in range(0, MN):
                    mid_matrix.append(matrix[start_point + i*sizeX + j])
            #压栈
            little_matrix.append(mid_matrix)
    return little_matrix

def De_Block(little_matrix, size):
    matrix = []
    for Y in range(0, size[1] / MN):
        for count1 in range(0, MN):
            for X in range(0, size[0] / MN):
                for count2 in range(0, MN):
                    if X+Y*(size[0]/MN) >= len(little_matrix):
                        print ("?0")
                    elif count2+count1*MN >= len(little_matrix[X+Y*(size[0]/MN)]):
                        print ("?1 %d %d %d %d %d %d" %(X,Y,count1, count2,count2+count1*MN, len(little_matrix[X+Y*(size[0]/MN)])))
                    matrix.append(little_matrix[X+Y*(size[0]/MN)][count2+count1*MN])
                    # matrix.append(count2 + X*MN + count1*MN*(size[0]/MN) + Y*MN*(size[0]/MN)*MN)
    return matrix
