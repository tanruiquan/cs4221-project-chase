class Relation():
    def __init__(self, attributes=set(), functional_dependencies=[], multivalued_dependencies=[]):
        self.attributes = attributes
        self.functional_dependencies = functional_dependencies
        self.multivalued_dependencies = multivalued_dependencies

    def add_attribute(self, attr):
        self.attributes.add(attr)

    def add_functional_dependency(self, lhs, rhs):
        self.functional_dependencies.append([lhs, rhs])

    def add_multivalued_dependency(self, lhs, rhs):
        self.multivalued_dependencies.append([lhs, rhs])

    def __str__(self):
        string = "RELATION\n"
        string += f"Attributes: {self.attributes}\n"
        string += f"Functional dependencies: {self.functional_dependencies}\n"
        string += f"Multivalued dependencies: {self.multivalued_dependencies}\n"
        return string