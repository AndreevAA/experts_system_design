import numpy as np
import matplotlib.pyplot as plt

class FuzzySet:
    def __init__(self, label, membership_func):
        self.label = label
        self.membership_func = membership_func

    def calculate_membership(self, value):
        return self.membership_func(value)

