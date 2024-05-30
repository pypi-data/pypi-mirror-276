import numpy as np


class ParallelOMBiomimeticCell:
    def __init__(Cell, index, inputSize, outputSize, weightSize, outputNums):
        Cell.index = index
        Cell.inputSize = inputSize
        Cell.outputSize = outputSize
        Cell.weightSize = weightSize
        Cell.outputNums = outputNums
        Cell.inputArray = np.zeros((1, inputSize))
        Cell.weightArray = np.zeros((weightSize, inputSize))
        Cell.outputArrays = np.zeros((outputNums, outputSize))
        Cell.activationFlag = False
        Cell.fireFlags = np.zeros(outputNums, dtype=bool)

    def __str__(Cell):
        return f"POMBmc({Cell.index}, {Cell.inputSize}, {Cell.outputSize}, {Cell.weightSize}, {Cell.outputNums}, {Cell.activationFlag}, {Cell.fireFlags})"

    def learn(Cell, featuresValues: np.array):
        Cell.weightArray = featuresValues

    def output(Cell, targetValues: np.array):
        Cell.outputArrays = targetValues

    def activate(Cell, inputValue: np.array):
        Cell.inputArray = inputValue
        Cell.activationFlag = np.sum(
            np.sum(
                np.logical_not(
                    np.logical_xor(
                        Cell.inputArray, Cell.weightArray)
                    ), axis=1
                ) == Cell.inputSize) > 0

    def fire(Cell, fireBiases):
        Cell.fireFlags = fireBiases
        if Cell.activationFlag == True:
            return np.where(Cell.fireFlags[:, None], Cell.outputArrays, np.zeros_like(Cell.outputArrays))
        else:
            return np.zeros((Cell.outputNums, Cell.outputSize), dtype=bool)