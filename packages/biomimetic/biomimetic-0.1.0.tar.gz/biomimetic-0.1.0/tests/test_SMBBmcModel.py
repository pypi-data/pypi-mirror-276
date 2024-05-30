import numpy as np
from biomimetic import SimpleModeBiasBmcModel


ModeBmcModelDataset = np.array([[[0,0,1],
                                 [0,1,1]], # Mode 0
                                [[1,1,0],
                                 [1,0,1]]]) # Mode 1
ModeBmcModel = SimpleModeBiasBmcModel("Xor", ModeBmcModelDataset, 2)
print(ModeBmcModel)
ModeBmcModel.learnModel()
print(ModeBmcModel.activateModel([[0,1]],0))
print(ModeBmcModel.activateModel([[0,0]],0))
print(ModeBmcModel.activateModel([[1,1]],0))
print(ModeBmcModel.activateModel([[1,0]],0))

print(ModeBmcModel.activateModel([[0,1]],1))
print(ModeBmcModel.activateModel([[0,0]],1))
print(ModeBmcModel.activateModel([[1,1]],1))
print(ModeBmcModel.activateModel([[1,0]],1))
