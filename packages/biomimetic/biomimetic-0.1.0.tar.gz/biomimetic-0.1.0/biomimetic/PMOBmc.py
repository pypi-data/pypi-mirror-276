import numpy as np


class ParallelMOBiomimeticCell:
  def __init__(Cell, index, inputNums, inputSize, outputSize, weightSize):
    Cell.index = index
    Cell.inputNums = inputNums
    Cell.inputSize = inputSize
    Cell.outputSize = outputSize
    Cell.weightSize = weightSize
    Cell.inputArrays = np.zeros((inputNums, inputSize))
    Cell.weightArray = np.zeros((weightSize, inputSize))
    Cell.outputArray = np.zeros((1, outputSize))
    Cell.activationFlags = np.zeros(inputNums, dtype=bool)
    Cell.fireFlag = False

  def __str__(Cell):
    return f"PMOBmc({Cell.index}, {Cell.inputNums}, {Cell.inputSize}, {Cell.outputSize}, {Cell.weightSize}, {Cell.activationFlags}, {Cell.fireFlag})"

  def learn(Cell, featuresValues: np.array):
    Cell.weightArray = featuresValues

  def output(Cell, targetValues: np.array):
    Cell.outputArray = targetValues

  def activate(Cell, inputValue: np.array):
    Cell.inputArrays = inputValue
    Cell.activationFlags = np.array([
            np.all(np.logical_not(np.logical_xor(Cell.inputArrays[i], Cell.weightArray[i])))
            for i in range(Cell.inputNums)
        ])

  def fire(Cell, fireBias: bool):
    Cell.fireFlag = fireBias
    if Cell.fireFlag == True and all(Cell.activationFlags) == True:
        return Cell.outputArray != 0
    else:
      return np.zeros(Cell.outputArray.shape) != 0