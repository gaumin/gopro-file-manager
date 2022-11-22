import os
import sys
import logging
from datetime import datetime

# Number of characters for the new name of file. Remaining characters are filled with zeros i.e. 0001.mp4
FILE_NAME_LENGTH = 4

# Number of characters for size record in log.txt file. Remaining characters are filled with zeros i.e. 0024.27
FILE_SIZE_LENGTH = 5

# Files smaller than this value (in megabytes) will be marked with "s_" prefix, which stands for 'small'
MINIMUM_FILE_SIZE = 20

# Files with those types of extensions will be moved and renamed. Other types of files will remain untouched
ALLOWED_FILE_EXTENSIONS = ('jpg', 'm4v', 'mp4', 'thm', 'gpr', 'lrv')

# Indicates which kind of files should be included into size check to set a prefix "s_"
VIDEO_FILES_EXTENSIONS = ('m4v', 'mp4')

# Determine if application is a script file or frozen exe. Required when creating an exe file to get path to working directory
if getattr(sys, 'frozen', False):
    DIR = os.path.dirname(os.path.realpath(sys.executable))
elif __file__:
    DIR = os.path.dirname(__file__)

# Location to files when testing a code
DIR = 'D:\\footage\\gopro\\'

logging.basicConfig(
    filename=DIR +"\\"+ "log.txt", force=True,
    format = '%(asctime)s %(levelname)-8s %(message)s',
    level = logging.INFO,
    datefmt = '%Y-%m-%d %H:%M:%S')

print('Current directory: ' + DIR)

# Ask user's approval to proceed-
response = ""
while (response != "y" or response != "n"):
    if (response == "n"):
        print('Exiting...')
        exit()
    if (response == "y"):
        print('Confirmed !!!')
        break
    response = input("Confirm to rename and move files (y/n): ")

def read_files(dir):
    """
    Read file names from 'dir' and return a dict as a result
    """
    filelist = {}

    for files in os.listdir(dir):
        file_name, file_extension = os.path.splitext(dir + '\\' + files)

        # checks if the file is not a folder and belongs to one of allowed file extensions
        if(file_extension.lower()[1:] in ALLOWED_FILE_EXTENSIONS):
            file_path = file_name + file_extension
            date = os.path.getmtime(file_path)
            filelist[file_name[len(dir)+1:] + file_extension] = [datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S'),
                                                                 get_file_size(file_path),
                                                                 file_extension.lower()]
    return filelist

def create_directory(path):
    """
    Check whether the specified path exists or not
    """
    isExist = os.path.exists(path)

    if not isExist:
        os.makedirs(path.upper())
        print(f"New directory {path} has been created!")

def set_prefix(file_size):
    """
    Returns a special prefix "s_" if file size is smaller than defined, otherwise returns empty string
    """
    if (file_size < MINIMUM_FILE_SIZE):
        return "s_"
    else:
        return ""

def rename_file(current, new, file_size):
    """
    Renames 'current' file name to 'new'. Working on absolute file path
    """

    old_path = DIR + '\\' + current.split('\\')[-1]

    try:
        os.rename(current, new)
        logging.info(f'{file_size}  {remove_double_backslash(old_path)} --> {remove_double_backslash(new)}')

    except:
        print(f'Error. Cant rename file: {remove_double_backslash(current)}')
        logging.error(f'Cant rename file: {remove_double_backslash(current)}')

def rename_files_in_directory(dir):
    """
    Renames all files in directory
    """
    current = 0

    filelist = read_files(dir)

    # Sort by file datestamp
    filelist = sorted(filelist.items(), key = lambda kv: kv[1][0])

    for f in filelist:
        current +=1
        new_name = str(current).zfill(FILE_NAME_LENGTH)

        prefix = ""
        if (f[1][2][1:] in VIDEO_FILES_EXTENSIONS):
            prefix = set_prefix(f[1][1])

        formated_file_size = format_file_size_record(str(f[1][1]))

        rename_file(dir + '\\' + f[0],
                    dir +'\\' + prefix + new_name + '.' + folder,
                    formated_file_size)

def move_files_to_directory(dir):
    """
    Moves files to newly created directories
    """

    filelist = read_files(DIR)

    if len(filelist) != 0:
        msg = str(ALLOWED_FILE_EXTENSIONS).replace("(", "").replace(")", "").replace(chr(39), "")
        print(f'Files found: {len(filelist)}, allowed file extensions: {msg}')
        logging.info(f'Files found: {len(filelist)}, allowed file extensions: {msg}')

        for f in filelist.items():
            ext = f[0].split('.')[1]
            path_current = DIR + '\\' + f[0]
            path_new = DIR + '\\' + ext + '\\' + f[0]

            create_directory(DIR + "\\" + ext)
            os.rename(path_current, path_new)
    else:
        print('No files found. Exiting..')
        logging.info('No files found. Exiting..')
        exit()

def remove_double_backslash(path):
    """
    Replace double backslash (\\) to a single (\)
    """
    return path.replace(chr(92)+chr(92), chr(92))

def get_file_size(path):
    """
    Returns file size in MB
    """
    if os.path.isfile(path):
        file_info = os.stat(path)
        return round(file_info.st_size/1048576.0, 2)

def format_file_size_record(file_size):
    """
    Converts file size (string) to proper format for logging into log file
    """
    whole_number = file_size.split(".")[0]
    decimal_number = file_size.split(".")[1]

    return whole_number.zfill(FILE_SIZE_LENGTH) + '.' + decimal_number.zfill(2) + ' MB'

# Execute
# step1 - move files to directories by extensions
move_files_to_directory(DIR)

# step2 - iterate through each of folder and rename files
for folder in os.listdir(DIR):
    file_name, file_extension = os.path.splitext(folder)

    if(file_extension =="" and file_name.lower() in ALLOWED_FILE_EXTENSIONS):
        rename_files_in_directory(DIR + '\\' + folder)
