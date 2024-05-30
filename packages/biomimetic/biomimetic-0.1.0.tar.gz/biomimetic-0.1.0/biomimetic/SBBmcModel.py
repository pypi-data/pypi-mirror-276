import numpy as np
from biomimetic import SimpleBiasBiomimeticCell


class SimpleBiasBmcModel:
  def __init__(Model, name, dataTable: np.array, featuresCount):
    Model.name = name
    Model.dataset = dataTable
    Model.featuresCount = featuresCount
    Model.outputsCount = featuresCount
    Model.datasetRows = dataTable.shape[0]
    Model.datasetColumns = dataTable.shape[1]
    Model.features = dataTable[0:Model.datasetRows, 0:featuresCount]
    Model.targets = dataTable[0:Model.datasetRows, featuresCount:Model.datasetColumns]

  def __str__(Model):
    return f"SBBmcModel({Model.name}, {Model.datasetRows}, {Model.datasetColumns}, {Model.featuresCount})"

  def learnModel(Model):
    Model.NeuralNetwork = []
    Model.outputs = np.unique(Model.targets, axis = 0)
    Model.outputsCount = Model.outputs.shape[0]
    for neuron in range(0, Model.outputsCount):
      Model.NeuralNetwork.append(SimpleBiasBiomimeticCell((1, neuron), Model.features.shape[1], Model.targets.shape[1], Model.datasetRows))
      selectedFeatures = []
      for row in Model.dataset:
        if row[Model.featuresCount:Model.datasetColumns] == Model.outputs[neuron,:]:
          selectedFeatures.append(row[0:Model.featuresCount])
      Model.NeuralNetwork[neuron].learn(selectedFeatures)
      Model.NeuralNetwork[neuron].output(Model.outputs[neuron,:])

  def activateModel(Model, inputValue: np.array):    
    for neuron in range(0, Model.outputsCount):
      Model.NeuralNetwork[neuron].activate(inputValue)
      Model.output = Model.NeuralNetwork[neuron].fire(True)
      if Model.NeuralNetwork[neuron].activationFlag == True and Model.NeuralNetwork[neuron].fireFlag == True:
        return Model.output
    return np.zeros(Model.output.shape) != 0