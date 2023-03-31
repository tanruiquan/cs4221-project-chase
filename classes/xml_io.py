import xml.etree.ElementTree as ET
from classes.Relation import Relation
from classes.Query import Query, Task

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

    def read_xml(self):
        """Reads an xml file and returns 2 objects: `Relation` and `Query`
        which represents the relational table and task that we are chasing
        respectively."""

        tree = ET.parse(self.input)
        root = tree.getroot()
        relation = Relation()
        for child in root.find("table"):
            if child.tag == "attribute":
                relation.add_attribute(child.text)
            else:
                lhs = child.find("lhs")
                lhs = [attr.text for attr in lhs.findall("attribute")]
                rhs = child.find("rhs")
                rhs = [attr.text for attr in rhs.findall("attribute")]
                if child.tag == "functional_dependency":
                    relation.add_functional_dependency(lhs, rhs)
                elif child.tag == "multivalued_dependency":
                    relation.add_multivalued_dependency(lhs, rhs)

        query = Query()
        for child in root.find("dependency_check"):
            if child.tag == "functional_dependency":
                query.set_task(Task.FUNCTIONAL_DEPENDENCY)
                lhs = child.find("lhs")
                lhs = [attr.text for attr in lhs.findall("attribute")]
                rhs = child.find("rhs")
                rhs = [attr.text for attr in rhs.findall("attribute")]
                query.add_check([lhs, rhs])
            elif child.tag == "multivalued_dependency":
                query.set_task(Task.MULTIVALUED_DEPENDENCY)
                lhs = child.find("lhs")
                lhs = [attr.text for attr in lhs.findall("attribute")]
                rhs = child.find("rhs")
                rhs = [attr.text for attr in rhs.findall("attribute")]
                query.add_check([lhs, rhs])
            elif child.tag == "table":
                query.set_task(Task.LOSSLESS_JOIN)
                query.add_check(Relation(set(child.findall("attribute"))))
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
