import numpy as np
from biomimetic import ModeOMBiomimeticCell 

MOMBmc = ModeOMBiomimeticCell((1,1), 3,2,3, 2,2)
print()
print(MOMBmc)
MOMBmc.learn([
   np.array([1, 0, 1]), # mode 0
   np.array([1, 1, 0]) # mode 1
])
MOMBmc.output(np.array([[True, False], 
                        [False, True]] # sharing the same output since it is the same neuron
                       ))
MOMBmc.activate(np.array([[1, 0, 1]]), 0)
print(MOMBmc)
print(MOMBmc.fire(np.array([0, 1])))
print(MOMBmc)

MOMBmc.activate(np.array([[1, 1, 0]]), 1)
print(MOMBmc)
print(MOMBmc.fire(np.array([1, 1])))
print(MOMBmc)

MOMBmc.activate(np.array([[1, 1, 0]]), 0)
print(MOMBmc)
print(MOMBmc.fire(np.array([1, 1])))
print(MOMBmc)