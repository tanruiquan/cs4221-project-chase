from argparse import ArgumentParser
from classes.Relation import Relation

from classes.xml_io import XMLIO
from classes.Query import Query, Task
from chaseFd import chaseFds
from chaseMvd import chaseMvds
from utils.common import ALPHA, FUNCTIONAL_DEPENDENCY, LOSSLESS_JOIN, MINIMAL_COVER, MULTIVALUED_DEPENDENCY


def main():
    args = parse_arguments()
    xml_io = XMLIO(args.input, args.output)
    relation, query = xml_io.read_xml()
    # schema is a dict of attributes to index, in the order it appears in the table
    if query.task != MINIMAL_COVER:
        checkEntailment(relation, query, xml_io)
    else:
        checkMinimalCover(relation, query, xml_io)


def parse_arguments():
    """Set up the command line arguments and parse it."""

    parser = ArgumentParser(
        description="Apply the chase algorithm to a xml format of a problem statement"
    )
    parser.add_argument("input")
    parser.add_argument("output", nargs="?", default="output.xml")

    return parser.parse_args()

# unique to each chase type


def setUpInitTable(relation, query):
    # convert the initTable to the tableData format
    schema = {}
    for idx, val in enumerate(sorted(relation.attributes)):
        schema[val] = idx
    schemaList = sorted(schema.items(), key=lambda x: x[1])
    table = []

    task = query.task
    if task == FUNCTIONAL_DEPENDENCY:
        table = [[], []]
        lhs = query.to_check[0][0]
        table[0] = [ALPHA for attr in schema]
        table[1] = [ALPHA if attr in lhs else attr +
                    str(2) for attr, idx in schemaList]

    elif task == MULTIVALUED_DEPENDENCY:
        table = [[], []]
        lhs = query.to_check[0][0]
        rhs = query.to_check[0][1]
        table[0] = [ALPHA if (attr in lhs or attr in rhs)
                    else attr + str(1) for attr, idx in schemaList]
        table[1] = [ALPHA if (attr in lhs or attr in set(schema.keys()).difference(set(rhs)))
                    else attr + str(2) for attr, idx in schemaList]

    elif task == LOSSLESS_JOIN:
        n = len(query.to_check)  # number of subtables
        table = [[] for i in range(0, n)]
        for i in range(0, n):
            subschema = query.to_check[i].attributes
            table[i] = [ALPHA if (attr in subschema) else attr + str(i+1)
                        for attr, idx in schemaList]

    return (schema, table)


def step(table, relation, schema):
    # loop thru all functional dependencies and multi-valued dependencies
    # if hasUpdate, return (updatedTableData, True)
    # else return (updatedTableDate, False)
    table, hasFdUpdate = chaseFds(
        table, relation.functional_dependencies, schema)

    table, hasMvdUpdate = chaseMvds(
        table, relation.multivalued_dependencies, schema)

    hasUpdate = hasFdUpdate or hasMvdUpdate

    return (table, hasUpdate)


# unique to each chase type
def satisfyRequirement(table, query, schema):
    # if alr valid, return True
    task = query.task
    if task == FUNCTIONAL_DEPENDENCY:
        rhs = query.to_check[0][1]
        for attr in rhs:
            for row in table:
                if row[schema[attr]] != ALPHA:
                    return False
        return True

    elif task == MULTIVALUED_DEPENDENCY:
        for row in table:
            if all(attr == ALPHA for attr in row):
                return True
        return False

    elif task == LOSSLESS_JOIN:
        for row in table:
            if all(attr == ALPHA for attr in row):
                return True
        return False

    return False


def checkEntailment(relation: Relation, query: Query, xml_io: XMLIO | None):
    schema, table = setUpInitTable(relation, query)
    stepNum = 1
    answer = True
    while not satisfyRequirement(table, query, schema):
        if xml_io is not None:
            print(f"Current: {stepNum}")
            xml_io.write_intermediate_result(schema, table, stepNum)
        table, changed = step(table, relation, schema)
        if not changed:
            answer = False
            break
        stepNum += 1
    if xml_io is not None:
        xml_io.write_result(schema, table, answer)
    return answer


def checkMinimalCover(relation: Relation, query: Query, xml_io: XMLIO | None):
    fds = query.functional_dependencies
    pos = 0
    if len(fds) == 0:
        return
    while pos < len(fds):
        # TODO: xml_io.print_fd(fds)
        newQuery = Query(FUNCTIONAL_DEPENDENCY)
        newQuery.add_functional_dependency(fds[pos])
        if not checkEntailment(relation, newQuery):
            fds.pop(pos)
        else:
            pos += 1


if __name__ == '__main__':
    main()
