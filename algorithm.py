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
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.activation = ReLu()

    def create_layers(self, layerlist):
        self.layers = []
        if len(layerlist) == 0:
            self.layers.append(Layer.randomWeights(self.inputs, self.outputs))
            return
        
        self.layers.append(Layer.randomWeights(self.inputs, layerlist[0]))
        for i in range(0, len(layerlist) - 1):
            self.layers.append(Layer.randomWeights(layerlist[i], layerlist[i + 1]))
        self.layers.append(Layer.randomWeights(layerlist[-1], self.outputs))
    
    def mutate_layers(self, layers):
        self.layers = layers
        for layer in self.layers:
            shape = layer.weights.shape
            mutation = np.random.uniform(-0.05, 0.05, shape)
            layer.weights += (layer.weights * mutation)

            shape = layer.biases.shape
            mutation = np.random.uniform(-0.05, 0.05, shape)
            layer.biases += (layer.biases * mutation)

    @classmethod
    def create(cls, inputs, layerlist, outputs):
        obj = cls(inputs, outputs)
        obj.create_layers(layerlist)
        return obj

    @classmethod
    def mutate(cls, nn):
        obj = cls(nn.inputs, nn.outputs)
        obj.mutate_layers(nn.layers)
        return obj

    @classmethod
    def copy(cls, nn):
        obj = cls(nn.inputs, nn.outputs)
        obj.layers = nn.layers
        return obj

    def forward(self, input):
        x = input
        for i, layer in enumerate(self.layers):
            x = layer.forward(x)
            if i < len(self.layers) - 1:
                x = self.activation.forward(x)

        return x

class Algorithm:
    def __init__(self, brains_per_gen):
        self.brains = [NeuralNetwork.create(inputs=4, layerlist=[3], outputs=1) for _ in range(brains_per_gen)]
        self.scores = []
    
    # changes: get the number of direction changes
    def record_score(self, index, score, changes):
        self.scores.append((index, score, changes))
        print(self.scores)

    def create_new_gen(self, num_of_descendants):
        INDEX = 0

        # sort by second element (score)
        self.scores = sorted(self.scores, key=lambda x: (x[0], x[1]))
        qualified_brains = sum(1 for tpl in self.scores if tpl[2] == 0)
        denom = sum(i ** -0.8 for i in range(1, qualified_brains+1))

        new_brains = []

        for i in range(qualified_brains):
            descendants = round(((i+1) ** -0.8) / denom, 1) * num_of_descendants
            index = self.scores[i][INDEX]
            brain_to_reproduce = self.brains[index]
            print(index)
            
            for j in range(descendants):
                if j == 0:
                    new_brains.append(NeuralNetwork.copy(brain_to_reproduce.nn))
                else:
                    new_brains.append(NeuralNetwork.mutate(brain_to_reproduce.nn))

        assert len(new_brains) == num_of_descendants
        self.brains = new_brains