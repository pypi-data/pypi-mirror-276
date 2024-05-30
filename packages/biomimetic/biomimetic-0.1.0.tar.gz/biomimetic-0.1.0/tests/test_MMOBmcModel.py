import numpy as np
from biomimetic import ModeMOBmcModel


MMOBmcModelDataSet = {
    ((1, 0, 1),
      (1, 0, 0)) : [False, True, True, False],
    ((1, 0, 0),
      (0, 1, 0)) : [True, False, True, False],
    ((1, 1, 1),
      (0, 0, 0)) : [False, True, True, False],
    ((0, 0, 1),
      (1, 1, 0)) : [True, False, False, False]
}
MMOBmcModel = ModeMOBmcModel("MMOBmcModel", MMOBmcModelDataSet)
print()
print(MMOBmcModel)
MMOBmcModel.learnModel()
print(MMOBmcModel.activateModel([[1, 0, 1],
                                  [1, 0, 0]], 0))
print(MMOBmcModel.activateModel([[1, 0, 0],
                                  [0, 1, 0]], 1))
print(MMOBmcModel.activateModel([[1, 0, 0],
                                  [0, 1, 0]], 0))
print(MMOBmcModel.activateModel([[1, 0, 1],
                                  [1, 0, 0]], 1))
print(MMOBmcModel.activateModel([[1, 1, 1],
                                  [0, 0, 0]], 0))
print(MMOBmcModel.activateModel([[0, 0, 1],
                                  [1, 1, 0]], 0))
print(MMOBmcModel.activateModel([[0, 0, 0],
                                  [1, 1, 1]], 0))
print(MMOBmcModel.activateModel([[0, 1, 1],
                                  [1, 0, 1]], 0))