from argparse import ArgumentParser
import xml.etree.ElementTree as ET

from classes.Relation import Relation
from classes.Query import Query, Task
from chaseFd import chaseFds
from chaseMvd import chaseMvds
from utils.fileutils import write_intermediate_result, write_result

from utils.common import ALPHA

from pprint import pprint


def main(relation, query, outputFilename):
    # schema is a dict of attributes to index, in the order it appears in the table
    schema, table = setUpInitTable(relation, query)
    stepNum = 1
    while not satisfyRequirement(table, query, schema):
        table, changed = step(table, relation, schema, stepNum, outputFilename)
        if not changed:
            handleFinalOutput(outputFilename, schema, table, False)
            return False
        stepNum += 1
    handleFinalOutput(outputFilename, schema, table, True)
    return True


# unique to each chase type
def setUpInitTable(relation, query):
    # convert the initTable to the tableData format
    schema = {}
    for idx, val in enumerate(sorted(relation.attributes)):
        schema[val] = idx
    schemaList = sorted(schema.items(), key=lambda x: x[1])
    table = []

    task = query.task
    if task == Task.FUNCTIONAL_DEPENDENCY:
        table = [[],[]]
        lhs = query.to_check[0][0]
        table[0] = [ALPHA for attr in schema]
        table[1] = [ALPHA if attr in lhs else attr + str(2) for attr,idx in schemaList]

    elif task == Task.MULTIVALUED_DEPENDENCY:
        table = [[],[]]
        lhs = query.to_check[0][0]
        rhs = query.to_check[0][1]
        table[0] = [ALPHA if (attr in lhs or attr in rhs) else attr + str(1) for attr,idx in schemaList]
        table[1] = [ALPHA if (attr in lhs or attr in set(schema.keys()).difference(set(rhs))) \
                        else attr + str(2) for attr,idx in schemaList]

    elif task == Task.LOSSLESS_JOIN:
        n = len(query.to_check)  # number of subtables
        table = [[] for i in range(0, n)]
        for i in range(0, n):
            subschema = query.to_check[i].attributes
            table[i] = [ALPHA if (attr in subschema) else attr + str(i+1) for attr,idx in schemaList]

    return (schema, table)


def step(table, relation, schema, stepNumber, outputFilename):
    # loop thru all functional dependencies and multi-valued dependencies
    # if hasUpdate, return (updatedTableData, True)
    # else return (updatedTableDate, False)
    table, hasFdUpdate = chaseFds(table, relation.functional_dependencies, schema)

    table, hasMvdUpdate = chaseMvds(table, relation.multivalued_dependencies, schema);

    hasUpdate = hasFdUpdate or hasMvdUpdate

    if hasUpdate:
        handleIntermediateOutput(outputFilename, schema, table, stepNumber) 
    return (table, hasUpdate)


def handleIntermediateOutput(outputFilename, schema, table, stepNumber):
    pprint(table)
    print()

    fileExtension = ".xml"
    intermediateOutputFilename = ''.join(outputFilename.split(fileExtension)) + f"_intermediate_{stepNumber}" + fileExtension
    write_intermediate_result(intermediateOutputFilename, schema, table)


def handleFinalOutput(outputFilename, schema, table, answer):
    pprint(table)
    print()
    write_result(outputFilename, schema, table, answer)


# unique to each chase type
def satisfyRequirement(table, query, schema):
    # if alr valid, return True
    task = query.task
    if task == Task.FUNCTIONAL_DEPENDENCY: 
        rhs = query.to_check[0][1]
        for attr in rhs:
            for row in table:
                if row[schema[attr]] != ALPHA:
                    return False
        return True

    elif task == Task.MULTIVALUED_DEPENDENCY:
        for row in table:
            if all(attr == ALPHA for attr in row):
                return True
        return False

    elif task == Task.LOSSLESS_JOIN:
        for row in table:
            if all(attr == ALPHA for attr in row):
                return True
        return False
    
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
    main(relation, query, args.output)
