from json import loads, dumps
import sys, subprocess, os
#https://developer.apple.com/swift/blog/?id=27

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

def prepareLineToOffset(filename):
    allLines = open(filename).read().split("\n")
    offsetToLine = [0]
    for line in allLines:
        offsetToLine.append(offsetToLine[-1] + len(line) + 1)
    return offsetToLine

classToOffset = {}
def getAllDefinedClasses(sourceKittenStruct, offsets):
    definedClasses = []
    for aThing in sourceKittenStruct['key.substructure']:
        if aThing['key.kind'] == 'source.lang.swift.decl.class':
            definedClasses.append(aThing['key.name'])
            classToOffset[aThing['key.name']] = mbsearch(offsets, aThing['key.nameoffset'])
    return definedClasses

def getAllParents(sourceKittenStruct):
    definedClasses = []
    for aThing in sourceKittenStruct['key.substructure']:
        if 'key.inheritedtypes' in aThing:
            for parent in aThing['key.inheritedtypes']:
                definedClasses.append(parent['key.name'])
    return definedClasses

allSwiftFiles = subprocess.Popen("find \"" + sys.argv[1] + "\" -iname '*.swift'" , shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").split("\n")

classesFileMap = {}
allParents = []
for file in allSwiftFiles:
    if not os.path.exists(file):
        continue
    struct = loads(subprocess.Popen("sourcekitten structure --file \"" + file + "\"", shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8"))
    offsetToLine = prepareLineToOffset(file)
    allParents.extend(getAllParents(struct))
    classesFileMap.update(dict(map(lambda x: (x, file), getAllDefinedClasses(struct, offsetToLine))))

classesThatShouldBeFinal = set(classesFileMap.keys()) - set(allParents)
for finalableClass in classesThatShouldBeFinal:
    print(classesFileMap[finalableClass] + ":" + str(classToOffset[finalableClass]) + ": warning: الكيلاس " + finalableClass + " عقيمة، يعني لازم تبقى فينل.")
