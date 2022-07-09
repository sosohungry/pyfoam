# enconding=utf-8#!/usr/bin/python
# -*- coding: UTF-8 -*-
from genericpath import exists
from sys import flags
from traceback import walk_tb
from PyFoam.Basics.Utilities import writeDictionaryHeader
from PyFoam.FoamInformation import changeFoamVersion, oldTutorialStructure
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
import os
import shutil

'''
粘度 viscosity
张力 tension
速度 velocity
润滑性 lubricity
转流线 flow_line
提液 extract


'''


'''
    改变粘度和张力的基础操作，各个函数输入为所需要操作的例子文件输入和某个需要改变的参数
'''

def file_copy(source_path, target_path):

    '''
         文件夹复制操作，递归复制source文件下的全部文件
         source_path:源文件夹
         taget_path:目标文件夹 确定
    
    '''

    shutil.copytree(source_path, target_path)

    print("copy dir finished!")

def changeViscosity(source_path, change_num_water, change_num_oil, did_copy=True):

    '''
        改变水和油的粘度
        source_path:需要改变例子的文件目录
        change_num_water:需要改变水的粘度值
        change_num_oil:需要改变油的粘度值
        did_copy:是否进行复制 默认为True
    '''

    transportProerties = ParsedParameterFile(source_path + "/constant/transportProperties")



    if did_copy == True:
        target_path = "./water_oil" + str(change_num_water) + "_" + str(change_num_oil)

        file_copy(source_path, target_path)

        change_trans = ParsedParameterFile(target_path + "/constant/transportProperties")

    else:
        change_trans = transportProerties


    water = change_trans["water"]

    water_nu = water["nu"]


    oil = change_trans["oil"]

    oil_nu = oil["nu"]

    
    print(water_nu)

    print(oil_nu)


    water_nu[2] = float(change_num_water)
    oil_nu[2] = float(change_num_oil)
    print(water_nu) 
    print(oil_nu)

    # 复制文件重新写入
    
    change_trans.writeFile()

def changeTension(source_path, change_num, did_copy):
    '''
        改变张力值
        source_path:需要改变例子的文件目录
        change_num:需要改变张力的数值
        did_copy:是否进行复制 默认为True
    '''

    transportProerties = ParsedParameterFile(source_path + "/constant/transportProperties")

    if did_copy == True:
        target_path = "./Tension" + str(change_num)

        file_copy(source_path, target_path)

        change_trans = ParsedParameterFile(target_path + "/constant/transportProperties")
    

    else:
        change_trans = transportProerties
    sigma = change_trans["sigma"]

    print(sigma)


    sigma[2] = change_num

    change_trans.writeFile()



def changeVelocity (source_path, boundaryName, change_num, did_copy):

    '''
    
        需要改变某个口的速度
        source_path:需要改变例子的文件目录
        boundaryName:所需要修改的某个端口的名字
        change_num:对指定端口速度需要修改的值
        did_copy:是否进行复制 默认为True
    '''

    U = ParsedParameterFile(source_path + "/0/U")

    if did_copy == True:
        target_path = "./Velocity " + str(boundaryName) + '_' + str(change_num)


        file_copy(source_path, target_path)


        change_trans = ParsedParameterFile(target_path + "/0/U")

    else:

        change_trans = U



    boundaryField = change_trans["boundaryField"]

    boundaryName = boundaryField[boundaryName]

    print(boundaryName)

    boundaryName_value = boundaryName["value"]
    print(boundaryName_value)
    print("source number %s:%s" % (boundaryName, boundaryName_value))

    boundaryName["value"] =  change_num

    change_trans.writeFile()

def changeLubricity(source_path, boundaryName, change_num, did_copy):

    '''
        需要改变某个口的润湿性
        source_path:需要改变例子的文件目录
        boundaryName:所需要修改的某个端口的名字
        change_num:对指定端需要修改的值
        did_copy:是否进行复制 默认为True
    '''

    alpha_water = ParsedParameterFile(source_path + "/0/alpha.water")


    if did_copy == True:
        target_path = "./Lubricity" + str(boundaryName) + "_" + str(change_num)


        file_copy(source_path, target_path)


        change_trans = ParsedParameterFile(target_path + "/0/alpha.water")
    else:
        change_trans = alpha_water

    boundaryField = change_trans["boundaryField"]

    boundaryName = boundaryField[boundaryName]

    print(boundaryName)

    boundaryName_value = boundaryName["value"]
    print(boundaryName_value)
    print("source number %s:%s" % (boundaryName, boundaryName_value))

    boundaryName["value"] = change_num

    change_trans.writeFile()
    
    
    #设置边界条件 墙 入口 出口
    #  





def changeContactAngle(source_path, change_wall, change_num, did_copy):

    '''
        需要改变某个口的类型
        source_path:需要改变例子的文件目录
        change_wall:需要修改的墙壁
        change_num:对指定端需要修改的值
        did_copy:是否进行复制 默认为True
    '''
        
        
    alpha_water = ParsedParameterFile(source_path + "/0/alpha.water")


    if did_copy == True:
        target_path = "./ContactAngle" + str(change_wall) + "_" + str(change_num)


        file_copy(source_path, target_path)
        change_trans = ParsedParameterFile(target_path + "/0/alpha.water")
    else:
        change_trans = alpha_water


    boundaryField = change_trans["boundaryField"] 


    boundaryField[change_wall]["type"] = "constantAlphaContactAngle"

    boundaryField[change_wall]["theta0"] = change_num


    change_trans.writeFile()


# def changeFlowLine(source_path):


#     U = ParsedParameterFile(source_path + "/0/U")

#     change_num_inlet1 = input("please input str to change Speed inlet1: ")

#     change_num_inlet2 = input("please input str to change Speed inlet2: ")


#     target_path = "./Flowline" + str(change_num_inlet1) + "_" + str(change_num_inlet2)


#     file_copy(source_path, target_path)

#     time0 = target_path + "/0"

#     time10 = target_path + "/10"

#     file_copy(time0, time10)

#     change_trans = ParsedParametterFile(target_path + "/10/U")

#     inlet1 = change_trans["boundaryField"]["inlet1"]

#     inlet2 = change_trans["boundaryField"]["inlet2"]

#     print(inlet1)

#     print(inlet2)
#     inlet1_value = inlet1["value"]

#     inlet2_value = inlet2["value"]


#     inlet1["value"] = change_num_inlet1

#     inlet2["value"] = change_num_inlet2


#     change_trans.writeFile()

# def changeExtract(source_path):

#     U = ParsedParameterFile(source_path + "/0/U")

#     change_num_inlet1 = input("please input str to change Speed inlet1: ")

#     change_num_inlet2 = input("please input str to change Speed inlet2: ")


#     target_path = "./Extract" + str(change_num_inlet1) + "_" + str(change_num_inlet2)


#     file_copy(source_path, target_path)

#     time0 = target_path + "/0"

#     time10 = target_path + "/10"

#     file_copy(time0, time10)

#     change_trans = ParsedParameterFile(target_path + "/10/U")

#     inlet1 = change_trans["boundaryField"]["inlet1"]

#     inlet2 = change_trans["boundaryField"]["inlet2"]

#     print(inlet1)

#     print(inlet2)
#     inlet1_value = inlet1["value"]

#     inlet2_value = inlet2["value"]


#     inlet1["value"] = change_num_inlet1

#     inlet2["value"] = change_num_inlet2


#     change_trans.writeFile()


