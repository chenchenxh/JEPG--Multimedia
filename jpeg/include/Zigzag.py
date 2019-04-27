# coding=utf-8
#DCT中的M和N参数，此处设置为8
MN = 8;
def In_Range(x, y):
    if x < 0 or y < 0 or x >= MN or y >= MN:
        return False
    else:
        return True

#对矩阵进行Zigzag扫描并返回
def Zigzag(matrix, ZIGZAG_trans_matrix):
    Zigzag_matrix = []
    i = 0
    j = 0
    #move_flag为0代表ij向右上移动，1代表向左下移动
    move_flag = 0
    Zigzag_matrix.append(matrix[0])
    for count in range(0, MN*MN-1):
        #求出i和j，i为横轴，j为纵轴
        if move_flag == 0:
            if In_Range(i+1, j-1):
                i = i+1
                j = j-1
            elif In_Range(i+1, j):
                i = i+1
                move_flag = 1
            elif In_Range(i, j+1):
                j = j+1
                move_flag = 1
        elif move_flag == 1:
            if In_Range(i-1, j+1):
                i = i-1
                j = j+1
            elif In_Range(i, j+1):
                j = j+1
                move_flag = 0
            elif In_Range(i+1, j):
                i = i+1
                move_flag = 0
        if len(ZIGZAG_trans_matrix)!= 64:
            ZIGZAG_trans_matrix.append(j*MN + i)
        Zigzag_matrix.append(matrix[j*MN + i])
    return Zigzag_matrix
def De_Zigzag(Zigzag_little_matrix,ZIGZAG_trans_matrix):
    mid_matrix = []
    if len(Zigzag_little_matrix)!= 64:
        print (len(Zigzag_little_matrix))
    for j in range(0, len(Zigzag_little_matrix)):
        for k in range(0, len(ZIGZAG_trans_matrix)):
            if ZIGZAG_trans_matrix[k] == j:
                # print j
                mid_matrix.append(Zigzag_little_matrix[k])
    if len(mid_matrix) != 64:
        print ("error")
        print (mid_matrix)
    return mid_matrix
