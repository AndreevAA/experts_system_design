from fuzzyset import *
from mathlb import *

class FuzzyRule:
    def __init__(self, inputs: dict[str, FuzzySet], output_label: str, output_set: FuzzySet):
        self.inputs = inputs
        self.output_label = output_label
        self.output_set = output_set

    def evaluate(self, variable_name: str, value: float):
        if variable_name not in self.inputs:
            return 0

        return self.inputs[variable_name].calculate_membership(value)

    def output_function(self, minimal_value: float):
        def constant_function(x):
            return minimal_value

        return Math().minimum_function([self.output_set.calculate_membership, constant_function])

    def __repr__(self):
        return "{:} -> {:}={:}".format(
            " & ".join(["{:}={:}".format(var, self.inputs[var].label) for var in self.inputs]),
            self.output_label,
            self.output_set.label,
        )


