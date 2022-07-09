
from genericpath import exists
from sys import flags
from traceback import walk_tb
from PyFoam.Basics.Utilities import writeDictionaryHeader
from PyFoam.FoamInformation import changeFoamVersion, oldTutorialStructure
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
import os
import shutil
from code.changfile import *

# changeFloodingDirection
# {
#     enable   true/false;
# 	inletOld    ***; 
# 	outletOld    ***; 
# 	inletNew      ***; 
# 	outletNew     ****; 
# 	inletVelocity    ****;  //inlet 
# 	inletAlpha       *****;  //inlet
# 	ouletPressure    ****;  //outlet
# 	contactAngle     45;     //wall
# }


def changeFloodDirection(source_path, did_copy):


    
    U = ParsedParameterFile(source_path + "/0/U")
    print("the boundary have:")
    let = U["boundaryField"]

    # for i in range(len(let.keys())):
    #     print(let[i])

    # print(let)
    let_it = let.keys()

    for x in let_it:
        print(x, end=" ")

    inletOld = input("please input old intet:")
    outletOld = input("please input old outlet:")

    inletNew = input("please input new inlet:")
    outletNew = input("please input new outlet:")

    inletVelocity = input("please input inlet velocity:")


    if did_copy == True:
        target_path = "./FloodDirection " + str(inletOld) + '_' + str(inletNew)


        file_copy(source_path, target_path)


        change_trans = ParsedParameterFile(target_path + "/0/U")

    else:

        change_trans = U



    if inletOld in let_it:
        change_trans[inletOld]["type"] = "fixedValue"

    if outletOld in let_it:
        change_trans[outletOld]["type"] = "fixedValue"

    if inletNew in let_it:

        change_trans[inletNew]["type"] = "inletOutlet"

    if outletNew in let_it:

        change_trans[outletNew]["type"] = "inletOutlet"

    
    change_trans[inletNew]["value"] = inletVelocity



    change_trans.writeFile()


    




changeFloodDirection("./Tension1", True)