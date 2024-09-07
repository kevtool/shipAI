import numpy as np

class Layer:
    def __init__(self, weights, biases):
        self.weights = weights
        self.biases = biases

    @staticmethod
    def setWeights(weights, biases):
        return Layer(weights, biases)

    @staticmethod
    def randomWeights(inputs, outputs):
        w = np.random.normal(0, 1, size=(inputs, outputs))
        b = np.random.normal(0, 1, size=(1, outputs))
        return Layer(w, b)

    def forward(self, input):
        # input: 1 * N
        return input @ self.weights + self.biases

class ReLu:
    def forward(self, input):
        return np.maximum(input, 0)

class NeuralNetwork:
    def __init__(self, inputs, layerlist, outputs):
        self.activation = ReLu()
        self.layers = self.create_layers(inputs, layerlist, outputs)

    def create_layers(self, inputs, layerlist, outputs):
        layers = []
        if len(layerlist) == 0:
            layers.append(Layer.randomWeights(inputs, outputs))
            return layers
        
        layers.append(Layer.randomWeights(inputs, layerlist[0]))
        for i in range(0, len(layerlist) - 1):
            layers.append(Layer.randomWeights(layerlist[i], layerlist[i + 1]))
        layers.append(Layer.randomWeights(layerlist[-1], outputs))
        return layers
    
    def import_layers():
        pass

    def forward(self, input):
        x = input
        for i, layer in enumerate(self.layers):
            x = layer.forward(x)
            if i < len(self.layers) - 1:
                x = self.activation.forward(x)

        return x

class Algorithm:
    def __init__(self):
        self.brain = NeuralNetwork(inputs=4, layerlist=[3], outputs=1)
        self.scores = []

    def get_action(self, input):
        action = self.brain.forward(input)
        return action
    
    def get_score(self, score):
        self.scores.append((self.brain, score))
        print(self.scores)

    def next_brain(self):
        self.brain = NeuralNetwork(inputs=4, layerlist=[3], outputs=1)