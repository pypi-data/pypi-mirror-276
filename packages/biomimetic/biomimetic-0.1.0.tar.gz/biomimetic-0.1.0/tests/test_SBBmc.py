import numpy as np
from biomimetic import SimpleBiasBiomimeticCell


NN = []
operation = np.array([[0,0,0],[0,0,1],[1,0,0],[1,0,1],[0,1,0],[0,1,1],[1,1,0],[1,1,1]])
result = np.array([[0,0],[0,1],[0,1],[1,0],[0,0],[1,1],[0,1],[0,0]])

for i in range(1,9):
  NN.append(SimpleBiasBiomimeticCell((1,i),3,2,1))

for i in range(1,9):
  NN[i-1].learn(operation[i-1])
  NN[i-1].output(result[i-1])

input = [[1,0,1]]
outputFinal = np.array([False, False])
for i in range(1,9):
  NN[i-1].activate(input)
  print(NN[i-1])
  outputFinal = np.logical_or(outputFinal , NN[i-1].fire(True))

print(outputFinal)


NNs = []
operation1 = np.array([[0,0,0],[0,1,0],[1,1,1]])
operation2 = np.array([[0,0,1],[1,0,0],[1,1,0]])
operation3 = np.array([[1,0,1]])
operation4 = np.array([[0,1,1]])
result = np.array([[0,0],[0,1],[1,0],[1,1]])

NNs.append(SimpleBiasBiomimeticCell((1,1),3,2,3))
NNs.append(SimpleBiasBiomimeticCell((1,2),3,2,3))
NNs.append(SimpleBiasBiomimeticCell((1,3),3,2,1))
NNs.append(SimpleBiasBiomimeticCell((1,4),3,2,1))

NN[0].learn(operation1)
NN[1].learn(operation2)
NN[2].learn(operation3)
NN[3].learn(operation4)

for i in range(1,5):
  NN[i-1].output(result[i-1])

input = [[0,1,1]]
outputFinal = np.array([False, False])
for i in range(1,5):
  NN[i-1].fire(False)
  NN[i-1].activate(input)
  print(NN[i-1])
  outputFinal = np.logical_or(outputFinal , NN[i-1].fire(True))

print(outputFinal)

input = [[1,0,1]]
outputFinal = np.array([False, False])
for i in range(1,5):
  NN[i-1].fire(False)
  NN[i-1].activate(input)
  print(NN[i-1])
  outputFinal = np.logical_or(outputFinal , NN[i-1].fire(True))

print(outputFinal)