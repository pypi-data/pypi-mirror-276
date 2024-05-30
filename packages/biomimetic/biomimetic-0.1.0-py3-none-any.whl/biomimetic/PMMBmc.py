import numpy as np


class ParallelMMBiomimeticCell:
  def __init__(Cell, index, inputNums, inputSize, outputSize, weightSize, outputNums):
    Cell.index = index
    Cell.inputNums = inputNums
    Cell.inputSize = inputSize
    Cell.outputSize = outputSize
    Cell.weightSize = weightSize
    Cell.outputNums = outputNums
    Cell.inputArrays = np.zeros((inputNums, inputSize))
    Cell.weightArray = np.zeros((weightSize, inputSize))
    Cell.allocationDict = {}
    Cell.outputArrays = np.zeros((outputNums, outputSize))
    Cell.activationFlags = np.zeros(inputNums, dtype=bool)
    Cell.fireFlags = np.zeros(outputNums, dtype=bool)
    
  def __str__(Cell):
    return f"PMMBmc({Cell.index}, {Cell.inputNums}, {Cell.inputSize}, {Cell.outputSize}, {Cell.weightSize}, {Cell.outputNums}, {Cell.activationFlags}, {Cell.fireFlags})"

  def learn(Cell, featuresValues: np.array):
    Cell.weightArray = featuresValues

  def output(Cell, targetValues: np.array):
    Cell.outputArrays = targetValues
    
  def allocate(Cell, allocations: dict):
    Cell.allocationDict = allocations

  def activate(Cell, inputValue: np.array):
    Cell.inputArrays = inputValue
    Cell.activationFlags = np.array([
            np.all(np.logical_not(np.logical_xor(Cell.inputArrays[i], Cell.weightArray[i])))
            for i in range(Cell.inputNums)
        ])

  def fire(Cell, fireBiases): # fireBiases: boolean list
    Cell.fireFlags = fireBiases
    output_results = np.zeros_like(Cell.outputArrays)
    for output_index, input_indices in Cell.allocationDict.items():
      if Cell.fireFlags[output_index] and all(Cell.activationFlags[input_indices]):
        output_results[output_index] = Cell.outputArrays[output_index] != 0
      else:
        output_results[output_index] = np.zeros(Cell.outputArrays[output_index].shape) != 0
    return output_results