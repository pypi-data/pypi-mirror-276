import numpy as np
from biomimetic import ModeMMBiomimeticCell

MMMBmc = ModeMMBiomimeticCell((1,1), 3, 3,2,3, 2,2)
print()
print(MMMBmc)
MMMBmc.learn([np.array([[1, 0, 1],
                       [1, 1, 0],
                       [0, 0, 1]]
                      ),
            np.array([[0, 0, 0],
                       [1, 0, 0],
                       [0, 1, 1]]
                      )])
MMMBmc.output(np.array([[True, False],
                        [False, True]]
                       ))
MMMBmc.allocate({0: [0, 1],
                 1: [2]})
MMMBmc.activate(np.array([[1, 0, 1],
                          [1, 1, 0],
                          [0, 0, 1]]
                        ), 0)
print(MMMBmc)
print(MMMBmc.fire([True, True]))
print(MMMBmc)

MMMBmc.activate(np.array([[1, 0, 1],
                          [1, 1, 0],
                          [0, 0, 1]]
                        ), 1)
print(MMMBmc)
print(MMMBmc.fire([True, True]))
print(MMMBmc)

MMMBmc.activate(np.array([[0, 0, 0],
                          [1, 0, 0],
                          [0, 0, 1]]
                        ), 1)
print(MMMBmc)
print(MMMBmc.fire([True, True]))
print(MMMBmc)

MMMBmc.activate(np.array([[0, 0, 0],
                          [1, 0, 0],
                          [0, 0, 1]]
                        ), 0)
print(MMMBmc)
print(MMMBmc.fire([True, True]))
print(MMMBmc)

MMMBmc.activate(np.array([[1, 0, 1],
                          [1, 1, 0],
                          [0, 0, 1]]
                        ), 0)
print(MMMBmc)
print(MMMBmc.fire([True, True]))
print(MMMBmc)

MMMBmc.activate(np.array([[0, 0, 1],
                          [1, 0, 0],
                          [0, 0, 1]]
                        ), 0)
print(MMMBmc)
print(MMMBmc.fire([True, True]))
print(MMMBmc)

MMMBmc.activate(np.array([[1, 0, 1],
                          [1, 1, 0],
                          [0, 0, 1]]
                        ), 0)
print(MMMBmc)
print(MMMBmc.fire([False, True]))
print(MMMBmc)

MMMBmc.activate(np.array([[0, 0, 1],
                          [1, 0, 0],
                          [0, 0, 1]]
                        ), 1)
print(MMMBmc)
print(MMMBmc.fire([True, True]))
print(MMMBmc)