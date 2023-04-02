from typing import Dict

from utils.common import ALPHA

# assume that ALL FDs are sorted in the order of schema


def chaseFds(table: list[list[str]], fds: list[list[list[str]]], schema: Dict[str, int]):
    for fd in fds:
        hasUpdated = False
        leftPos = list(map(lambda x: schema[x], fd[0]))
        rightPos = list(map(lambda x: schema[x], fd[1]))
        leftToRight, counts = getLeftToRight(
            leftPos, rightPos, table)
        for i, row in enumerate(table):
            left = combineList(list(map(lambda x: row[x], leftPos)))
            right = list(map(lambda x: row[x], rightPos))
            mostCommonRight = getMostCommonRight(leftToRight[left], counts)
            if mostCommonRight != right:
                hasUpdated = True
                table[i] = updateRow(row, rightPos, mostCommonRight)
        if hasUpdated:
            return table, True
    return table, False


def getMostCommonRight(rights: Dict[str, int], counts: Dict[str, int]):
    maxCount = 0
    maxRight = ''
    for count in counts:
        if counts[count] > maxCount and count in rights:
            maxCount = counts[count]
            maxRight = count
    return breakUpCombine(maxRight)


def getLeftToRight(leftPos: list[int], rightPos: list[int], table: list[list[str]]):
    result: Dict[str, Dict[str, int]] = {}
    counts: Dict[str, int] = {}
    for row in table:
        left = combineList(list(map(lambda x: row[x], leftPos)))
        right = list(map(lambda x: row[x], rightPos))
        combine_right = combineList(right)

        if isDistinguished(right):
            result[left] = {combine_right: 9999}
            counts[combine_right] = 9999
        else:
            if combine_right in counts:
                counts[combine_right] += 1
            else:
                counts[combine_right] = 1
            if left in result:
                if combine_right in result[left]:
                    result[left][combine_right] += 1
                else:
                    result[left][combine_right] = 1
            else:
                result[left] = {combine_right: 1}
    return result, counts


def combineList(lst: list[str]):
    return ','.join(lst)


def breakUpCombine(combine: str):
    return combine.split(',')


def isDistinguished(right: list[str]):
    for r in right:
        if r != ALPHA:
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
    # table = [[ALPHA, 'b1', 'c1', ALPHA, 'e1'],
    #          [ALPHA, ALPHA, 'c2', 'd2', 'e2'],
    #          ['a3', ALPHA, 'c3', 'd3', ALPHA],
    #          ['a4', 'b4', ALPHA, ALPHA, ALPHA],
    #          [ALPHA, 'b5', 'c5', 'd5', ALPHA]]
    # fds = [[['A'], ['C']],
    #        [['B'], ['C']],
    #        [['C'], ['D']],
    #        [['D', 'E'], ['C']],
    #        [['C', 'E'], ['A']]]
    # schema = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    table = [['a1', 'b1', 'c1', 'd1'], ['a1', 'b2', 'c2', 'd2'],
             ['a1', 'b2', 'c2', 'd1'], ['a1', 'b1', 'c1', 'd2']]
    fds = [[['D'], ['C']]]
    schema = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

    while canContinue:
        print(table)
        table, canContinue = chaseFds(table, fds, schema)


if __name__ == '__main__':
    main()
