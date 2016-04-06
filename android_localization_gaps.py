from xml.dom import minidom
import sys, getopt
import codecs

from ASProjectTree import ASProject
from Log import Logger

# Todo
# 1. Give Android Studio source route and then automatically find gaps for all
#       localization w.r.t base strings xml. Handle cases like filename other than
#       strings.xml
# 2. Add support for string arrays

def showHelp():
    print "\nUsage: "
    print 'python android_localization_gaps.py -b <basefile> -l <localizedfile>'
    print 'options:'
    print '--root: Android Studio project root '
    print '-d: enable debug mode'
    print '-h: show help'
    print '-s: sort all string resource files by its name'

def getItemListFromStringsXml(fileName):
    baseXmlDoc = minidom.parse(fileName)
    baseItemList = baseXmlDoc.getElementsByTagName('string')
    baseItemList.append(baseXmlDoc.getElementsByTagName('string-array'))
    return baseItemList

def sort(stringFilePath):
    nodes = getItemListFromStringsXml(stringFilePath);
    nodes.sort(key=lambda x: str(x.attributes['name'].value))
    return nodes

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hdsb:l:",["base=","localized=", "root="])
    except getopt.GetoptError:
        showHelp()
        sys.exit()

    if '--root' not in opts:
        print "\'--root\' is compulsory argument."
        showHelp()
        sys.exit()

    log = Logger()
    baseFile=None
    localizedFile=None

    for opt, arg in opts:
        if opt == '-h':
            showHelp()
            sys.exit()
        elif opt == '-d':
            log.logEnabled = True
        elif opt in ("-b", "--base"):
            log.d("basefile: " + arg)
            baseFile = arg
        elif opt in ("-l", "--localized"):
            log.d("localizedFile: " + arg)
            localizedFile = arg
        elif opt == '--root':
            project = ASProject(arg)
            project.getStringFiles()
            sys.exit()

    # base strings file
    log.d("Reading base strings.. ")
    baseItemList = getItemListFromStringsXml(baseFile)
    log.d( "No of base strings : " + str(len(baseItemList)))

    # localized strings file
    log.d("Reading localized strings.. ")
    localizedItemList = getItemListFromStringsXml(localizedFile)
    log.d( "No of localized strings : " + str(len(localizedItemList)))

    noOfUntranslatedStrings = 0;
    outputFile = codecs.open('gaps.txt', encoding='utf-8', mode='w')
    for s in baseItemList:
        baseName = s.attributes['name'].value
        found = False

        for localizedString in localizedItemList:
            if baseName == localizedString.attributes['name'].value:
                found = True
                continue

        if found is False:
            if s.firstChild.nodeValue is not None:
                outputFile.write(s.firstChild.nodeValue + '\n')
                noOfUntranslatedStrings = noOfUntranslatedStrings + 1
            else:
                log.d("None Node Value for:  " + s.attributes['name'].value)

    outputFile.close()
    log.d('\nNo of Untranslated Strings: ' + str(noOfUntranslatedStrings) + '\n')
