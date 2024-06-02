import importlib
import sys

from python_compute_module.query_runner import QueryRunner


class ComputeModuleApp:
    def __init__(self):
        self.registered_functions = []


    def function(self, func):
        self.registered_functions.append(func)
        return func

    def run(self):
        QueryRunner(*self.registered_functions)
