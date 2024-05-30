import numpy as np
from biomimetic import ModeMMBmcModel


MMMBmcModelDataSet = {
    ((1, 0, 1),
      (1, 0, 0),
      (1, 1, 1)) : [[False, True], [True, False]],
    ((1, 0, 1),
      (1, 0, 0),
      (1, 1, 0)) : [[False, True], [True, True]],
    ((1, 0, 0),
      (0, 1, 0),
      (1, 0, 1)) : [[True, False], [True, False]],
    ((1, 1, 1),
      (0, 0, 0),
      (1, 1, 0)) : [[False, True], [True, True]],
    ((0, 0, 1),
      (1, 1, 0), 
      (0, 0, 1)) : [[True, False], [False, False]]
}

MMMBmcModelDataSetAllocations = {0: [0, 1],
                                  1: [2]}

MMMBmcModel = ModeMMBmcModel("MMMBmcModel", MMMBmcModelDataSet)
print()
print(MMMBmcModel)
MMMBmcModel.learnModel(MMMBmcModelDataSetAllocations)
print(MMMBmcModel.activateModel([[1, 0, 1],
                                  [1, 1, 0],
                                  [1, 1, 0]], 0))
print(MMMBmcModel.activateModel([[1, 0, 1],
                                  [1, 1, 0],
                                  [1, 1, 0]], 1))
print(MMMBmcModel.activateModel([[1, 0, 1],
                                  [1, 1, 0],
                                  [1, 1, 1]], 0))
print(MMMBmcModel.activateModel([[1, 0, 0],
                                  [0, 1, 0],
                                   [1, 1, 1]], 0))
print(MMMBmcModel.activateModel([[1, 1, 1],
                                  [0, 0, 0],
                                  [1, 1, 0]], 0))
print(MMMBmcModel.activateModel([[0, 0, 1],
                                  [1, 1, 0],
                                  [0, 0, 1]], 0))
print(MMMBmcModel.activateModel([[1, 0, 1],
                                  [1, 1, 0],
                                  [1, 1, 1]], 1))
print(MMMBmcModel.activateModel([[1, 0, 0],
                                  [0, 1, 0],
                                   [1, 1, 1]], 1))
print(MMMBmcModel.activateModel([[1, 1, 1],
                                  [0, 0, 0],
                                  [1, 1, 0]], 1))
print(MMMBmcModel.activateModel([[0, 0, 1],
                                  [1, 1, 0],
                                  [0, 0, 1]], 1))
print(MMMBmcModel.activateModel([[0, 1, 1],
                                  [1, 0, 1],
                                  [1, 0, 0]], 2))