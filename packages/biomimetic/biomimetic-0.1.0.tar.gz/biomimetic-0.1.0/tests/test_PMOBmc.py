import numpy as np
from biomimetic import ParallelMOBiomimeticCell


PMOBmc = ParallelMOBiomimeticCell((1,1), 2, 3,2,3)
print()
print(PMOBmc)
PMOBmc.learn(np.array([[True, False, True],
                       [True, False, False]]
                      ))
PMOBmc.output(np.array([True, False]))
PMOBmc.activate(np.array([[True, False, True], 
                          [True, False, True]]
                         ))
print(PMOBmc)
print(PMOBmc.fire(True))
print(PMOBmc)

PMOBmc.output(np.array([True, True]))
PMOBmc.learn(np.array([[True, False, True],
                       [True, True, True]]
                      ))
PMOBmc.activate(np.array([[True, False, True], 
                          [True, False, True]]
                         ))
print(PMOBmc)
print(PMOBmc.fire(True))
print(PMOBmc)

PMOBmc.activate(np.array([[True, False, True],
                          [True, True, True]]
                        ))
print(PMOBmc)
print(PMOBmc.fire(True))
print(PMOBmc)