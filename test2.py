from genericpath import exists
from sys import flags
from traceback import walk_tb
from PyFoam.Basics.Utilities import writeDictionaryHeader
from PyFoam.FoamInformation import changeFoamVersion, oldTutorialStructure
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
import os
import shutil

from sip import delete

U = ParsedParameterFile("./Tension1/0/U")

# print(U)

a = U["boundaryField"]

# print(a)

print(a.keys())

b = input()

if b in a.keys():
    print(b + " in boundaryfield")