def main():
    table = setUpInitTable(input)
    while not satisfyRequirement():
        data, changed = step(
            tableData, functionalDependencies, multiValuedDependencies)
        if not changed:
            return False
    return True


# unique to each chase type
def setUpInitTable(input):
    # convert the initTable to the tableData format
    print("Hello World")


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
