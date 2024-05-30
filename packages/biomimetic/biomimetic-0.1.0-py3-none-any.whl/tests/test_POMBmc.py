import numpy as np
from biomimetic import ParallelOMBiomimeticCell


POMBmc = ParallelOMBiomimeticCell((1,1), 3,2,3, 2)
print()
print(POMBmc)
POMBmc.learn(np.array([[1, 0, 1]]))
POMBmc.output(np.array([[True, False], 
                        [False, False]]
                       ))
POMBmc.activate(np.array([[1, 0, 1]]))
print(POMBmc)
print(POMBmc.fire(np.array([1, 0])))
print(POMBmc)

POMBmc.activate(np.array([[0, 1, 1]]))
print(POMBmc)
print(POMBmc.fire(np.array([1, 1])))
print(POMBmc)