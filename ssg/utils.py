import os
import fnmatch
import shutil
import inspect


def print_parse_exception(exc, filename=None):
    msg = "Parse Error "
    if filename:
        msg += "while compiling {0}".format(filename)
    msg += ": " + exc.msg + "\n"
    msg += exc.line + "\n"
    msg += " "*(exc.column-1) + "^"
    print(msg)

# ===================================================================================
# I/O
# ===================================================================================

def walk_folder(root='.'):
    for subdir, dirs, files in os.walk(root):
        reldir = subdir[len(root):] if subdir.startswith(root) else subdir
        reldir = reldir.lstrip('/')
        for filename in files:
            yield os.path.join(reldir, filename)


def open_file(path, mode='rb', create_dir=False, create_mode=0o755):
    # Opens the given path. If create_dir is set, will
    # create all intermediate folders necessary to open
    try:
        newfile = open(path, mode)
    except IOError:
        # end here if not create_dir
        if not create_dir:
            raise
        newfile = None

    if not newfile:
        # may raise OSError
        filedir = os.path.split(path)[0]
        os.makedirs(filedir, create_mode)
        newfile = open(path, mode)

    return newfile


def read_file(path, mode='r'):
    data = None
    try:
        f = open_file(path, mode)
        data = f.read()
        f.close()
    except IOError as e:
        #print "failed to read file: " + path + ": " + str(e)
        raise e
    return data


def get_file_lines(path):
    lines = []
    try:
        f = open_file(path, 'r')
        lines = f.readlines()
        f.close()
    except Exception as e:
        print "failed to read file: " + path + ": " + str(e)
    return lines


def write_file(path, data, mode='w', overwrite=False):
    if isinstance(data, list):
        write_list_to_file(path, data, mode, overwrite)
        return

    if path_exists(path) and not overwrite:
        return

    outfile = open_file(path, mode)
    outfile.write(data)
    outfile.close()


def write_list_to_file(path, data, mode='w', overwrite=False):
    if not isinstance(data, list):
        raise TypeError("Second parameter 'data' must be of type 'list'")

    if path_exists(path) and not overwrite:
        return False

    outfile = open_file(path, mode, True)
    outfile.writelines(data)
    outfile.close()


def copy_file(src, dst, create_dir=True, create_mode=0o755):
    try:
        shutil.copy2(src, dst)
    except IOError:
        if not create_dir:
            raise
        # may raise OSError
        filedir = os.path.split(dst)[0]
        os.makedirs(filedir, create_mode)
        shutil.copy2(src, dst)


def create_directory(path, create_mode=0o755):
    if not path:
        return False
    try:
        os.mkdir(path, create_mode)
    except OSError as e:
        print "Error: " + path + " already exists: " + str(e)
        return False
    return True


def remove_directory(root):
    if not path_exists(root):
        return True
    if not os.path.isdir(root):
        print "Error removing directory: " + root + " is not a valid directory."
        return False
    try:
        shutil.rmtree(root)
    except Exception as e:
        print "Failed to remove " + root + ": " + str(e)
        return False
    return True

def directory_empty(path):
    return (len(os.listdir(path)) == 0)


def path_exists(path):
    return os.path.exists(path)


def get_extension(path):
    if not path_exists(path):
        raise Exception(path + " does not exist.")
    filename, ext = os.path.splitext(path)
    return ext.replace(".", "")


def get_filename(path):
    if not path_exists(path):
        raise Exception(path + " does not exist.")
    parts = path.replace("\\", "/").split("/")
    return parts[len(parts) - 1]

# TODO: create path class
def get_filename_no_extension(path):
    if not path_exists(path):
        raise Exception(path + " does not exist.")
    filename, ext = os.path.splitext(path)
    parts = filename.replace("\\", "/").split("/")
    return parts[len(parts) - 1]

def normalize_path(path, delim="/"):
    return path.replace("\\", delim)

def normalize_directory(dir, delim="/"):
    d = dir.replace("\\", delim)
    d = d + delim if d[-1] != delim else d
    return d

def get_current_dir():
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# ===================================================================================

def matches_pattern(pattern, filepath):

    def _is_match(pattern_list, token_list):
        if not pattern_list or not token_list:
            return False
        i, j = 0, 0
        while True:
            if pattern_list[j] == '**':
                if j+1 == len(pattern_list): 
                    return True
                if _is_match(pattern_list[j+1:], token_list[i:]):
                    return True
                else:
                    i+=1 
            elif fnmatch.fnmatch(token_list[i], pattern_list[j]):
                i+=1
                j+=1
            else:
                return False
            if i==len(token_list) and j==len(pattern_list):
                return True
            if i==len(token_list) or j==len(pattern_list):
                return False

    return _is_match(pattern.strip('/').split('/'), 
                     filepath.strip('/').split('/'))

