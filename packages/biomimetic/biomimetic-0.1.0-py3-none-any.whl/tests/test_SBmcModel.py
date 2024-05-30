import numpy as np
from biomimetic import SimpleBmcModel


BmcModelDataset = np.array([[0,0,0],
                            [0,1,1],
                            [1,0,1],
                            [1,1,0]])
BmcModel = SimpleBmcModel("Xor", BmcModelDataset, 2)
print(BmcModel)
BmcModel.learnModel()
print(BmcModel.activateModel([[0,1]]))
print(BmcModel.activateModel([[0,0]]))
print(BmcModel.activateModel([[1,1]]))
print(BmcModel.activateModel([[1,0]]))