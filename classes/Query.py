from enum import Enum

# functional syntax
Task = Enum('Task', ['FUNCTIONAL_DEPENDENCY', 'MULTIVALUED_DEPENDENCY', 'LOSSLESS_JOIN'])

class Query():
    def __init__(self):
        self.task = ""
        self.to_check = []

    def set_task(self, task):
        self.task = task

    def add_check(self, check):
        self.to_check.append(check)

    def __str__(self):
        string = "QUERY\n"
        string += f"Task: {self.task}\n"
        string += f"Checking for: {self.to_check}\n"
        return string

