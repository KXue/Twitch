rulesList = ['', "F->n", "F->v", "E->T", "E->EaT", "E->EsT", "T->F", "T->TmF", "T->TdF", "F->oEc", "S->bEe"]
reduceList = [0, 1, 1, 1, 3, 3, 1, 3, 3, 3, 3]
alphaList = ['n', 'v', 'o', 'c', 'a', 's', 'm', 'd', 'b', 'e', 'S', 'E', 'F', 'T', 'L']
parseTable = [[-1 for x in range(15)] for x in range(14)]
parseTable[0][8] = 2
parseTable[1] = [7, 7, 10, -1, -1, -1, -1, -1, -1, -1, -1, 3, 9, 8, -1]
parseTable[2][4] = 5
parseTable[2][5] = 5
parseTable[2][9] = 4
parseTable[3] = ['acc' for x in range(15)]
parseTable[4] = parseTable[1][:]
parseTable[4][11] = -1
parseTable[4][13] = 6
parseTable[5][6] = 11
parseTable[5][7] = 11
parseTable[5][14] = 'r4/5;a,s,c,e'
parseTable[6] = ['r1/2' for x in range(15)]
parseTable[7] = parseTable[5][:]
parseTable[7][14] = 'r3;a,s,c,e';
parseTable[8] = ['r6' for x in range(15)]
parseTable[9] = parseTable[1][:]
parseTable[9][11] = 13
parseTable[10] = parseTable[9][:]
parseTable[10][11] = -1
parseTable[10][12] = 12
parseTable[10][13] = -1
parseTable[11] = ['r7/8' for x in range(15)]
parseTable[12][4] = 5
parseTable[12][5] = 5
parseTable[12][3] = 14
parseTable[13] = ['r9' for x in range(15)]
stateRuleDictionary = {}
stateRuleDictionary[3] = 10
stateRuleDictionary[5] = 4
stateRuleDictionary[6] = 1
stateRuleDictionary[7] = 3
stateRuleDictionary[8] = 6
stateRuleDictionary[11] = 7
stateRuleDictionary[13] = 9
class Tokens:
    Number, Variable, OBracket, CBracket, Add, Sub, Mult, Div, BOF, EOF, Start, Expression, Factor, Term = range(14)
class Node:
    def __init__(self):
        self.token = ()
        self.children = []

def expressionScanner(expression):
    if expression[-1] == '\n':
        expression = expression[:-1]
    expressionList = expression.split(' ')
    tokenList = []
    for element in expressionList:
        token = Tokens.Number
        if element == '(':
            token = Tokens.OBracket
        elif element == ')':
            token = Tokens.CBracket
        elif element == '+':
            token = Tokens.Add
        elif element == '-':
            token = Tokens.Sub
        elif element == '*':
            token = Tokens.Mult
        elif element == '/':
            token = Tokens.Div
        elif element.isalpha():
            token = Tokens.Variable
        tokenList.append((token, element))
    tokenList.append((Tokens.EOF, ''))
    tokenList = [(Tokens.BOF, '')] + tokenList
    return tokenList

def parse(tokenList):
    stateList = [0]
    nodeList = []
    while tokenList:
        token = tokenList[0]
        #peek
        if not isinstance(parseTable[stateList[-1]][14], int) and peek(parseTable[stateList[-1]][14], token):
            #if reduce possible reduce
            reduce(stateList, nodeList)
        else:
            #else shift token
            shift(stateList, nodeList, token)
            #remove token
            del tokenList[0]
    if stateList[-1] != 3:
        return 0
    return nodeList

def peek(action, token):
    print(alphaList[token[0]])
    print(action)
    return alphaList[token[0]] in action and ';' in action or ';' not in action

def shift(stateList, nodeList, token):
    print("shift " + `token` + " at state " + `stateList[-1]`)
    nextState = parseTable[stateList[-1]][token[0]] - 1
    stateList.append(nextState)
    node = Node()
    node.token = token
    nodeList.append(node)

def reduce(stateList, nodeList):
    reduceRule = stateRuleDictionary[stateList[-1]]
    print(rulesList[reduceRule])
    parent = Node()
    nonTerminal = rulesList[reduceRule][0]
    nonTerminalIndex = alphaList.index(nonTerminal)
    parent.token = (nonTerminalIndex, nonTerminal)
    for x in range(reduceList[reduceRule]):
        parent.children.insert(0, nodeList[-1])
        del nodeList[-1]
        del stateList[-1]
    nodeList.append(parent)
    nextState = parseTable[stateList[-1]][parent.token[0]] - 1
    stateList.append(nextState)

def printNode(nodeList):
    nodeStack = list(nodeList)
    print("____________Nodes:_____________")
    while nodeStack:
        nextStack = []
        lineString = ''
        while nodeStack:
            lineString += (`nodeStack[0].token` + ", ")
            nextStack.extend(nodeStack[0].children)
            del nodeStack[0]
        print lineString
        nodeStack = nextStack

def endOutput(nodeList):
    outputString = ''
    for node in nodeList:
        if node.token[0] < Tokens.BOF:
            outputString += node.token[1] + ' '
        outputString += endOutput(node.children)
    return outputString

def polish(nodeList):
    for node in nodeList:
        if len(node.children) > 2 and node.children[1].token[0] in (Tokens.Add, Tokens.Sub, Tokens.Mult, Tokens.Div):
            node.children[0], node.children[1] = node.children[1], node.children[0]
            openBracketNode = Node()
            openBracketNode.token = (Tokens.OBracket, '(')
            closeBracketNode = Node()
            closeBracketNode.token = (Tokens.CBracket, ')')
            node.children.insert(0, openBracketNode)
            node.children.append(closeBracketNode)
        elif len(node.children) == 3 and node.children[0].token[0] == Tokens.OBracket and node.children[2].token[0] == Tokens.CBracket:
            del node.children[2]
            del node.children[0]
        polish(node.children)

def evaluate(rootNode):
    action = None
    first = None
    second = None
    output = ''
    for node in rootNode.children:
        if node.token[0] in (Tokens.Add, Tokens.Sub, Tokens.Mult, Tokens.Div):
            action = node.token[0]
        elif action and not first:
            first = evaluate(node)
        elif action and first and not second:
            second = evaluate(node)
    if action and first and second:
        output += operate(action, first, second)
    elif rootNode.token[0] <= Tokens.Variable:
        output = rootNode.token[1]
    else:
        for node in rootNode.children:
            output += evaluate(node)
    if not isInt(output) and action:
        output = '(' + output + ')'
    return output

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def operate(action, first, second):
    result = -1
    if isInt(first) and isInt(second):
        first = int(first)
        second = int(second)
        if action == Tokens.Add:
            result = first + second
        elif action == Tokens.Sub:
            result = first - second
        elif action == Tokens.Mult:
            result = first * second
        elif action == Tokens.Div:
            result = first / second
    else:
        result = ('+','-','*','/')[action-4] + ' ' + first + ' ' + second
    if isInt(result):
        result = `result`
    return result

def prefix(expression):
    tokenList = expressionScanner(expression)
    nodeList = parse(tokenList)
    if nodeList:
        print("success")
        printNode(nodeList)
        polish(nodeList)
        result = endOutput(nodeList)
        print(result)
        print(evaluate(nodeList[1]))
        return result
    else:
        print("failure")
    return -1

if __name__ == "__main__":
    '''print(operate(Tokens.Add, 1, 2))
    print(operate(Tokens.Sub, 4, 'x'))
    print(operate(Tokens.Mult, 'y', 'x'))
    '''
    for x in parseTable:
        row = ''
        for y in x:
            row += (`y` + ", ")
        print(row)
    file = open("expressions.txt", 'r')
    for line in file:
        prefix(line)
