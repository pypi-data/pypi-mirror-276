import numpy as np
from biomimetic import ModeOMBmcModel


MOMBmcModelDataSet = {
        (0,1,1): [[False, True], [True, False]],
        (0,1,0): [[True, False], [True, False]],
        (1,0,0): [[False, True], [True, False]],
        (1,1,0): [[True, False], [False, False]]
}

MOMBmcModel = ModeOMBmcModel("MOMBmcModel", MOMBmcModelDataSet)
print(MOMBmcModel)
MOMBmcModel.learnModel()
print(MOMBmcModel.activateModel(np.array([[0,1,1]]), 1)) # wrong weight index so weight should be 1,0,0
print(MOMBmcModel.activateModel(np.array([[0,1,1]]), 0))
print(MOMBmcModel.activateModel(np.array([[1,1,1]]), 0)) # unfamiliar input
print(MOMBmcModel.activateModel(np.array([[1,1,0]]), 0))
print(MOMBmcModel.activateModel(np.array([[0,1,0]]), 1)) # out of bounds weight