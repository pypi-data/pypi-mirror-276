import numpy as np
from biomimetic import SimpleModeBiasBiomimeticCell


class SimpleModeBiasBmcModel:
  def __init__(Model, name, dataCube: np.array, featuresCount):
    Model.name = name
    Model.dataset = dataCube
    Model.featuresCount = featuresCount
    Model.outputsCount = featuresCount
    Model.datasetModes = dataCube.shape[0]
    Model.datasetRows = dataCube.shape[1]
    Model.datasetColumns = dataCube.shape[2]
    Model.features = dataCube[0:Model.datasetModes, 0:Model.datasetRows, 0:featuresCount]
    Model.targets = dataCube[0:Model.datasetModes, 0:Model.datasetRows, featuresCount:Model.datasetColumns]

  def __str__(Model):
    return f"SMBBmcModel({Model.name}, {Model.datasetModes}, {Model.datasetRows}, {Model.datasetColumns}, {Model.featuresCount})"

  def learnModel(Model):
    Model.NeuralNetwork = []
    Model.outputs = np.unique(Model.targets[0,:,:], axis = 0)
    Model.outputsCount = Model.outputs.shape[0]
    for neuron in range(0, Model.outputsCount):
      Model.NeuralNetwork.append(SimpleModeBiasBiomimeticCell((1, neuron), Model.features.shape[1], Model.targets.shape[1], Model.datasetRows, Model.datasetModes))
      selectedMode = []
      for mode in Model.dataset:
        selectedFeatures = []
        for row in mode:
          if row[Model.featuresCount:Model.datasetColumns] == Model.outputs[neuron,:]:
            selectedFeatures.append(row[0:Model.featuresCount])
        selectedMode.append(selectedFeatures)
      Model.NeuralNetwork[neuron].learn(selectedMode)
      Model.NeuralNetwork[neuron].output(Model.outputs[neuron,:])

  def activateModel(Model, inputValue: np.array, modeValue):
    for neuron in range(0, Model.outputsCount):
      Model.NeuralNetwork[neuron].activate(inputValue, modeValue)
      Model.output = Model.NeuralNetwork[neuron].fire(True)
      if Model.NeuralNetwork[neuron].activationFlag == True and Model.NeuralNetwork[neuron].fireFlag == True:
        return Model.output
    return np.zeros(Model.output.shape) != 0