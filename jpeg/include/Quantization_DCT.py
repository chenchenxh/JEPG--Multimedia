# coding=utf-8 
#DCT中的M和N参数，此处设置为8
MN = 8;
import math
from jpegMatrix import *
#常数C(u)的函数
def C(u, MN):
    return math.sqrt(1.0 / MN) if u == 0 else math.sqrt(2.0 / MN)

def DCT(matrix, DCT_matrix, MN):
    for u in range(0, MN):
        for v in range(0,MN):
            mid = 0
            for i in range(0 ,MN):
                for j in range(0, MN):
                    mid += math.cos((2*i+1)*u*math.pi/(2*MN)) * math.cos((2*j+1)*v*math.pi/(2*MN)) * matrix[i*MN+j]
            DCT_matrix.append(int(round(C(u,MN)*C(v,MN)*mid)))

#量化函数
def Luminance_Quantization(DCT_matrix, Quantization_DCT_matrix, MN):
    for i in range(0, MN*MN):
        Quantization_DCT_matrix.append(int(round(1.0 * DCT_matrix[i] / Luminance_Quantization_Matrix[i])))
def Chroma_Quantization(DCT_matrix, Quantization_DCT_matrix, MN):
    for i in range(0, MN*MN):
        Quantization_DCT_matrix.append(int(round(1.0 * DCT_matrix[i] / Chroma_Quantization_Matrix[i])))
#此函数实现两个过程，1调用DCT函数，2量化
def Quantization_DCT(matrix, DC_AC):
    #存储DCT矩阵
    DCT_matrix = []
    Quantization_DCT_matrix = []
    # for i in range(0, MN*MN):
    #     #矩阵每个值都减去128，整齐化
    #     matrix[i] = matrix[i] - 128
    #第一步：生成DCT矩阵
    DCT(matrix, DCT_matrix, MN)
    #量化,然后输出
    if DC_AC == 0:
        Luminance_Quantization(DCT_matrix, Quantization_DCT_matrix, MN)
    else:
        Chroma_Quantization(DCT_matrix, Quantization_DCT_matrix, MN)
    # 输出测试矩阵
    # print "test matrix:"
    # for i in range(0,MN*MN):
    #     if(i % MN != MN-1):
    #         print matrix[i],
    #     else:
    #         print matrix[i]

    # # 处理完输出DCT矩阵
    # print "DCT matrix:"
    # for i in range(0, MN*MN):
    #     if(i % MN != MN-1):
    #         print int(round(DCT_matrix[i])),
    #     else:
    #         print int(round(DCT_matrix[i]))

    # print "Quantization DCT matrix:"
    # for i in range(0, MN*MN):
    #     if(i % MN != MN-1):
    #         print Quantization_DCT_matrix[i],
    #     else:
    #         print Quantization_DCT_matrix[i]
    # return Quantization_DCT_matrix
    return DCT_matrix
def De_Luminance_Quantization(DCT_matrix, Quantization_DCT_matrix):
    for i in range(0, MN*MN):
        DCT_matrix.append(Quantization_DCT_matrix[i] * Luminance_Quantization_Matrix[i])
def De_Chroma_Quantization(DCT_matrix, Quantization_DCT_matrix):
    for i in range(0, MN*MN):
        DCT_matrix.append(Quantization_DCT_matrix[i] * Chroma_Quantization_Matrix[i])

def oneIDCT(array, i):
    mid = 0
    for u in range(0, MN):
        mid += math.cos((2*i+1) * u * math.pi / 16) * array[u] * C(u,MN)
    return mid

def De_DCT(DCT_matrix):
    temp_matrix = list(range(64))
    temp_matrix2 = list(range(64))
    #列IDCT求出temp_matrix
    for i in range(0, MN):
        array = []
        for j in range(0, MN):
            array.append(DCT_matrix[i + j*MN])
        for u in range(0, MN):
            temp_matrix[u*MN + i] = oneIDCT(array, u)
    #行IDCT求出temp_matrix2
    for i in range(0, MN):
        array = []
        for j in range(0, MN):
            array.append(temp_matrix[i*MN + j])
        for u in range(0, MN):
            temp_matrix2[i*MN + u] = (oneIDCT(array, u))
    return temp_matrix2

def De_Quantization_DCT(Quantization_DCT_matrix, DC_AC):
    #存储DCT矩阵
    DCT_matrix = []
    #第一步：生成DCT矩阵
    if DC_AC == 0:
        De_Luminance_Quantization(DCT_matrix, Quantization_DCT_matrix)
    else:
        De_Chroma_Quantization(DCT_matrix, Quantization_DCT_matrix)
    #反量化,然后输出
    matrix = []
    matrix = De_DCT(Quantization_DCT_matrix)
    for i in range(0, MN*MN):
        matrix[i] = int(round(matrix[i]))
    #输出测试矩阵
    # print "Quantization DCT matrix:"
    # for i in range(0, MN*MN):
    #     #矩阵每个值都减去128，整齐化
    #     # DCT_matrix[i] = matrix[i] - 128
    #     if(i % MN != MN-1):
    #         print Quantization_DCT_matrix[i],
    #     else:
    #         print Quantization_DCT_matrix[i]
    # # 处理完输出DCT矩阵
    # print "DCT matrix:"
    # for i in range(0, MN*MN):
    #     if(i % MN != MN-1):
    #         print DCT_matrix[i],
    #     else:
    #         print DCT_matrix[i]
    # print "matrix:"
    # for i in range(0,MN*MN):
    #     if(i % MN != MN-1):
    #         print matrix[i],
    #     else:
    #         print matrix[i]
    return matrix

def DCT_pre(little_matrix, length, DC_AC):
    mid_matrix = []
    DCT_flag = 0
    for i in range(0, length):
        DCT_flag+=1
        mid_matrix.append(Quantization_DCT(little_matrix[i], DC_AC))
    return mid_matrix
def De_DCT_pre(Quantization_DCT_matrix, length, DC_AC):
    mid_matrix = []
    DCT_flag = 0
    for i in range(0, length):
        DCT_flag+=1
        mid_matrix.append(De_Quantization_DCT(Quantization_DCT_matrix[i], DC_AC))
    return mid_matrix
