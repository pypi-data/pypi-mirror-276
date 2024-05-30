import numpy as np
from biomimetic import ParallelMOBmcModel


PMOBmcModelDataSet = {
    ((1, 0, 1),
      (1, 0, 0)) : [False, True, True, False],
    ((1, 0, 0),
      (0, 1, 0)) : [True, False, True, False],
    ((1, 1, 1),
      (0, 0, 0)) : [False, True, True, True],
    ((0, 0, 1),
      (1, 1, 0)) : [True, False, False, False]
}

PMOBmcModel = ParallelMOBmcModel("PMOBmcModel", PMOBmcModelDataSet)
print()
print(PMOBmcModel)
PMOBmcModel.learnModel()
print(PMOBmcModel.activateModel([[1, 0, 1],
                                  [1, 0, 0]]))
print(PMOBmcModel.activateModel([[1, 0, 0],
                                  [0, 1, 0]]))
print(PMOBmcModel.activateModel([[1, 1, 1],
                                  [0, 0, 0]]))
print(PMOBmcModel.activateModel([[0, 0, 1],
                                  [1, 1, 0]]))
print(PMOBmcModel.activateModel([[0, 0, 0],
                                  [1, 1, 1]]))  # Some Familiar input, proble for future
print(PMOBmcModel.activateModel([[0, 1, 1],
                                  [1, 0, 1]]))  # Unfamiliar input