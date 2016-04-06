import glob
# Iterates through Android studio project structure and give helper functions
# to access various files and paths

#Todo
# 1. validate for valid project root
class ASProject:
    projectRoot = None

    def __init__(self, root):
        self.projectRoot = root

    # returns all string files in a project
    def getStringFiles(self):
        resRoot = self.projectRoot + "/app/src/main/res"
        valuesDirs = glob.glob(resRoot + "/values*")
        stringResourceFiles = []
        for valuesDir in valuesDirs:
            files = glob.glob(valuesDir + "/string*")
            for file1 in files:
                stringResourceFiles.append(file1)

        print stringResourceFiles
        return stringResourceFiles
