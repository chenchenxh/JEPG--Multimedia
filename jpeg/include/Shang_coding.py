# coding=utf-8
#十进制转二进制
#DCT中的M和N参数，此处设置为8
MN = 8;
from jpegMatrix import *
#接收DCmatrix，然后在DC后面拼接AC的数值
def AC(mid_matrix, src_matrix):
    num_of_0 = 0
    for i in range(1, MN*MN):
        if src_matrix[i] != 0:
            mid_matrix.append((num_of_0, src_matrix[i]))
            num_of_0 = 0
        elif i == MN*MN-1:
            mid_matrix.append((num_of_0, src_matrix[i]))
            num_of_0 = 0
        else :
            num_of_0+=1
        if num_of_0>15:
            mid_matrix.append((15, 0))
            num_of_0 = 0

def Dec_To_Bin(Number):
    i = 0
    bin_number = 0
    Number = abs(Number)
    while Number != 0:
        temp = Number % 2
        Number = Number / 2
        bin_number = bin_number + temp*(10**i)
        i+=1
    return bin_number 
#二进制转十进制
def Bin_To_Dec(Number):
    Dec_Number = 0
    i = 0
    while Number != 0:
        temp = Number % 10
        Number = Number / 10
        Dec_Number = Dec_Number + temp*(2**i)
        i += 1
    return Dec_Number

#接收一个数字，返回它的VLI
def VLI(VLI_Num):
    code_mid = str(Dec_To_Bin(VLI_Num))
    code = ''
    if VLI_Num < 0:
        for i in range(0, len(code_mid)):
            if code_mid[i] == '0':
                code = code + '1'
            elif code_mid[i] == '1':
                code = code + '0'
    else:
        code = code_mid
    return ((len(code), code))
#str不为空，第一个数字如果为0说明是负数，进行转换
def De_VLI(VLI_Num_str):
    # print "VLI_Num_str: %s" %(VLI_Num_str)
    if VLI_Num_str[0] == '0':
        mid_str = ''
        for i in range(0,len(VLI_Num_str)):
            if VLI_Num_str[i] == '1':
                mid_str += '0'
            elif VLI_Num_str[i] == '0':
                mid_str += '1'
        return -Bin_To_Dec(int(mid_str))
    else:
        return Bin_To_Dec(int(VLI_Num_str))

def DC_and_AC_coding(bianma_matrix, Zigzag_little_matrix, length):
    for i in range(0, length):
        mid_matrix = []
        U_mid_matrix = []
        V_mid_matrix = []
        #DC
        if i == 0:
            mid_matrix.append((0, Zigzag_little_matrix[i][0]))
        else:
            mid_matrix.append((0 ,Zigzag_little_matrix[i][0] - Zigzag_little_matrix[i-1][0]))
        #求出AC
        AC(mid_matrix, Zigzag_little_matrix[i])
        bianma_matrix.append(mid_matrix)
def De_DC_and_AC_coding(bianma_matrix, Zigzag_little_matrix):
    for i in range(0, len(bianma_matrix)):
        mid_matrix = []
        for j in range(0, len(bianma_matrix[i])):
            for count in range(0, bianma_matrix[i][j][0]):
                mid_matrix.append(0)
            if i > 0 and j == 0:
                mid_matrix.append(bianma_matrix[i][j][1] + Zigzag_little_matrix[i-1][0])
            else:
                mid_matrix.append(bianma_matrix[i][j][1])
        if len(mid_matrix) != 64:
            print (bianma_matrix[i])
            print ("block number error %d" %(len(mid_matrix)))
        Zigzag_little_matrix.append(mid_matrix)

def Shang_Coding(matrix_array, str_array, DC_AC):
    for count in range(0, len(matrix_array)):
        (DC_group, DC_VLI_code) = VLI(matrix_array[count][0][1])
        DC_HUffman_code = ''
        if DC_AC == 0:
            DC_HUffman_code = DC_Luminance_Huffman[DC_group]
        else:
            DC_HUffman_code = DC_Chroma_Huffman[DC_group]
        code_sum = DC_HUffman_code + DC_VLI_code
        for i in range(1, len(matrix_array[count])):
            (AC_group, AC_VLI_code) = VLI(matrix_array[count][i][1])
            AC_Huffman_code = ''
            if DC_AC == 0:
                AC_Huffman_code = AC_Luminance_Huffman[(matrix_array[count][i][0], AC_group)]
            else:
                AC_Huffman_code = AC_Chroma_Huffman[(matrix_array[count][i][0]), AC_group]
            #code_sum存储每个8*8矩阵压缩后的编码
            code_sum += AC_Huffman_code + AC_VLI_code
        str_array.append(code_sum)

def De_Shang_Coding(str_array, matrix_array, DC_AC):
    items = 0
    key = 0
    for i in range(0, len(str_array)):
        j = 0
        #flag用于标志这个是不是第一个，如果是则用DC，否则用AC
        flag = 0
        mid_str = ''
        mid_matrix = []
        while j < len(str_array[i]):
            mid_str += str_array[i][j]
            # print "mid_str: %s" %(mid_str)
            j+=1
            if DC_AC == 0 :
                if flag == 0:
                    items = DC_Luminance_Huffman.items()
                elif flag == 1:
                    items = AC_Luminance_Huffman.items()
            elif DC_AC == 1:
                if flag == 0:
                    items = DC_Chroma_Huffman.items()
                elif flag == 1:
                    items = AC_Chroma_Huffman.items()
            for (k,v) in items:
                # print mid_str
                if v == mid_str:
                    key = k
                    mid_str = ''
                    VLI_Num = 0
                    #此处得到key，根据key再读入key个数字，然后就压栈。记得判断key的type
                    #如果flag为0，那么说明是DC，此时key为int
                    if flag == 0:
                        # print "key : %d" %(key)
                        VLI_Num_str = ''
                        for k in range(0, key):
                            VLI_Num_str += str_array[i][j]
                            j+=1
                        #处理VLI_Num_str，变成整数
                        if VLI_Num_str == '':
                            print ("VLI_Num: %d" %(VLI_Num))
                            mid_matrix.append((0, 0))
                        else:
                            VLI_Num = De_VLI(VLI_Num_str)
                            # print "VLI_Num: %d" %(VLI_Num)
                            mid_matrix.append((0, VLI_Num))
                    #如果flag为1，那么说明是AC，此时key为（int，int）
                    elif flag == 1:
                        # print "key : %d" %(key[1])
                        VLI_Num_str = ''
                        for k in range(0, key[1]):
                            VLI_Num_str += str_array[i][j]
                            j+=1
                        if VLI_Num_str == '':
                            # print "VLI_Num: %d" %(VLI_Num)
                            mid_matrix.append((key[0],0))
                        else:
                            VLI_Num = De_VLI(VLI_Num_str)
                            # print "VLI_Num: %d" %(VLI_Num)
                            mid_matrix.append((key[0], VLI_Num))
                    # print 
                    flag = 1
        matrix_array.append(mid_matrix)
