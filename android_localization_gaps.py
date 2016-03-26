from xml.dom import minidom
import sys, getopt
import codecs

class Logger:
    logEnabled = False;

    def __init__(self):
        logEnabled = False

    def d(self, logStr):
        if self.logEnabled:
            print logStr

def showHelp():
    print 'test.py -b <basefile> -l <localizedfile>'
    print 'options'
    print '-d: enable debug mode'
    print '-h: show help'

def getItemListFromStringsXml(fileName):
    baseXmlDoc = minidom.parse(fileName)
    baseItemList = baseXmlDoc.getElementsByTagName('string')
    return baseItemList

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hdb:l:",["base=","localized="])
    except getopt.GetoptError:
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
