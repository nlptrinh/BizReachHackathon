import os
import json


def write(file, obj):
    """ Write the obj as json to file.
    It will overwrite the file if it exist
    It will create the folder if it doesn't exist.
    Args:
        file: the file's path, like : ./tmp/INFOX/repo_info.json
        obj: the instance to be written into file (can be list, dict)
    Return:
        none
    """
    path = os.path.dirname(file)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(file, 'w') as write_file:
        write_file.write(json.dumps(obj))
    print('finish write %s to file....' % file)


def read(path):
    if os.path.exists(path):
        with open(path) as f:
            result = json.load(f)
        return result
    else:
        raise Exception('no such file %s' % path)


def try_read(path):
    if os.path.exists(path):
        try:
            return read(path)
        except:
            return None
    return None
