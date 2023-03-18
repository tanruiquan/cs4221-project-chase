class Relation():
    """
    A class used to represent a relational schema and its associated
    dependencies.

    Attributes
    ----------
    attributes : set
        A set of attributes of the relation.
    functional_dependencies : list
        A list of functional dependencies on the relation.
    multivalued_dependencies : list
        A list of multivalued dependencies on the relation.

    Methods
    -------
    add_attribute(attr)
        Adds the given attribute to the relation.
    add_functional_dependency(lhs, rhs)
        Adds a functional dependency, lhs -> rhs, to the list of 
        functional dependencies on the relation.
    add_multivalued_dependency(lhs, rhs)
        Adds a multivalued dependency, lhs ->> rhs, to the list of
        multivalued dependencies on the relation.
    """

    def __init__(self, attributes=None, functional_dependencies=None, multivalued_dependencies=None):
        """
        Parameters
        ----------
        attributes : set, optional
            A set of attributes of the relation (default is empty set).
        functional_dependencies : list, optional
            A list of functional dependencies on the relation (default is empty list).
        multivalued_dependencies : list, optional
            A list of multivalued dependencies on the relation (default is empty list).
        """

        if attributes is None:
            attributes = set()
        if functional_dependencies is None:
            functional_dependencies = []
        if multivalued_dependencies is None:
            multivalued_dependencies = []
        self.attributes = attributes
        self.functional_dependencies = functional_dependencies
        self.multivalued_dependencies = multivalued_dependencies

    def add_attribute(self, attr):
        """Adds the given attribute to the relation.

        If the attribute already exists, it will not be added.

        Parameters
        ----------
        attr : str
            The attribute to be added.
        """

        self.attributes.add(attr)

    def add_functional_dependency(self, lhs, rhs):
        """Adds a functional dependency, lhs -> rhs, to the list of
        functional dependencies on the relation.
        
        If the functional dependency already exists, it will not be 
        added. As a side effect, the lhs and rhs will be sorted.

        Parameters
        ----------
        lhs : list
            The left-hand side of the functional dependency.
        rhs : list
            The right-hand side of the functional dependency.
        """

        lhs.sort()
        rhs.sort()
        fd = [lhs, rhs]
        if fd in self.functional_dependencies:
            return
        self.functional_dependencies.append(fd)

    def add_multivalued_dependency(self, lhs, rhs):
        """Adds a multivalued dependency, lhs ->> rhs, to the list of
        multivalued dependencies on the relation.
        
        If the multivalued dependency already exists, it will not be 
        added. As a side effect, the lhs and rhs will be sorted.

        Parameters
        ----------
        lhs : list
            The left-hand side of the multivalued dependency.
        rhs : list
            The right-hand side of the multivalued dependency.
        """

        lhs.sort()
        rhs.sort()
        mvd = [lhs, rhs]
        if mvd in self.multivalued_dependencies:
            return
        self.multivalued_dependencies.append(mvd)

    def __str__(self):
        string = "RELATION\n"
        string += f"Attributes: {self.attributes}\n"
        string += f"Functional dependencies: {self.functional_dependencies}\n"
        string += f"Multivalued dependencies: {self.multivalued_dependencies}\n"
        return string
