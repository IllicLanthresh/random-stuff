class Neuron:
    def __init__(self):
        self.inputs = []
        self.weights = []
        self.bias = 0

    @property
    def output(self):
        return sum([i*w for i, w in zip(self.inputs, self.weights)]) + self.bias


class Layer:
    size = 0
    inputs = []
    weights = [
        [],
    ]
    biases = []

    @property
    def outputs(self):
        outputs = []
        for _ in range(self.size):

