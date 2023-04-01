import xml.etree.ElementTree as ET
from classes.Relation import Relation
from classes.Query import Query


class XMLIO:
    """
    A class used to represent an xml file reader and writer.

    Attributes
    ----------
    input : str
        A string representing the input filename or path.
    output : str
        A string representing the outpu tfilename or path.
    """

    def __init__(self, input, output):
        self.input = input
        self.output = output

    def get_relation(self, root):
        """Returns the `Relation` data structure."""

        # Extract the table name and its attributes
        table_name = root.find('table').get('name')
        attributes = [elem.text for elem in root.find(
            'table').findall('attribute')]

        relation = Relation(table_name, attributes)

        for fd in root.findall('table/functional_dependency'):
            lhs = [elem.text for elem in fd.find("lhs")]
            rhs = [elem.text for elem in fd.find("rhs")]
            relation.add_functional_dependency(lhs, rhs)

        for mvd in root.findall('table/multivalued_dependency'):
            lhs = [elem.text for elem in mvd.find("lhs")]
            rhs = [elem.text for elem in mvd.find("rhs")]
            relation.add_multivalued_dependency(lhs, rhs)

        return relation

    def get_query(self, root):
        # Extract the dependency check type and tables
        check_type = root.find('dependency_check').get('type')

        query = Query(check_type)

        for fd in root.findall('dependency_check/functional_dependency'):
            lhs = [elem.text for elem in fd.find("lhs")]
            rhs = [elem.text for elem in fd.find("rhs")]
            query.add_functional_dependency(lhs, rhs)

        for mvd in root.findall('dependency_check/multivalued_dependency'):
            lhs = [elem.text for elem in mvd.find("lhs")]
            rhs = [elem.text for elem in mvd.find("rhs")]
            query.add_multivalued_dependency(lhs, rhs)

        for table in root.findall('dependency_check/table'):
            table_name = table.get('name')
            table_attributes = [
                elem.text for elem in table.findall('attribute')]
            query.add_relation(Relation(table_name, table_attributes))

        return query

    def read_xml(self):
        """Reads an xml file and returns 2 objects: `Relation` and `Query`
        which represents the relational table and task that we are chasing
        respectively."""

        tree = ET.parse(self.input)
        root = tree.getroot()
        relation = self.get_relation(root)
        query = self.get_query(root)
        print(relation)
        print(query)

        return (relation, query)

    def get_intermediate_filename(self, step_number):
        """Returns a string for an intermediate filename with step number."""

        filename = self.output.split('.')[:-1]
        file_extension = self.output.split('.')[-1]
        filename.extend([f"_intermediate_{step_number}.", file_extension])
        return ''.join(filename)

    def write_intermediate_result(self, schema, table, step_number):
        """Writes an intermediate result of the chase algorithm to
        `self.output`.

        Parameters
        ----------
        schema : dict[str, int]
            A mapping of the attributes to the index it appears in the
            table.
        table : list[list[str]]
            A 2d array representing the chase table.
        step_number : int
            An integer representing the number of steps taken.
        """

        # Create the root element
        root = ET.Element('intermediate_result')

        # Create the table and header element and add attribute elements
        table_element = ET.SubElement(root, 'table')
        header = ET.SubElement(table_element, 'header')
        for attr, _ in sorted(schema.items(), key=lambda x: x[1]):
            ET.SubElement(header, 'attribute').text = attr

        # Create row elements and add value elements
        for row_data in table:
            row = ET.SubElement(table_element, 'row')
            for value in row_data:
                ET.SubElement(row, 'value').text = str(value)

        # Add the step number element
        _ = ET.SubElement(root, 'step_number').text = str(step_number)

        # Write the XML file
        tree = ET.ElementTree(root)
        filename = self.get_intermediate_filename(step_number)
        tree.write(filename)

    def write_min_cov(self, fds):
        """Writes the minimum cover of a relation to `self.output`.

        Parameters
        ----------
        fds : list[FunctionalDependency]
            A list of functional dependencies.
        """

        # Create the root element
        root = ET.Element('minimum_cover')

        # Create the functional dependency elements
        for fd in fds:
            fd_element = ET.SubElement(root, 'functional_dependency')
            lhs = ET.SubElement(fd_element, 'lhs')
            for attr in fd[0]:
                ET.SubElement(lhs, 'attribute').text = attr
            rhs = ET.SubElement(fd_element, 'rhs')
            for attr in fd[1]:
                ET.SubElement(rhs, 'attribute').text = attr

        # Write the XML file
        tree = ET.ElementTree(root)
        tree.write(self.output)

    def write_result(self, schema, table, answer):
        """Writes the result of the chase algorithm to `self.output`.

        Parameters
        ----------
        schema : dict[str, int]
            A mapping of the attributes to the index it appears in the
            table.
        table : list[list[str]]
            A 2d array representing the chase table.
        answer : bool
            The answer to the decision problem.
        """

        # Create the root element
        root = ET.Element('result')

        # Create the table and header element and add attribute elements
        table_element = ET.SubElement(root, 'table')
        header = ET.SubElement(table_element, 'header')
        for attr, _ in sorted(schema.items(), key=lambda x: x[1]):
            ET.SubElement(header, 'attribute').text = attr

        # Create row elements and add value elements
        for row_data in table:
            row = ET.SubElement(table_element, 'row')
            for value in row_data:
                ET.SubElement(row, 'value').text = str(value)

        # Add the answer element
        _ = ET.SubElement(root, 'answer').text = 'yes' if answer else 'no'

        # Write the XML file
        tree = ET.ElementTree(root)
        tree.write(self.output)
