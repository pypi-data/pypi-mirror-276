import numpy as np


class SimpleBiasBiomimeticCell:
  def __init__(Cell, index, inputSize, outputSize, weightSize):
    Cell.index = index
    Cell.inputSize = inputSize
    Cell.outputSize = outputSize
    Cell.weightSize = weightSize
    Cell.inputArray = np.zeros((1, inputSize))
    Cell.weightArray = np.zeros((weightSize, inputSize))
    Cell.outputArray = np.zeros((1, outputSize))
    Cell.activationFlag = False
    Cell.fireFlag = False

  def __str__(Cell):
    return f"SBBmc({Cell.index}, {Cell.inputSize}, {Cell.outputSize}, {Cell.weightSize}, {Cell.activationFlag}, {Cell.fireFlag})"

  def learn(Cell, featuresValues: np.array):
    Cell.weightArray = featuresValues

  def output(Cell, targetValues: np.array):
    Cell.outputArray = targetValues

  def activate(Cell, inputValue: np.array):
    Cell.inputArray = inputValue
    Cell.activationFlag = np.sum(np.sum(np.logical_not(np.logical_xor(Cell.inputArray, Cell.weightArray)), axis = 1) == Cell.inputSize) > 0

  def fire(Cell, fireBias: bool):
    Cell.fireFlag = fireBias
    if Cell.activationFlag == True and Cell.fireFlag == True:
      return Cell.outputArray != 0
    else:
      return np.zeros(Cell.outputArray.shape) != 0