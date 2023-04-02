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
    distinguished = False
    if distinguished:  # distinguished chase
        if query.task != MINIMAL_COVER:
            checkEntailment(relation, query, xml_io)
        else:
            checkMinimalCover(relation, query, xml_io)
    else:  # simple chase
        if query.task != MINIMAL_COVER:
            simpleEntailment(relation, query, xml_io)
        else:
            simpleMinimalCover(relation, query, xml_io)


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
        lhs = query.functional_dependencies[0][0]
        table[0] = [ALPHA for attr in schema]
        table[1] = [ALPHA if attr in lhs else attr +
                    str(2) for attr, idx in schemaList]

    elif task == MULTIVALUED_DEPENDENCY:
        table = [[], []]
        lhs = query.multivalued_dependencies[0][0]
        rhs = query.multivalued_dependencies[0][1]
        table[0] = [ALPHA if (attr in lhs or attr in rhs)
                    else attr + str(1) for attr, idx in schemaList]
        table[1] = [ALPHA if (attr in lhs or attr in set(schema.keys()).difference(set(rhs)))
                    else attr + str(2) for attr, idx in schemaList]

    elif task == LOSSLESS_JOIN:
        n = len(query.relations)  # number of subtables
        table = [[] for i in range(0, n)]
        for i in range(0, n):
            subschema = query.relations[i].attributes
            table[i] = [ALPHA if (attr in subschema) else attr + str(i+1)
                        for attr, idx in schemaList]

    return (schema, table)


def setUpSimpleTable(relation, query):
    schema = {}
    for idx, val in enumerate(sorted(relation.attributes)):
        schema[val] = idx
    schemaList = sorted(schema.items(), key=lambda x: x[1])
    table = [1, 2]
    table = list(map(lambda x: [attr[0] + str(x)
                 for attr in schemaList], table))
    task = query.task
    if task == FUNCTIONAL_DEPENDENCY:
        lhs = query.functional_dependencies[0][0]
        lhs_index = list(map(lambda x: schema[x], lhs))
        for index in lhs_index:
            table[1][index] = table[0][index]

    elif task == MULTIVALUED_DEPENDENCY:
        lhs = query.multivalued_dependencies[0][0]
        lhs_index = list(map(lambda x: schema[x], lhs))
        for index in lhs_index:
            table[1][index] = table[0][index]

    elif task == LOSSLESS_JOIN:
        # only 2 relation for simple chase
        if len(query.relations) != 2:
            print("Error: only 2 relations for simple chase")
            return
        subschema1 = query.relations[0].attributes
        subschema2 = query.relations[1].attributes
        uniqueTo1 = set(subschema1).difference(set(subschema2))
        uniqueTo2 = set(subschema2).difference(set(subschema1))
        if len(uniqueTo1) == 0:
            print("Error: first relation is a proper subset of second relation")
        if len(uniqueTo2) == 0:
            print("Error: second relation is a proper subset of first relation")
        mvdLhs = list(uniqueTo1)
        mvdRhs = list(uniqueTo2)
        lhs_index = list(map(lambda x: schema[x], mvdLhs))
        for index in lhs_index:
            table[1][index] = table[0][index]
        query.task = MULTIVALUED_DEPENDENCY
        query.multivalued_dependencies = [[mvdLhs, mvdRhs]]

    return (schema, table)


def step(table, relation, schema):
    # loop thru all functional dependencies and multi-valued dependencies
    # if hasUpdate, return (updatedTableData, True)
    # else return (updatedTableDate, False)
    table, hasFdUpdate = chaseFds(
        table, relation.functional_dependencies, schema)

    if hasFdUpdate:
        return (table, hasFdUpdate)

    table, hasMvdUpdate = chaseMvds(
        table, relation.multivalued_dependencies, schema)

    return (table, hasMvdUpdate)


# unique to each chase type
def satisfyRequirement(table, query, schema):
    # if alr valid, return True
    task = query.task
    if task == FUNCTIONAL_DEPENDENCY:
        rhs = query.functional_dependencies[0][1]
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


def satisfySimpleRequirement(table, query, schema):
    # if alr valid, return True
    task = query.task
    if task == FUNCTIONAL_DEPENDENCY:
        lhs = query.functional_dependencies[0][0]
        lshPos = list(map(lambda x: schema[x], lhs))
        rhs = query.functional_dependencies[0][1]
        rhsPos = list(map(lambda x: schema[x], rhs))
        for i in range(0, len(table)):
            currLhs = list(map(lambda x: table[i][x], lshPos))
            currRhs = list(map(lambda x: table[i][x], rhsPos))
            for j in range(i+1, len(table)):
                checkLhs = list(map(lambda x: table[j][x], lshPos))
                checkRhs = list(map(lambda x: table[j][x], rhsPos))
                if checkLhs == currLhs and checkRhs != currRhs:
                    return False
        return True

    elif task == MULTIVALUED_DEPENDENCY:
        return satisfyMvd(table, query.multivalued_dependencies[0], schema)

    elif task == LOSSLESS_JOIN:
        print('Error: This should not happen!')
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


def simpleEntailment(relation: Relation, query: Query, xml_io: XMLIO | None):
    schema, table = setUpSimpleTable(relation, query)
    stepNum = 1
    while True:
        if xml_io is not None:
            print(f"Current: {stepNum}")
            xml_io.write_intermediate_result(schema, table, stepNum)
        table, changed = step(table, relation, schema)
        if not changed:
            break
        stepNum += 1
    answer = satisfySimpleRequirement(table, query, schema)
    if xml_io is not None:
        xml_io.write_result(schema, table, answer)
    return answer


def checkMinimalCover(relation: Relation, query: Query, xml_io: XMLIO | None):
    fds = query.functional_dependencies
    pos = 0
    step_num = 1
    if len(fds) == 0:
        return
    xml_io.write_min_cov(fds, 0)
    while pos < len(fds):
        newQuery = Query(FUNCTIONAL_DEPENDENCY)
        newQuery.add_functional_dependency(fds[pos][0], fds[pos][1])
        newRelation = Relation(relation.name, relation.attributes)
        for i, fd in enumerate(fds):
            if i != pos:
                newRelation.add_functional_dependency(fd[0], fd[1])
        if checkEntailment(newRelation, newQuery, None):
            fds.pop(pos)
            xml_io.write_min_cov(fds, step_num)
            step_num += 1
        else:
            pos += 1


def simpleMinimalCover(relation: Relation, query: Query, xml_io: XMLIO | None):
    fds = query.functional_dependencies
    pos = 0
    step_num = 1
    if len(fds) == 0:
        return
    xml_io.write_min_cov(fds, 0)
    while pos < len(fds):
        newQuery = Query(FUNCTIONAL_DEPENDENCY)
        newQuery.add_functional_dependency(fds[pos][0], fds[pos][1])
        newRelation = Relation(relation.name, relation.attributes)
        for i, fd in enumerate(fds):
            if i != pos:
                newRelation.add_functional_dependency(fd[0], fd[1])
        if checkEntailment(newRelation, newQuery, None):
            fds.pop(pos)
            xml_io.write_min_cov(fds, step_num)
            step_num += 1
        else:
            pos += 1


def satisfyMvd(table, mvd, schema):
    lhs = mvd[0]
    lshPos = list(map(lambda x: schema[x], lhs))
    rhs = mvd[1]
    rhsPos = list(map(lambda x: schema[x], rhs))
    for i in range(0, len(table)):
        currLhs = list(map(lambda x: table[i][x], lshPos))
        currRhs = list(map(lambda x: table[i][x], rhsPos))
        for j in range(0, len(table)):
            checkLhs = list(map(lambda x: table[j][x], lshPos))
            checkRhs = list(map(lambda x: table[j][x], rhsPos))
            if checkLhs == currLhs and checkRhs != currRhs:
                currRowCopy = table[i].copy()
                for k in range(0, len(currRowCopy)):
                    if k not in lshPos and k not in rhsPos:
                        currRowCopy[k] = table[j][k]
                if currRowCopy not in table:
                    return False
    return True


if __name__ == '__main__':
    main()
