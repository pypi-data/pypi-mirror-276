import numpy as np
from biomimetic import ParallelOMBmcModel


POMBmcModelDataSet = {
    (0,1,1): [[False, True], [True, False]],
    (0,1,0): [[True, False], [True, False]],
    (1,0,0): [[False, True], [True, True]],
    (1,1,0): [[True, False], [False, False]]
}

POMBmcModel = ParallelOMBmcModel("POMBmcModel", POMBmcModelDataSet)
print()
print(POMBmcModel)
POMBmcModel.learnModel()
print(POMBmcModel.activateModel([0, 1, 1]))
print(POMBmcModel.activateModel([0, 1, 0]))
print(POMBmcModel.activateModel([1, 1, 0]))
print(POMBmcModel.activateModel([1, 0, 0]))
print(POMBmcModel.activateModel([0, 0, 0]))  # Unfamiliar input