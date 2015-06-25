from collections import deque
from random import randint
class Node:
    def __init__(self, content):
        self.consonantChildrenDictionary = {}
        self.contents = content
        self.terminating = False
        self.vowelChildrenDictionary = {}

def isVowel(char):
    #ignoring y
    vowels = ('a', 'e', 'i', 'o', 'u')
    return char.lower() in vowels

def traverse(root):
    if root.terminating:
        print root.contents
    for consonant in root.consonantChildrenDictionary:
        traverse(root.consonantChildrenDictionary[consonant])
    for vowel in root.vowelChildrenDictionary:
        traverse(root.vowelChildrenDictionary[vowel])

def addKey(root, string):
    if len(string) > 1:
        char = string[0]
        if isVowel(char):
            if char in root.vowelChildrenDictionary:
                addKey(root.vowelChildrenDictionary[char], string[1:])
            else:
                vowelChild = Node(root.contents + char)
                root.vowelChildrenDictionary[char] = vowelChild
                addKey(root.vowelChildrenDictionary[char], string[1:])
        else:
            if char in root.consonantChildrenDictionary:
                addKey(root.consonantChildrenDictionary[char], string[1:])
            else:
                consonantChild = Node(root.contents + char)
                root.consonantChildrenDictionary[char] = consonantChild
                addKey(root.consonantChildrenDictionary[char], string[1:])
    else:
        root.terminating = True

def findString(queue, tokenList):
    for token in tokenList:
        tempQueue = []
        for numberOfRepeats in range(token[3]):
            nextQueue = []
            while len(queue) > 0:
                node = queue.popleft()
                if token[1]: #isVowel
                    nextQueue.extend(node.vowelChildrenDictionary.values())
                else: #inConsonant
                    if token[2].lower() in node.consonantChildrenDictionary:
                        nextQueue.append(node.consonantChildrenDictionary[token[2].lower()])
                    if token[2].upper() in node.consonantChildrenDictionary:
                        nextQueue.append(node.consonantChildrenDictionary[token[2].upper()])
            queue.extend(nextQueue)
            tempQueue.extend(nextQueue)
        queue = deque(tempQueue)
    for node in queue:
        if node.terminating:
            return node.contents

'''
breaks a string up into tokens containing info on whether it's a vowel, upper case, the char content and number of times it consecutively repeats

mostly optional but helps me understand (or break down) my input a bit better by simplifying repeated characters
'''
def stringScanner(string):
    tokenList = []
    charPosition = 0
    while charPosition < len(string):
        char = string[charPosition]
        lower = False
        vowel = False
        if char.islower():
            lower = True
        if isVowel(char):
            vowel = True
        repeatPosition = charPosition
        #we don't care about case here. We also don't care about duplicates of unequal vowels and treat every vowel as the same character
        while repeatPosition < len(string) and (string[repeatPosition].lower() == char.lower() or (isVowel(string[repeatPosition]) and isVowel(char))):
            repeatPosition += 1
        numberOfRepeats = repeatPosition - charPosition
        charPosition = repeatPosition
        tokenList.append((lower, vowel, char, numberOfRepeats))
    return tokenList;

def generateTrollStringsFromInputFile(file):
    outputFile = "Kevin-10000-Trollglish.txt"
    trolledIO = open(outputFile, 'w')
    for line in file:
        trolled = ""
        for char in line:
            if char.isalpha():
                duplicate = randint(1, 9)
                for index in range(duplicate):
                    nextChar = char
                    if isVowel(nextChar):
                        nextChar = ('a', 'e', 'i', 'o', 'u')[randint(0,4)]
                    if randint(0,1) == 1: #upper case
                        nextChar = nextChar.upper()
                    else:
                        nextChar = nextChar.lower()
                    trolled += nextChar
        trolledIO.write(trolled + "\n")
    trolledIO.close()

if __name__ == "__main__":
    inputFile = "google-10000-english.txt"
    root = Node("")
    file = open(inputFile, 'r');
    for line in file:
        addKey(root, line)
    file.seek(0)
    generateTrollStringsFromInputFile(file)
    file.close()
    queue = deque([root])
    trolledFile = "Kevin-10000-Trollglish.txt"
    trollFile = open(trolledFile, 'r')
    resolvedString = ""
    couldNotResolveArray = []
    for line in trollFile:
        resolvedString = findString(deque([root]), stringScanner(line.strip('\n')))
        if resolvedString:
            print("Trolled: " + line + "Resolved:" + resolvedString)
        else:
            print("NONE FOUND FOR" + line)
            couldNotResolveArray.append(line)
            break;
    for line in couldNotResolveArray:
        print(line + " could not be resolved.")
