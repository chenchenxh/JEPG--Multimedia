# coding=utf-8 
#有两个数学模块math和cmath，第一个模块允许您访问实数的双曲线，三角函数和对数函数，而后者允许您使用复数。
from PIL import Image
import imageio
import math
import numpy as np
from include.Fill import *
from include.Block import *
from include.Quantization_DCT import *
from include.Sample import *
from include.Shang_coding import *
from include.Zigzag import *
#DCT中的M和N参数，此处设置为8
MN = 8;
#Zigzag置换表
ZIGZAG_trans_matrix = [0]

def test_main():
    #读取文件
    print("Please input the picture name:")
    pic = raw_input()
    print ("Reading image %s ... " %(str(pic)+".jpg"))
    image = Image.open(str(pic) + ".jpg")
    size = image.size
    #编码，得到YUV三个压缩编码数据流
    # (Y_coding_str, U_coding_str, V_coding_str) = encode(image)
    #用来存储YUV三个表
    Y_matrix = []
    U_matrix = []
    V_matrix = []
    #由每个像素点的RGB生成每个像素点的YUV,将RGB表转换成YUV三个matrix
    for i in range(0, size[0]):
        for j in range(0, size[1]):
            pixel = image.getpixel((i, j))
            Y_matrix.append(0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2])
            U_matrix.append(-0.1687*pixel[0] - 0.3313*pixel[1] + 0.5*pixel[2] + 128)
            V_matrix.append(0.5*pixel[0] - 0.419*pixel[1] - 0.081*pixel[2]+128)
    #填充
    print ("Fill...")
    newsize = [0, 0]
    Y_matrix = fill(Y_matrix, size, newsize)
    U_matrix = fill(U_matrix, size, newsize)
    V_matrix = fill(V_matrix, size, newsize)
    newsize2 = newsize
    #采样，此处使用的比例是4:1:1
    # newsize2 = [newsize[0]/2,newsize[1]/2]
    # print "Sample..."
    # U_matrix = Sample(U_matrix,newsize)
    # V_matrix = Sample(V_matrix,newsize)
    print ("Block...")
    Y_little_matrix = Block(Y_matrix,newsize[0],newsize[1])
    U_little_matrix = Block(U_matrix,newsize2[0],newsize2[1])
    V_little_matrix = Block(V_matrix,newsize2[0],newsize2[1])

    #每个块进行DCT和量化处理，最后的参数0代表亮度，1代表色度
    print ("Quantization and DCT...")
    Y_little_matrix = DCT_pre(Y_little_matrix, len(Y_little_matrix), 0)
    U_little_matrix = DCT_pre(U_little_matrix, len(U_little_matrix), 1)
    V_little_matrix = DCT_pre(V_little_matrix, len(V_little_matrix), 1)

    #DC的DPCM编码，AC的游长编码
    #先进行Zigzag扫描排序
    print ("Zigzag sort...")
    Zigzag_Y_little_matrix = []
    Zigzag_U_little_matrix = []
    Zigzag_V_little_matrix = []
    for i in range(0, len(Y_little_matrix)):
        Zigzag_Y_little_matrix.append(Zigzag(Y_little_matrix[i], ZIGZAG_trans_matrix))
    for i in range(0, len(U_little_matrix)):
        Zigzag_U_little_matrix.append(Zigzag(U_little_matrix[i], ZIGZAG_trans_matrix))
    for i in range(0, len(V_little_matrix)):
        Zigzag_V_little_matrix.append(Zigzag(V_little_matrix[i], ZIGZAG_trans_matrix))

    #DC,AC系数编码,处理Zigzag_Y_little_matrix[i],mid_matrix存储中间矩阵
    #bianma_matrix存储DC的差值（0，差值）和AC（RUNLENGTH，VALUE）键值对
    print ("DC and AC coding...")
    Y_bianma_matrix = []
    U_bianma_matrix = []
    V_bianma_matrix = []
    DC_and_AC_coding(Y_bianma_matrix, Zigzag_Y_little_matrix, len(Zigzag_Y_little_matrix))
    DC_and_AC_coding(U_bianma_matrix, Zigzag_U_little_matrix, len(Zigzag_U_little_matrix))
    DC_and_AC_coding(V_bianma_matrix, Zigzag_V_little_matrix, len(Zigzag_V_little_matrix))
    #熵编码
    #首先进行VLI变长整数编码，（x， y） = VLI(数字)
    #需要三个表：VLI表、DC亮度Huffman表、AC亮度Huffman表
    #用来存储最终的各个8*8矩阵的数据流
    print ("shang coding...")
    Y_coding_str = []
    U_coding_str = []
    V_coding_str = []
    #此处0代表亮度，1代表色度
    Shang_Coding(Y_bianma_matrix, Y_coding_str, 0)
    Shang_Coding(U_bianma_matrix, U_coding_str, 1)
    Shang_Coding(V_bianma_matrix, V_coding_str, 1)
#-------------------------------------------------------------------------------------
#     #从二进制变成VLI键值对
    print ("De Shang coding...")
    Y_bianma_matrix2 = []
    U_bianma_matrix2 = []
    V_bianma_matrix2 = []
    De_Shang_Coding(Y_coding_str, Y_bianma_matrix2, 0)
    De_Shang_Coding(U_coding_str, U_bianma_matrix2, 1)
    De_Shang_Coding(V_coding_str, V_bianma_matrix2, 1)
    #键值对通过变成64位矩阵
    print ("De_DC_and_AC_coding...")
    Zigzag_Y_little_matrix = []
    Zigzag_U_little_matrix = []
    Zigzag_V_little_matrix = []
    De_DC_and_AC_coding(Y_bianma_matrix, Zigzag_Y_little_matrix)
    De_DC_and_AC_coding(U_bianma_matrix, Zigzag_U_little_matrix)
    De_DC_and_AC_coding(V_bianma_matrix, Zigzag_V_little_matrix)
    #矩阵反zigzag
    print ("De_Zigzag...")
    Y_little_matrix = []
    U_little_matrix = []
    V_little_matrix = []
    for i in range(0, len(Zigzag_Y_little_matrix)):
        Y_little_matrix.append(De_Zigzag(Zigzag_Y_little_matrix[i], ZIGZAG_trans_matrix))
    for i in range(0, len(Zigzag_U_little_matrix)):
        U_little_matrix.append(De_Zigzag(Zigzag_U_little_matrix[i], ZIGZAG_trans_matrix))
    for i in range(0, len(Zigzag_V_little_matrix)):
        V_little_matrix.append(De_Zigzag(Zigzag_V_little_matrix[i], ZIGZAG_trans_matrix))
    #反量化和反DCT
    print ("De_Quantization_DCT...")
    Y_little_matrix = De_DCT_pre(Y_little_matrix, len(Y_little_matrix), 0)
    U_little_matrix = De_DCT_pre(U_little_matrix, len(U_little_matrix), 1)
    V_little_matrix = De_DCT_pre(V_little_matrix, len(V_little_matrix), 1)

    #块合并
    print ("De_Block...")
    Y_matrix = De_Block(Y_little_matrix, newsize)
    U_matrix = De_Block(U_little_matrix, newsize2)
    V_matrix = De_Block(V_little_matrix, newsize2)

    #反采样
    # print ("De_Sample...")
    # U_matrix = De_Sample(U_matrix, newsize2)
    # V_matrix = De_Sample(V_matrix, newsize2)
    #反填充
    print ("De fill...")
    Y_matrix = De_fill(Y_matrix,size)
    U_matrix = De_fill(U_matrix,size)
    V_matrix = De_fill(V_matrix,size)
    #YUV转RGB
    R = []
    G = []
    B = []
    for i in range(0, len(Y_matrix)):
        R.append(Y_matrix[i] + 1.402*(V_matrix[i] - 128))
        G.append(Y_matrix[i] - 0.34414*(U_matrix[i] - 128) - 0.71414*(V_matrix[i] - 128))
        B.append(Y_matrix[i] + 1.772*(U_matrix[i] - 128))

    #生成图片
    print ("waiting new pic...")
    x = image.size[0]
    y = image.size[1]
    # x = 1008
    # y = 720
    im = Image.new("RGB", (x, y))
    for i in range(0, x):
        for j in range(0, y):
            im.putpixel((i,j), (int(R[i*y+j]), int(G[i*y+j]), int(B[i*y+j])))
    # im.show()
    im.save(str(pic) + "_jpeg.jpg")

def test_DCT():
    # matrix_test = matrix_test
    matrix_src = matrix_test2
    print (matrix_src)
    Quantization_DCT_matrix = Quantization_DCT(matrix_src, 0)
    print (Quantization_DCT_matrix)
    matrix = De_Quantization_DCT(Quantization_DCT_matrix, 0)
    print (matrix)
    # print matrix_test2
    for i in range(0,MN*MN):
        print (matrix[i] - matrix_test2[i])
    
if __name__ == '__main__':
    test_main()

