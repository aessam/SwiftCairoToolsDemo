from json import loads, dumps
import sys, subprocess, os
 

def mbsearch(seq, t):
    min = 1
    max = len(seq) - 1
    while True:
        if max < min:
            return 0
        m = (min + max) // 2
        if seq[m-1] <= t and t <= seq[m]:
            return m
        elif seq[m-1] < t:
            min = m + 1
        elif seq[m] > t:
            max = m - 1

def load_words():
    with open('./words_alpha.txt') as word_file:
        valid_words = set(word_file.read().lower().split())
    return valid_words

def prepareLineToOffset(filename):
    allLines = open(filename).read().split("\n")
    offsetToLine = [0]
    for line in allLines:
        offsetToLine.append(offsetToLine[-1] + len(line) + 1)
    return offsetToLine

def camelCasingToEnglish(variable):
    words = [""]
    for c in variable:
        if c.isupper() and len(words[-1]) > 1:
            words.append("")
        words[-1] += c
    return words

def getAllNames(sourceKittenStruct):
    returnArr = []
    if type(sourceKittenStruct) is list:
        for item in sourceKittenStruct:
            returnArr += getAllNames(item)

    if "key.kind" in sourceKittenStruct \
        and "key.name" in sourceKittenStruct \
        and sourceKittenStruct["key.kind"].startswith("source.lang.swift.decl"):
        returnArr.append( (camelCasingToEnglish(sourceKittenStruct["key.name"].split("(")[0]), sourceKittenStruct["key.offset"]) )
    if "key.substructure" in sourceKittenStruct:
        returnArr += getAllNames(sourceKittenStruct["key.substructure"])
    return returnArr

allSwiftFiles = subprocess.Popen("find \"" + sys.argv[1] + "\" -iname '*.swift'" , shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").split("\n")

for file in allSwiftFiles:
    if not os.path.exists(file):
        continue
    struct = loads(subprocess.Popen("sourcekitten structure --file \"" + file + "\"", shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8"))
    offsetToLine = prepareLineToOffset(file)
    allVars = getAllNames(struct)
    words = load_words()
    for var in allVars:
        lineNumber = mbsearch(offsetToLine, var[1])
        for word in var[0]:
            if word.lower() not in words:
                print(file + ":" + str(lineNumber) + ": warning: " + word + " not found in our english dict")
