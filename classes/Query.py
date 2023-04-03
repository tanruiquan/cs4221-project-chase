class Query():
    """
    A class to represent the task the chase algorithm is chasing.

    Attributes
    ----------
    task : str
        The task that this query represent.
    functional_dependencies : list
        A list of functional dependencies for entailment and minimal
        cover queries.
    multivalued_dependencies : list
        A list of multivalued dependencies for entailment and minimal
        cover queries.
    relations : list
        A list of relations for lossless join queries.

    Methods
    -------
    set_task(task)
        Sets the task for this query.
    add_functional_dependency(lhs, rhs)
        Adds a functional dependency, lhs -> rhs, to the list of 
        functional dependencies needed for the query.
    add_multivalued_dependency(lhs, rhs)
        Adds a multivalued dependency, lhs ->> rhs, to the list of
        multivalued dependencies needed for the query.
    add_relation(relation)
        Adds a relation to the list of relations needed for the query.
    """

    def __init__(self, task=None, functional_dependencies=None, multivalued_dependencies=None, relations=None):
        if functional_dependencies is None:
            functional_dependencies = []
        if multivalued_dependencies is None:
            multivalued_dependencies = []
        if relations is None:
            relations = []
        self.task = task
        self.functional_dependencies = functional_dependencies
        self.multivalued_dependencies = multivalued_dependencies
        self.relations = relations

    def set_task(self, task):
        """Sets the task for this query."""

        self.task = task

    def add_functional_dependency(self, lhs, rhs):
        """Adds a functional dependency, lhs -> rhs, to the list of
        functional dependencies.

        The functional dependencies are are used for entailment and
        minimal cover queries. If the functional dependency already
        exists, it will not be added. As a side effect, the lhs and
        rhs will be sorted.

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
        multivalued dependencies.

        The multivalued dependencies are are used for entailment and
        minimal cover queries. If the multivalued dependency already
        exists, it will not be added. As a side effect, the lhs and
        rhs will be sorted.

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

    def add_relation(self, relation):
        """Adds a relation to the list of relations.

        The relations are used for lossless join queries.

        Parameters
        ----------
        relation : Relation
            The relation to be added.
        """

        if relation in self.relations:
            return
        self.relations.append(relation)

    def __str__(self):
        """String representation of `Query` for debugging."""

        string = f"Query type: {self.task}\n"
        string += "Functional Dependencies:\n"
        for lhs, rhs in self.functional_dependencies:
            string += f'  {lhs} -> {rhs}\n'
        string += "Multivalued Dependencies\n"
        for lhs, rhs in self.multivalued_dependencies:
            string += f'  {lhs} ->> {rhs}\n'
        string += "Relations:\n"
        for relation in self.relations:
            string += f"  {str(relation)}"
        return string
