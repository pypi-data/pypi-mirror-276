import numpy as np
from biomimetic import SimpleBiasBmcModel


BiasBmcModelDataset = np.array([[0,0,0],
                                [0,1,1],
                                [1,0,1],
                                [1,1,0]])
BiasBmcModel = SimpleBiasBmcModel("Xor", BiasBmcModelDataset, 2)
print(BiasBmcModel)
BiasBmcModel.learnModel()
print(BiasBmcModel.activateModel([[0,1]]))
print(BiasBmcModel.activateModel([[0,0]]))
print(BiasBmcModel.activateModel([[1,1]]))
print(BiasBmcModel.activateModel([[1,0]]))