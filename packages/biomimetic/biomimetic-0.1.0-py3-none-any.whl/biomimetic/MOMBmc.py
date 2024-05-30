import numpy as np


class ModeOMBiomimeticCell:
    def __init__(Cell, index, inputSize, outputSize, weightSize, modeCount, outputNums):
        Cell.index = index
        Cell.inputSize = inputSize
        Cell.outputSize = outputSize
        Cell.weightSize = weightSize
        Cell.outputNums = outputNums
        Cell.modeCount = modeCount
        Cell.inputArray = np.zeros((1, inputSize))
        Cell.weightArrays = np.zeros((modeCount, weightSize, inputSize))
        Cell.outputArrays = np.zeros((outputNums, outputSize))
        Cell.activationFlag = False
        Cell.fireFlags = np.zeros(outputNums, dtype=bool)

    def __str__(Cell):
        return f"MOMBmc({Cell.index}, {Cell.inputSize}, {Cell.outputSize}, {Cell.weightSize}, {Cell.outputNums}, {Cell.activationFlag}, {Cell.fireFlags})"

    def learn(Cell, featuresValues):
        Cell.weightArrays = featuresValues

    def output(Cell, targetValues):
        Cell.outputArrays = targetValues

    def activate(Cell, inputValue:np.array, modeValue):
        Cell.inputArray = inputValue
        Cell.weightArraySheet = Cell.weightArrays[modeValue]
        Cell.activationFlag = np.sum(
            np.sum(
                np.logical_not(
                    np.logical_xor(
                        Cell.inputArray, Cell.weightArraySheet)
                    ), axis=1
                ) == Cell.inputSize) > 0

    def fire(Cell, fireBiases):
        Cell.fireFlags = fireBiases
        if Cell.activationFlag == True:
            return np.where(Cell.fireFlags[:, None], Cell.outputArrays, np.zeros_like(Cell.outputArrays))
        else:
            return np.zeros((Cell.outputNums, Cell.outputSize), dtype=bool)