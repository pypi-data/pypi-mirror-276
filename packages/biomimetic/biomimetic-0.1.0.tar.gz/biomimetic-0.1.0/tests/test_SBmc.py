import numpy as np
from biomimetic import SimpleBiomimeticCell

BMC = SimpleBiomimeticCell((1,1),8,8)
BMC.learn(np.array([[True, False, True, False, True, False, True, False]]))
BMC.output(np.array([True, True, True, True, False, False, False, False]))

print(BMC)
print(BMC.activate(np.array([True, False, True, False, True, False, True, False])))
print(BMC)
print(BMC.activate(np.array([False, False, True, False, True, False, True, False])))
print(BMC)


BMC_Xor10 = SimpleBiomimeticCell((1,1), 2, 1)
BMC_Xor01 = SimpleBiomimeticCell((1,2), 2, 1)
BMC_Xor10.learn(np.array([[1,0]]))
BMC_Xor01.learn(np.array([[0,1]]))
BMC_Xor10.output(np.array([1]))
BMC_Xor01.output(np.array([1]))

print(BMC_Xor10)
print(BMC_Xor10.activate(np.array([1,0])))
print(BMC_Xor01)
print(BMC_Xor01.activate(np.array([0,1])))