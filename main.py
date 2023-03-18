from argparse import ArgumentParser
import xml.etree.ElementTree as ET
from classes.relation import Relation
from classes.query import Query, Task

ALPHA = -1  # distinguished variable symbol


def main(relation, query):
    # attrOrder is a list of attributes in the order as it appears in the table
    attrOrder, table = setUpInitTable(relation, query)
    while not satisfyRequirement():
        data, changed = step(
            tableData, functionalDependencies, multiValuedDependencies)
        if not changed:
            return False
    return True


# unique to each chase type
def setUpInitTable(relation, query):
    # convert the initTable to the tableData format
    attrOrder = list(relation.attributes)
    table = []

    task = query.task
    if task == Task.FUNCTIONAL_DEPENDENCY:
        table = [[],[]]
        lhs = query.to_check[0][0]
        table[0] = [ALPHA for attr in attrOrder]
        table[1] = [ALPHA if attr in lhs else attr + str(1) for attr in attrOrder]

    elif task == Task.MULTIVALUED_DEPENDENCY:
        table = [[],[]]
        lhs = query.to_check[0][0]
        rhs = query.to_check[0][1]
        table[0] = [ALPHA if (attr in lhs or attr in rhs) else attr + str(0) for attr in attrOrder]
        table[1] = [ALPHA if (attr in lhs or attr in set(attrOrder).difference(set(rhs))) else attr + str(1) for attr in attrOrder]

    elif task == Task.LOSSLESS_JOIN:
        n = len(query.to_check)  # number of subtables
        table = [[] for i in range(0, n)]
        for i in range(0, n):
            schema = query.to_check[i].attributes
            table[i] = [ALPHA if (attr in schema) else attr + str(i) for attr in attrOrder]

    return (attrOrder, table)


def handleOutput():
    # convert the tableData to the output xml format
    print("Hello World")


def step(tableData, functionalDependencies, multiValuedDependencies):
    # loop thru all functional dependencies and multi-valued dependencies
    # if haveUpdate, return (updatedtableData, True)
    # else
    handleOutput()
    return (tableData, False)


# unique to each chase type
def satisfyRequirement():
    # if alr valid, return True
    return False


def parse_input(input_file):
    """Takes in a xml file and returns 2 objects: `Relation` and `Query`
    which represents the relational table and task that we are chasing
    respectively."""

    tree = ET.parse(input_file)
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


if __name__ == '__main__':
    parser = ArgumentParser(
        description="Apply the chase algorithm to a xml format of a problem statement"
    )
    parser.add_argument("input")
    parser.add_argument("output", nargs="?", default="output.xml")
    args = parser.parse_args()

    relation, query = parse_input(args.input)
    print(relation)
    print(query)
    main(relation, query)
