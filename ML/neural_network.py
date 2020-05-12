import typing


class Layer:
    _input = None
    sets_of_weights = [
        [],
    ]
    biases = []

    @property
    def inputs(self) -> typing.List[float]:
        if isinstance(self._input, Layer):
            return self._input.outputs
        elif isinstance(self._input, list):
            return self._input

    @inputs.setter
    def inputs(self, inputs):
        if isinstance(inputs, Layer):
            
        elif isinstance(inputs, list):


    @property
    def outputs(self) -> typing.List[float]:
        outputs = []
        for weights_set, bias in zip(self.sets_of_weights, self.biases):
            outputs.append(sum([i*w for i, w in zip(self.inputs, weights_set)]) + bias)
        return outputs
