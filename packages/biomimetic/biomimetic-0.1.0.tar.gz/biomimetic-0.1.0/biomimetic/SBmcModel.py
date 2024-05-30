import numpy as np
from biomimetic import SimpleBiomimeticCell


class SimpleBmcModel:
  def __init__(Model, name, dataTable: np.array, featuresCount):
    Model.name = name
    Model.dataset = dataTable
    Model.featuresCount = featuresCount
    Model.datasetRows = dataTable.shape[0]
    Model.datasetColumns = dataTable.shape[1]
    Model.features = dataTable[0:Model.datasetRows, 0:featuresCount]
    Model.targets = dataTable[0:Model.datasetRows, featuresCount:Model.datasetColumns]

  def __str__(Model):
    return f"SBmcModel({Model.name}, {Model.datasetRows}, {Model.datasetColumns}, {Model.featuresCount})"

  def learnModel(Model):
    Model.NeuralNetwork = []
    for neuron in range(0, Model.datasetRows):
      Model.NeuralNetwork.append(SimpleBiomimeticCell((1, neuron),Model.features.shape[1],Model.targets.shape[1]))
      Model.NeuralNetwork[neuron].learn(Model.features[neuron])
      Model.NeuralNetwork[neuron].output(Model.targets[neuron])

  def activateModel(Model, inputValue: np.array):
    for neuron in range(0, Model.datasetRows):
      Model.output = Model.NeuralNetwork[neuron].activate(inputValue)
      if Model.NeuralNetwork[neuron].activationFlag == True:
        return Model.output
    return np.zeros(Model.output.shape) != 0