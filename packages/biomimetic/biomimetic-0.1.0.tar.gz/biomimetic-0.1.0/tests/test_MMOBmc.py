import numpy as np
from biomimetic import ModeMOBiomimeticCell


MMOBmc = ModeMOBiomimeticCell((1,1), 2, 3,2,3, 2)
print()
print(MMOBmc)
MMOBmc.learn([np.array([[True, False, True],
                       [True, False, False]]),
            np.array([[True, False, True],
                       [True, False, False]])])
MMOBmc.output(np.array([True, False]))
MMOBmc.activate(np.array([[True, False, True], 
                          [True, False, True]]), 0) # wrong index
print(MMOBmc)
print(MMOBmc.fire(True))
print(MMOBmc)
MMOBmc.activate(np.array([[True, False, True], 
                          [True, False, True]]), 1)
print(MMOBmc)
print(MMOBmc.fire(True))
print(MMOBmc)
MMOBmc.activate(np.array([[True, False, True],
                          [True, False, False]]), 0)
print(MMOBmc)
print(MMOBmc.fire(True))
print(MMOBmc)
MMOBmc.activate(np.array([[True, False, True],
                          [True, False, False]]), 1) # wrong index
print(MMOBmc)
print(MMOBmc.fire(True))
print(MMOBmc)

MMOBmc.output(np.array([True, True]))
MMOBmc.learn([np.array([[True, False, True],
                       [True, True, True]]
                      )])
MMOBmc.activate(np.array([[True, False, True], 
                          [True, False, True]]
                         ), 0)
print(MMOBmc)
print(MMOBmc.fire(True))
print(MMOBmc)

MMOBmc.activate(np.array([[True, False, True],
                          [True, True, True]]
                        ), 0)
print(MMOBmc)
print(MMOBmc.fire(True))
print(MMOBmc)