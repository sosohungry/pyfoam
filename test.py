from genericpath import exists
from sys import flags
from traceback import walk_tb
from typing import Dict
from PyFoam.Basics.Utilities import writeDictionaryHeader
from PyFoam.FoamInformation import changeFoamVersion, oldTutorialStructure
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
import os
import shutil
from PyFoam.Basics.DataStructures import Vector,Field,Dimension,DictProxy,TupleProxy,Tensor,SymmTensor,Unparsed,UnparsedList,Codestream,DictRedirection,BinaryBlob,BinaryList,BoolProxy


from sip import delete

U = ParsedParameterFile("./SetDefault /0/U")



a = DictProxy()
print(a)

a["value"] = "fixed"

print(a)