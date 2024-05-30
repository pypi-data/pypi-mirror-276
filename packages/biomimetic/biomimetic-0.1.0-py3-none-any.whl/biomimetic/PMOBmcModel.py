import numpy as np
from biomimetic import ParallelMOBiomimeticCell


class ParallelMOBmcModel:
  def __init__(Model, name, data: dict):
    Model.name = name
    Model.data = data
    Model.datasetRows = len(data)
    Model.inputNums = len(next(iter(data.keys())))
    Model.featuresCount = len(next(iter(next(iter(data.keys())))))
    Model.outputSize = len(next(iter(data.values())))
    Model.datasetColumns = Model.featuresCount * Model.inputNums + Model.outputSize

  def learnModel(Model):
    Model.NeuralNetwork = []
    for index, (inputs, outputs) in enumerate(Model.data.items()):
      neuron = ParallelMOBiomimeticCell(index, len(inputs), Model.featuresCount, Model.outputSize, Model.featuresCount)
      neuron.learn(np.array(inputs))
      neuron.output(np.array(outputs))
      Model.NeuralNetwork.append(neuron)

  def __str__(Model):
    return f"PMOBmcModel({Model.name}, Rows: {Model.datasetRows}, Columns: {Model.datasetColumns}, Features: {Model.featuresCount}, Inputs: {Model.inputNums})"

  def activateModel(Model, inputValue: np.array):
    results = []
    for neuron in Model.NeuralNetwork:
      neuron.activate(inputValue)
      if all(neuron.activationFlags):
        return neuron.fire(True)
    if results:
      return results
    return np.full((Model.outputSize,), False)