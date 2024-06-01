from tikos.tikos import AddExtractionFile, AddExtractionFiles, AddExtractionFileStream, AddExtractionFileStreams
from typing import List

def AddFile():
    requestId = 'b8d1c770-2b71-4273-a768-9cebc5b87ff2'
    authToken = '8d9f9bd7-c92f-4ce4-8f87-77180836f770'
    # files = [('README.1.md',open('README.1.md', 'rb'))]
    files = ('README.md','../README.md')

    rtnval = AddExtractionFile(requestId=requestId, authToken=authToken, fileObj=files)
    print(rtnval)

def AddFiles():
    requestId = 'b8d1c770-2b71-4273-a768-9cebc5b87ff2'
    authToken = '8d9f9bd7-c92f-4ce4-8f87-77180836f770'
    # files = [('README.md','../README.md'), ('LICENSE','../LICENSE')]
    files = [('README.md', open('../README.md', 'rb')), ('LICENSE', open('../LICENSE', 'rb'))]

    rtnval = AddExtractionFileStreams(requestId=requestId, authToken=authToken, fileObjs=files)
    print(rtnval)

def checkfile(files: List[object]=None):

    for fileObj in files:
        name = fileObj[0]
        fileLocation = fileObj[1]
        print(name, fileLocation)


if __name__ == '__main__':
    # ViewVersion()
    # Description()
    # AddRequest()
    # AddText()
    # AddFile()
    AddFiles()