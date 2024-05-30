import numpy as np
from biomimetic import ParallelMMBiomimeticCell


PMMBmc = ParallelMMBiomimeticCell((1,1), 3, 3,2,3, 2)
print()
print(PMMBmc)
PMMBmc.learn(np.array([[1, 0, 1],
                       [1, 1, 0],
                       [0, 0, 1]]
                      ))
PMMBmc.output(np.array([[True, False],
                        [False, True]]
                       ))
PMMBmc.allocate({0: [0, 1],
                 1: [2]})
PMMBmc.activate(np.array([[1, 0, 1],
                          [1, 1, 0],
                          [0, 0, 1]]
                        ))
print(PMMBmc)
print(PMMBmc.fire([True, True]))
print(PMMBmc)

PMMBmc.activate(np.array([[1, 0, 1],
                          [1, 1, 0],
                          [0, 0, 1]]
                        ))
print(PMMBmc)
print(PMMBmc.fire([True, True]))
print(PMMBmc)

PMMBmc.activate(np.array([[0, 0, 1],
                          [1, 0, 0],
                          [0, 0, 1]]
                        ))
print(PMMBmc)
print(PMMBmc.fire([True, True]))
print(PMMBmc)

PMMBmc.activate(np.array([[1, 0, 1],
                          [1, 1, 0],
                          [0, 0, 1]]
                        ))
print(PMMBmc)
print(PMMBmc.fire([False, True]))
print(PMMBmc)