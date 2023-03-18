from enum import Enum

# functional syntax
Task = Enum('Task', ['FUNCTIONAL_DEPENDENCY', 'MULTIVALUED_DEPENDENCY', 'LOSSLESS_JOIN'])

class Query():
    """
    A class to represent the task the chase algorithm is chasing.

    Attributes
    ----------
    task : enum
        The task that this query represent.
    to_check : list
        A list of checks that the query needs to perform the task.

    Methods
    -------
    set_task(task)
        Sets the task for this query.
    add_check(check)
        Adds a check to the list.
    """

    def __init__(self):
        self.task = ""
        self.to_check = []

    def set_task(self, task):
        """Sets the task for this query."""

        self.task = task

    def add_check(self, check):
        """Adds a check the list."""

        self.to_check.append(check)

    def __str__(self):
        string = "QUERY\n"
        string += f"Task: {self.task}\n"
        string += f"Checking for: {self.to_check}\n"
        return string
