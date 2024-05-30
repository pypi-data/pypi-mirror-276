# -*- coding:utf-8 -*-
# data analyst for Yoshie Lab prepared by ZD
# 20240528 v0.1


import re
import math

def IR_data_read(data_file, x1, x2):  # x1到x2为读取范围，返回范围内data
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