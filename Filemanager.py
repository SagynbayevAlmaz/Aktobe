import os
import time
from os import path


def MainMenu():
    print("Input '1' - work with files")
    print("Input '2' - work with directories")


def FileMenu():
    print("Input '1' - delete file")
    print("Input '2' - rename file")
    print("Input '3' - add content to this file")
    print("Input '4' - rewrite content of this file")
    print("Input '5' - return to the parent directory")

def DirMenu():
    print("Input '1' - rename directory")
    print("Input '2' - print number of files in it")
    print("Input '3' - print number of directories in it")
    print("Input '4' - list content of the directory")
    print("Input '5' - add file to this directory")
    print("Input '6' - add new directory to this directory")

def DeleteFiles(FileName):
    if os.path.exists(FileName): 
        os.remove(CurDir + '/' + FileName)
        print("File was deleted")
    else:
        print("File does not exist")

def RenameFiles(FileName, NewFileName):
    if os.path.exists(FileName) == False:
        os.rename(FileName, NewFileName)
        print("File was renamed")
    else:
        print("File does not exist")

def AddContent(Filename):
    with open(Filename , "a") as file:
        addcont = input('Input your  text to add this file: ')
        file.write(f'{addcont}\n')
        print("File was added")

def ReWrite(Filename):
    if os.path.exists(Filename):
        with open(Filename , "w") as file:
            cont = input('Input your  text to rewrite: ')
            file.write(f'{cont}\n')
            print("File  was rewrited")
    else:
        print("File does not exist")
    
def RetPar():
    print(os.path.abspath(os.curdir))
    os.chdir("..")
    print(os.path.abspath(os.curdir))

def RenameDir(DirName, NewDirName):
    if os.path.exists(DirName):
        os.rename(DirName, NewDirName)
        print("Directory was renamed")
    else:
        print("Directory does not exist")
def NumOfFiles():
    entries = os.listdir(CurDir)
    cnt =0
    for entry in entries:
        if os.path.isfile(entry):
            cnt += 1
    print("Number of files is" , str(cnt))

def NumOfDIrs():
    entries = os.listdir(CurDir)
    cnt =0
    for entry in entries:
        if os.path.isdir(entry):
            cnt += 1
    print("Number of directories is", str(cnt))

def ListOfCont():
    print(os.listdir(CurDir))

def NewFile(Filename):
    file = open(Filename, "w")
    file.close()
    print("File was created")

def NewDir(DirName):
    os.mkdir(DirName)

while(True):
    CurDir = os.getcwd()
    MainMenu()
    choose1 = int(input())
    print("Current directory is" + CurDir)

    if (choose1 == 1):
        FileMenu()
        choose2 = int(input())
        if(choose2 == 1):
            filename = input("Input name of file:")
            DeleteFiles(filename)
        elif(choose2 == 2):
            filename = input("Input name of file:")
            newfilename = input("Input new name of file:")
            RenameFiles(filename, newfilename)
        elif(choose2 == 3):
            filename = input("Input name of file:")
            AddContent(filename)
        elif(choose2 == 4):
            filename = input("Input name of file:")
            ReWrite(filename)
        elif(choose2 == 5):
            RetPar()
    
    elif(choose1 == 2):
        DirMenu()
        choose2 = int(input())
        if(choose2 == 1):
            dirname = input("Input name of directory:")
            newdirname = input("Input new name of directory:")
            RenameDir(dirname, newdirname)
        elif(choose2 == 2):
            NumOfFiles()
        elif(choose2 == 3):
            NumOfDirs()
        elif(choose2 == 4):
            ListOfCont()
        elif(choose2 == 5):
            filename = input("Input name of file:")
            NewFile(filename)
        elif(choose2 == 6):
            dirname = input("Input name of directory:")
            NewDir(dirname)