import numpy as np
from biomimetic import ParallelMMBiomimeticCell


class ParallelMMBmcModel:
  def __init__(Model, name, data: dict):
    Model.name = name
    Model.data = data
    Model.datasetRows = len(data)
    Model.inputNums = len(next(iter(data.keys())))
    Model.outputNums = len(next(iter(data.values())))
    Model.featuresCount = len(next(iter(next(iter(data.keys())))))
    Model.outputSize = len(next(iter(next(iter(data.values())))))
    Model.datasetColumns = Model.featuresCount * Model.inputNums + Model.outputSize * Model.outputNums

  def learnModel(Model, PMMBmcModelDataSetAllocations):
    Model.NeuralNetwork = []
    for index, (inputs, outputs) in enumerate(Model.data.items()):
      neuron = ParallelMMBiomimeticCell(index=(1, index), inputNums=len(inputs), inputSize=Model.featuresCount, outputSize=len(outputs[0]), outputNums=Model.outputNums, weightSize=Model.featuresCount)
      neuron.learn(np.array(inputs))
      neuron.allocate(PMMBmcModelDataSetAllocations)
      neuron.output(np.array(outputs))
      Model.NeuralNetwork.append(neuron)

  def __str__(Model):
    return f"PMMBmcModel({Model.name}, Rows: {Model.datasetRows}, Columns: {Model.datasetColumns}, Features: {Model.featuresCount}, Inputs: {Model.inputNums}, Outputs: {Model.outputNums})"

  def activateModel(Model, inputValue: np.array):
    results = []
    for neuron in Model.NeuralNetwork:
      neuron.activate(inputValue)
      fireBiases = np.ones(shape=Model.outputNums, dtype=bool)
      for output_index, input_indices in neuron.allocationDict.items():
        if all(neuron.activationFlags[input_indices]):
          continue
        else:
          fireBiases[output_index] = False
      results.append(neuron.fire(fireBiases))
    if results:
      return results
    return np.full((Model.outputSize,), False)