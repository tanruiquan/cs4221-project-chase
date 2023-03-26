from typing import Dict

# assume distinguished value here is 'a'
# assume that ALL FDs are sorted in the order of schema


def chaseFds(table: list[list[str]], fds: list[list[list[str]]], schema: Dict[str, int]):
    for fd in fds:
        hasUpdated = False
        leftPos = list(map(lambda x: schema[x], fd[0]))
        rightPos = list(map(lambda x: schema[x], fd[1]))
        leftToRight: Dict[str, list[str]] = getLeftToRight(
            leftPos, rightPos, table)
        for i, row in enumerate(table):
            left = combineList(list(map(lambda x: row[x], leftPos)))
            right = list(map(lambda x: row[x], rightPos))
            if leftToRight[left] != right:
                hasUpdated = True
                table[i] = updateRow(row, rightPos, leftToRight[left])
        if hasUpdated:
            return table, True
    return table, False


def getLeftToRight(leftPos: list[int], rightPos: list[int], table: list[list[str]]):
    result: Dict[str, list[str]] = {}
    for row in table:
        left = combineList(list(map(lambda x: row[x], leftPos)))
        right = list(map(lambda x: row[x], rightPos))
        if left in result:
            if isDistinguished(right):
                result[left] = right
        else:
            result[left] = right
    return result


def combineList(lst: list[str]):
    return ','.join(lst)


def isDistinguished(right: list[str]):
    for r in right:
        if r != 'a':
            return False
    return True


def updateRow(row: list[str], rightPos: list[int], rightValues: list[str]):
    for i, pos in enumerate(rightPos):
        row[pos] = rightValues[i]
    return row


def main():
    canContinue = True
    # table = [['a', 'a', 'a', 'a'], ['a', 'b', 'c', 'd'],
    #          ['a', 'a', 'a', 'd'], ['a', 'b', 'c', 'a']]
    # fds = [[['D'], ['C']]]
    # schema = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    table = [['a', 'b1', 'c1', 'a', 'e1'],
             ['a', 'a', 'c2', 'd2', 'e2'],
             ['a3', 'a', 'c3', 'd3', 'a'],
             ['a4', 'b4', 'a', 'a', 'a'],
             ['a', 'b5', 'c5', 'd5', 'a']]
    fds = [[['A'], ['C']],
           [['B'], ['C']],
           [['C'], ['D']],
           [['D', 'E'], ['C']],
           [['C', 'E'], ['A']]]
    schema = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    while canContinue:
        print(table)
        table, canContinue = chaseFds(table, fds, schema)


if __name__ == '__main__':
    main()
