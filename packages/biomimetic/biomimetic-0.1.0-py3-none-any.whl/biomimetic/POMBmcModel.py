import numpy as np
from biomimetic import ParallelOMBiomimeticCell



class ParallelOMBmcModel:
    def __init__(Model, name, data: dict):
        Model.name = name
        Model.data = data
        Model.datasetRows = len(data)
        Model.outputNums = len(next(iter(data.values()))[0])
        Model.featuresCount = len(next(iter(data.keys())))
        Model.datasetColumns = Model.featuresCount + Model.outputNums * len(next(iter(next(iter(data.values())))))

    def learnModel(Model):
        Model.NeuralNetwork = []
        for index, (inputs, outputs) in enumerate(Model.data.items()):
            neuron = ParallelOMBiomimeticCell(index, Model.featuresCount, len(outputs[0]), Model.featuresCount, len(outputs))
            neuron.learn(np.array(inputs))
            neuron.output(np.array(outputs))
            Model.NeuralNetwork.append(neuron)

    def __str__(Model):
        return f"POMBmcModel({Model.name}, Rows: {Model.datasetRows}, Columns: {Model.datasetColumns}, Features: {Model.featuresCount}, Outputs: {Model.outputNums})"

    def activateModel(Model, inputValue):
        results = []
        inputValue = np.array([inputValue])
        for neuron in Model.NeuralNetwork:
            neuron.activate(inputValue)
            if neuron.activationFlag:
                return neuron.fire(np.ones(len(neuron.outputArrays), dtype=bool))
        if results:
            return results
        return np.full((Model.outputNums, len(next(iter(Model.data.values()))[0])), False)