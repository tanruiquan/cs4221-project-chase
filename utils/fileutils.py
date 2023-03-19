"""
A module that exposes various file utility functions to read from and wrtie to xml file.
"""
import xml.etree.ElementTree as ET

def write_intermediate_result(filename, schema, table):
    """Writes an intermediate result of the chase algorithm to
    `filename`.

    Parameters
    ----------
    filename : str
        The name of the output file.
    schema : dict[str, int]
        A mapping of the attributes to the index it appears in the
        table.
    table : list[list[str]]
        A 2d array representing the chase table.
    """

    # Create the root element
    root = ET.Element('table')

    # Create the header element and add attribute elements
    header = ET.SubElement(root, 'header')
    for attr, _ in sorted(schema.items(), key=lambda x: x[1]):
        ET.SubElement(header, 'attribute').text = attr

    # Create row elements and add value elements
    for row_data in table:
        row = ET.SubElement(root, 'row')
        for value in row_data:
            ET.SubElement(row, 'value').text = str(value)

    # Write the XML file
    tree = ET.ElementTree(root)
    tree.write(filename)

def write_result(filename, schema, table, answer):
    """Writes the result of the chase algorithm to `filename`.

    Parameters
    ----------
    filename : str
        The name of the output file.
    schema : dict[str, int]
        A mapping of the attributes to the index it appears in the
        table.
    table : list[list[str]]
        A 2d array representing the chase table.
    answer : bool
        The answer to the decision problem.
    """

    # Create the root element
    root = ET.Element('table')

    # Create the header element and add attribute elements
    header = ET.SubElement(root, 'header')
    for attr, _ in sorted(schema.items(), key=lambda x: x[1]):
        ET.SubElement(header, 'attribute').text = attr

    # Create row elements and add value elements
    for row_data in table:
        row = ET.SubElement(root, 'row')
        for value in row_data:
            ET.SubElement(row, 'value').text = str(value)

    # Add the answer element
    _ = ET.SubElement(root, 'answer').text = 'yes' if answer else 'no'

    # Write the XML file
    tree = ET.ElementTree(root)
    tree.write(filename)

def main():
    """Tests the function of the file ultils."""
    filename = "test_output.xml"
    schema = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    table = [['a', 'b1', 'c1', 'a', 'e1'],
             ['a', 'a', 'c2', 'd2', 'e2'],
             ['a3', 'a', 'c3', 'd3', 'a'],
             ['a4', 'b4', 'a', 'a', 'a'],
             ['a', 'b5', 'c5', 'd5', 'a']]
    write_intermediate_result(filename, schema, table)

if __name__ == '__main__':
    main()
