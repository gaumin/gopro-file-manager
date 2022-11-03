import os
from datetime import datetime
import sys

NAME_LENGTH = 4
ALLOWED_EXTENSIONS = ('.jpg', '.m4v', '.mp4', '.thm', '.lrv')

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    DIR = os.path.dirname(os.path.realpath(sys.executable))
elif __file__:
    DIR = os.path.dirname(__file__)

#Remove before PUSH
#DIR = 'C:\\Users\\promind\\Desktop\\PY\\Code\\file_rename\\gopro'

print('CURRENT DIR ' + DIR)

# Command promt to ask user to proceed
response = ""
while (response != "y" or response != "n"):
    if (response == "n"):
        print('Exiting...')
        exit()
    if (response == "y"):
        print('Confirmed !!!')
        break
    response = input("Please confirm to rename files (y/n): ")

print(response)


def readFilesToList(dir):
    """
    Read file name from 'dir' and return a dict as a result
    """
    filelist = {}

    for files in os.listdir(dir):
        file_name, file_extension = os.path.splitext(dir + '\\' + files)

        # checks if the file is not a folder of exe
        if(file_extension.lower() in ALLOWED_EXTENSIONS):
            file_url = file_name + file_extension
            date = os.path.getmtime(file_url)
            filelist[file_name[len(dir)+1:] + file_extension] = datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
    return filelist

def createDirectory(path):
    """
    Check whether the specified path exists or not
    """
    isExist = os.path.exists(path)

    if not isExist:
        os.makedirs(path)
        print("The new directory is created!")

def renameSingleFile(current, new):
    """
    Renames 'current' file name to 'new'. Full file path needed
    """
    try:
        os.rename(current, new)
    except:
        print(f'Error. Cant rename file: {current}')

def renameFilesInDirecotry(dir):
    '''Renames all files in dir directory.
    '''
    current = 0

    filelist = readFilesToList(dir)

    # Sort by file datestamp
    filelist = sorted(filelist.items(), key = lambda kv: kv[1])

    for f in filelist:
        current +=1
        new_name = str(current)
        length = 1;

        while length < NAME_LENGTH:
            new_name = '0' + new_name
            length = len(str(new_name))

        renameSingleFile(dir+'\\'+f[0], dir+'\\' + new_name + '.'+folder)

def moveFilesToDir(dir):

    filelist = readFilesToList(DIR)

    for f in filelist.items():
        ext = f[0].split('.')[1]
        path_current = DIR + '\\' + f[0]
        path_new = DIR + '\\' + ext + '\\' + f[0]

        createDirectory(DIR + "\\" + ext)
        os.rename(path_current, path_new)


# step1 - move files to directories by extesnions
moveFilesToDir(DIR)

# step2 - iterate through each of folder and rename files
for folder in os.listdir(DIR):
    if(folder[-4:] != '.exe'):
        renameFilesInDirecotry(DIR + '\\' + folder)
