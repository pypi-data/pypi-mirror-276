# -*- coding:utf-8 -*-
# data analyst for Yoshie Lab prepared by ZD
# 20240528 v0.3
# 20240529 v0.5


import re
import math
import csv
import matplotlib.pyplot as plt


def IR_data_reader(data_file, x1=500, x2=4000):  # x1到x2为读取范围，返回范围内data
    column = []  # 返回一个list,[[x],[y]]
    list_count = -1  # 动态list计数器
    read_IR_bool = 0
    IR_bool = 0
    with open(data_file, 'r') as file_object:
        for line in file_object:
            if read_IR_bool == 1:  # IR
                if line.replace("\r", "").replace("\n", "") == "":
                    break
                else:
                    while len(column) < list_count:  # 动态list初始化
                        column.append([])
                temprow = re.split('[,\t]', line.replace("\r", "").replace("\n", ""))  # 定义临时行
                if x1 <= float(temprow[0]) <= x2:
                    column[0] += [float(temprow[0])]
                    column[1] += [float(temprow[1])]
            if str(line).replace("\r", "").replace("\n", "").replace(" ", "") == "##YUNITS=Abs" or str(line).replace(
                    "\r", "").replace("\n", "").replace(" ", "") == "##YUNITS=%T":  # IR 特征
                read_IR_bool = 1
                IR_bool = 1
                list_count = 2
    return column  # 返回一个list,[[x],[y]]


# from here: Tensile data reader

# from here support for Tensile
def read_cvs_file(file):  # support for Tensile
    count = -1
    read_tensile_bool = 0  # 0 False 1 True 是否可以开始读取的bool开关
    tensile_bool = 0  # 确认读取文件类型
    read_data = []  # 将数据读取到这个list里，[[test1],[test2]...]
    with open(file, 'r', encoding='gbk') as csvfile:
        count_csv = csv.reader(csvfile, delimiter=',')
        for line in count_csv:
            if line != []:
                if read_tensile_bool == 1:
                    if len(read_data) < count + 1:  # 手动添加动态list
                        read_data.append([])
                    read_data[count] += [line]
                if line[0] == 'sec' and line[1] == 'N':  # tensile文件特征
                    count += 1
                    read_tensile_bool = 1
                    tensile_bool = 1
            else:
                read_tensile_bool = 0
    csvfile.close()
    if tensile_bool == 1:
        read_data.append('tensile')
    # read_data.append(count+1)
    # print(read_data)
    return read_data
# support for Tensile
# support for Tensile
def read_tensile_thickness(file):  # support for Tensile
    read_bool = 0  # 0 False 1 True 是否可以开始读取的bool开关
    thickness = []  # 将数据读取到这个list里，[[test1],[test2]...]
    with open(file, 'r', encoding='gbk') as csvfile:
        count_csv = csv.reader(csvfile, delimiter=',')
        for line in count_csv:
            if line != []:
                if read_bool == 1:
                    thickness.append(line[1])
                if line[1] == 'Thickness':
                    read_bool = 1
            else:
                read_bool = 0
    csvfile.close()
    del thickness[0]
    return thickness
# to here support for Tensile

def Tensile_data_reader(filename):  # 读取文件 # 输出[[x1],[y1],[x2],[y2]]
    output_column = []
    tempfilename = re.split(r'[./\\]',str(filename))
    if str(tempfilename[len(tempfilename)-1]) == "csv":
        data_in = read_cvs_file(filename)
        global fname
        fname = str(tempfilename[len(tempfilename)-2])
    else:
        data_in = '0'
    if data_in != '0':
        if data_in[len(data_in) - 1] == "tensile":  # 确认读取为tensile
            del data_in[len(data_in) - 1]
            thickness = read_tensile_thickness(filename)
            count = 0
            i = 0
            j = 0  # i: 帮助定位thickness的临时变量
            x = []
            y = []
            for temp_list in data_in:
                column1 = []
                column2 = []
                column3 = []  # column1: time, column2 : force, column3: strain
                for real_list in temp_list:
                    column1.append(real_list[0])
                    column2.append(float(real_list[1]) / (1.33 * float(thickness[i])))
                    column3.append(float(real_list[2]) / 0.08)
                x.append([])
                y.append([])
                x[i] = column3
                y[i] = column2
                output_column.append([])
                output_column.append([])
                # print([column3]+[column2])
                output_column[j]=column3
                output_column[j+1]=column2
                i += 1
                j += 2
    return(output_column)  # 输出[[x1],[y1],[x2],[y2]]
# to here: Tensile data reader

# 写入list(一般是其他fuc转换为的list),当reverse为True，将按列储存转换为按行储存，然后输出到output_filename中
def write_to_txt(output_filename, list_input, reverse=True, write = True):  # 写入list(一般是其他fuc转换为的list),当reverse为True，将按列储存转换为按行储存，然后输出到output_filename中
    # 找到最长的列长度
    max_length = max(len(column) for column in list_input)
    # 将每列填充到相同的长度
    padded_columns = [column + [''] * (max_length - len(column)) for column in list_input]
    # 转置列表
    # list_of_reverse = list(zip(*padded_columns))
    if reverse == True:
        # 转置列表
        list_of_reverse = list(zip(*padded_columns))
    else:
        list_of_reverse = list_input
    if write == True:
        with open('./'+output_filename,'w',encoding='utf-8') as writeObject1:
            for row in list_of_reverse:
                # line = ','.join(str(row))
                writeObject1.write(str(row).replace('(','').replace(')','')+'\n')
        writeObject1.close()
    # print(list_of_reverse)
    return list_of_reverse  # 返回置换后的list


# cyclic的data切断，需要输入write_to_txt转换好的[[x1,y1],[x2,y2]...]的格式
def Cyclic_data_arrange(colunm_input_cyc, threshold=0.01):  # column_input_cyc: 被column_reverse转换好的[[x1,y1],[x2,y2]...]的格式
    x = 0  # 读取x值
    i = 0
    output_column = []
    output_column.append([])
    output_column.append([])
    read_bool = True
    for line in colunm_input_cyc:
        difference = float(str(line).replace('(','').replace(')','').split(',')[0]) - x
        if math.fabs(difference) >= math.fabs(threshold):
            if read_bool == False:
                i+=2
                output_column.append([])
                output_column.append([])
            read_bool = True
        else:
            read_bool = False
        if read_bool == True:
            output_column[i].append(float(str(line).replace('(','').replace(')','').split(',')[0]))
            output_column[i+1].append(float(str(line).replace('(', '').replace(')', '').split(',')[1]))
        x = float(str(line).replace('(','').replace(')','').split(',')[0])
    return output_column  # 输出切断好的数据