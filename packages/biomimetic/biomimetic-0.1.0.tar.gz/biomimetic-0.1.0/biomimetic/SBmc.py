import numpy as np


class SimpleBiomimeticCell:
  def __init__(Cell, index, inputSize, outputSize):
    Cell.index = index
    Cell.inputSize = inputSize
    Cell.outputSize = outputSize
    Cell.inputArray = np.zeros((1, inputSize))
    Cell.weightArray = np.zeros((1, inputSize))
    Cell.outputArray = np.zeros((1, outputSize))
    Cell.activationFlag = False

  def __str__(Cell):
    return f"SBmc({Cell.index}, {Cell.inputSize}, {Cell.outputSize}, {Cell.activationFlag})"

  def learn(Cell, featuresValue: np.array):
    Cell.weightArray = featuresValue

  def output(Cell, targetValue: np.array):
    Cell.outputArray = targetValue

  def activate(Cell, inputValue: np.array):
    Cell.inputArray = inputValue
    Cell.activationFlag = np.sum(np.sum(np.logical_not(np.logical_xor(Cell.inputArray, Cell.weightArray)),axis=1)==Cell.inputSize)>0
    if Cell.activationFlag == True:
      return Cell.outputArray != 0
    else:
      return np.zeros(Cell.outputArray.shape) != 0
   
