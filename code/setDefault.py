from genericpath import exists
from sys import flags
from traceback import walk_tb
from types import new_class
# from typing_extensions import ParamSpec
import PyFoam
from PyFoam.Basics.Utilities import writeDictionaryHeader
from PyFoam.FoamInformation import changeFoamVersion, oldTutorialStructure
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
import os
import shutil
from code.changfile import *

from PyFoam.Basics import FoamFileGenerator
from PyFoam.Basics import DataStructures




def setDefault(source_path):

    target_path = "./SetDefault"


    file_copy(source_path, target_path)


    change_trans_U = ParsedParameterFile(target_path + "/0/U")
    change_trans_alpha = ParsedParameterFile(target_path + "/0/alpha.water")
    change_trans_prgh = ParsedParameterFile(target_path + "/0/p_rgh")
    transport = ParsedParameterFile(target_path + "/constant/transportProperties")

    # print(change_trans_alpha)
    # print(change_trans_prgh)
    # print(change_trans_U)
    # print(transport)

    print("please input inlet boundaryName:")

    inletboundary = input().split()

    print("please input outlet boundaryName:")

    outletboundary = input().split()

    print("please input wall boundaryName:")

    wall = input().split()

    allboundary = inletboundary + outletboundary + wall

    print(inletboundary)

    print(outletboundary)

    print(allboundary)


    ## inlet
    for i in range(len(inletboundary)):
        change_trans_U["boundaryField"][inletboundary[i]] = DataStructures.DictProxy()
        change_trans_U["boundaryField"][inletboundary[i]]["type"] = "fixedValue"
        print("please input %s inletVelocity:" % inletboundary[i])
        inletVelocity = input()
        change_trans_U["boundaryField"][inletboundary[i]]["value"] = inletVelocity

    for i in range(len(inletboundary)):

        change_trans_alpha["boundaryField"][inletboundary[i]] = DataStructures.DictProxy()
        change_trans_alpha["boundaryField"][inletboundary[i]]["type"]  =  "constantAlphaContactAngle"

        print("please input %s inletAlpha" % inletboundary[i])
        inletAlpha = input()
        change_trans_alpha["boundaryField"][inletboundary[i]]["theta0"]  =  inletAlpha
        change_trans_alpha["boundaryField"][inletboundary[i]]["limit"]  =  "gradient"
        change_trans_alpha["boundaryField"][inletboundary[i]]["value"]  =  "uniform 0"


    for i in range(len(inletboundary)):
        change_trans_prgh["boundaryField"][inletboundary[i]] = DataStructures.DictProxy()

        change_trans_prgh["boundaryField"][inletboundary[i]]["type"] = "fixedFluxPressure"
        change_trans_prgh["boundaryField"][inletboundary[i]]["value"] = "uniform 0"


    ## outlet
    for i in range(len(outletboundary)):
        change_trans_U["boundaryField"][outletboundary[i]] = DataStructures.DictProxy()
        change_trans_U["boundaryField"][outletboundary[i]]["type"] = "inletOutlet"
        print("please input outlet value")
        outletValue = input()
        change_trans_U["boundaryField"][outletboundary[i]]["value"] = outletValue


    for i in range(len(outletboundary)):
        change_trans_alpha["boundaryField"][outletboundary[i]] = DataStructures.DictProxy()

        change_trans_alpha["boundaryField"][outletboundary[i]]["type"] = "constantAlphaContactAngle"
        change_trans_alpha["boundaryField"][outletboundary[i]]

    for i in range(len(outletboundary)):
        change_trans_prgh["boundaryField"][outletboundary[i]] = DataStructures.DictProxy()

        change_trans_prgh["boundaryField"][outletboundary[i]]["type"] = "fixedValue"
        change_trans_prgh["boundaryField"][outletboundary[i]]["value"] = "uniform 0"

       
    ## wall

    for i in range(len(wall)):

        change_trans_U["boundaryField"][wall[i]] = DataStructures.DictProxy()
        change_trans_U["boundaryField"][wall[i]]["type"] = "fixedValue"
        change_trans_U["boundaryField"][wall[i]]["value"] = "uniform 0"

    for i in range(len(wall)):
        change_trans_alpha["boundaryField"][wall[i]] = DataStructures.DictProxy()


        change_trans_alpha["boundaryField"][wall[i]]["type"] = "constantAlphaContactAngle"
        print("please input theta of wall:")
        theta = input()
        change_trans_alpha["boundaryField"][wall[i]]["theta0"] = theta
        change_trans_alpha["boundaryField"][wall[i]]["limit"] = "gradient"
        change_trans_alpha["boundaryField"][wall[i]]["value"] = "uniform 0"

    for i in range(len(wall)):

        change_trans_prgh["boundaryField"][wall[i]] = DataStructures.DictProxy()

        change_trans_prgh["boundaryField"][wall[i]]["type"] = "fixedFluxPressure"
        change_trans_prgh["boundaryField"][wall[i]]["value"] = "uniform 0"



    
    boundary_u = change_trans_U["boundaryField"].keys()

    print(boundary_u)

    for i in range(len(boundary_u)):
        if boundary_u[i] not in allboundary:
            del change_trans_U["boundaryField"][boundary_u[i]]

    
    boundary_alpha = change_trans_alpha["boundaryField"].keys()

    print(boundary_alpha)

    for i in range(len(boundary_alpha)):
        if boundary_u[i] not in allboundary:
            del change_trans_alpha["boundaryField"][boundary_alpha[i]]


    boundary_p = change_trans_prgh["boundaryField"].keys()

    print(boundary_p)

    for i in range(len(boundary_p)):
        if boundary_p[i] not in allboundary:
            del change_trans_prgh["boundaryField"][boundary_p[i]]
        

    print(change_trans_U["boundaryField"])
    print(change_trans_alpha["boundaryField"])
    print(change_trans_prgh["boundaryField"])


    print("please input water and oil viscosity")
    water_viscosity = input()
    transport["water"]["nu"][2] = water_viscosity
    oil_viscosity = input()
    transport["oil"]["nu"][2] = oil_viscosity

    print("please input surfacetenstion:")
    tension = input()

    transport["sigma"][2] = input()


    change_trans_alpha.writeFile()
    change_trans_prgh.writeFile()
    change_trans_U.writeFile()
    transport.writeFile()

