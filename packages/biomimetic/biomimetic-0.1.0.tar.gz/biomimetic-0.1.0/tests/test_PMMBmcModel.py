import numpy as np
from biomimetic import ParallelMMBmcModel


PMMBmcModelDataSet = {
    ((1, 0, 1),
      (1, 0, 0),
      (1, 1, 1)) : [[False, True], [True, False]],
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

PMMBmcModelDataSetAllocations = {0: [0, 1],
                                  1: [2]}

PMMBmcModel = ParallelMMBmcModel("PMMBmcModel", PMMBmcModelDataSet)
print()
print(PMMBmcModel)
PMMBmcModel.learnModel(PMMBmcModelDataSetAllocations)
print(PMMBmcModel.activateModel([[1, 0, 1],
                                  [1, 1, 0], # not equal 0
                                  [1, 1, 1]]))
print(PMMBmcModel.activateModel([[1, 0, 0],
                                  [0, 1, 0],
                                   [1, 1, 1]])) # not equal 1
print(PMMBmcModel.activateModel([[1, 1, 1],
                                  [0, 0, 0],
                                  [1, 1, 0]]))
print(PMMBmcModel.activateModel([[0, 0, 1],
                                  [1, 1, 0],
                                  [0, 0, 1]]))
print(PMMBmcModel.activateModel([[0, 1, 1],
                                  [1, 0, 1],
                                  [1, 0, 0]]))  # Unfamiliar input (both not equal)
