def chaseMvds(table: list[list[str]], mvds: list[list[list[str]]]):
    attr_col = {}
    isUpdated = False

    for i in range(len(table[0])): # mapping of attr to index
        attr_col[table[0][i]] = i
    mapToIndex(mvds, attr_col)

    for mvd in mvds:
        lhs_col = mvd[0] 
        rhs_col = mvd[1]
        lhs_to_rhs = {}
        generated = [] # list of rows generated

        for row in table[1:]:
            lhs = tuple(row[i] for i in lhs_col)
            rhs = tuple(row[i] for i in rhs_col)
            if lhs not in lhs_to_rhs:
                lhs_to_rhs[lhs] = set()
                lhs_to_rhs[lhs].add(rhs)
            else : 
                lhs_to_rhs[lhs].add(rhs)

        for row in table[1:]:
            curr_rhs = tuple(row[i] for i in rhs_col)
            all_rhs = lhs_to_rhs[tuple(row[i] for i in lhs_col)]
            for rhs in all_rhs:
                if rhs != curr_rhs:
                    new_row = row.copy()
                    idx = 0
                    for attr in rhs: 
                        new_row[rhs_col[idx]] = attr
                        idx += 1

                    if (new_row not in generated) and (new_row not in table) :
                        generated.append(new_row)
        
        if generated: 
            isUpdated = isUpdated or True
            table += generated
            print(table) # print intermediate tables

    return (table, isUpdated)

def mapToIndex(mvds: list[list[list[str]]], attr_col: dict):
    for mvd in mvds: 
        lhs_col = list(map(lambda x: attr_col[x], mvd[0]))
        rhs_col = list(map(lambda x: attr_col[x], mvd[1]))
        mvd[0] = lhs_col
        mvd[1] = rhs_col

def main():
    table = [['A', 'B', 'C', 'D'],
            ['a1', 'b1', 'c1', 'd1'], 
            ['a1', 'b2', 'c2', 'd2']]
    
    mvds = [[['A'], ['B']], [['B'], ['C']]]
    res = chaseMvds(table, mvds)
    print(res[0])

if __name__ == '__main__':
    main()