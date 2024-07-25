import os
import re
import codecs
import requests
import xml.etree.ElementTree as ET
import pygount

import local_file

LOCAL_DATA_PATH = 'C:\\Users\\37583\\Documents\\tmp'
RENEW_FLAG = False
KEEP_LANGUAGE = ['.py', '.cpp', '.c', '.java']
# KEEP_LANGUAGE = ['.java']


'''
def extract_libs(file):
    libs = []
    with codecs.open(file, 'r', 'utf-8') as f:
        try:
            for t in f.readlines():
                if t[:7] == 'import ':
                    if t[7:][:6] == 'static':
                        continue
                    lib_name = t[7:-3]
                    libs.append(lib_name)
        except:
            pass
    return libs

def get_libs(repo):
    all_libs = set()
    for file in get_source_files(repo):
        all_libs |= set(extract_libs(file))
    # print('%s libs: %s' % (repo, all_libs))
    return all_libs
'''

def get_source_files(repo):
    folder = os.path.join(LOCAL_DATA_PATH, repo.replace('/', '_'))
    if (not os.path.exists(folder)) or RENEW_FLAG:
        os.system('git clone --depth=1 https://github.com/%s.git %s' % (repo, folder))
    java_files = []
    for (fpath, dirs, fs) in os.walk(folder):
        for file_name in fs:
            file_full_name = os.path.join(fpath, file_name)
            fileoriname, file_extension = os.path.splitext(file_full_name)
            if file_extension in KEEP_LANGUAGE:
                java_files.append(file_full_name)
    return java_files

def extract_LOC(file):
    analysis = pygount.source_analysis(file, 'pygount')
    try:
        return analysis.code, analysis.documentation
    except:
        return 0, 0

def count_line(repo):
    code_line = 0
    comment_line = 0
    for file in get_source_files(repo):
        x, y = extract_LOC(file)
        code_line += x
        comment_line += y
    return code_line, comment_line

def readability_score(repo):
    code_line, comment_line = count_line(repo)
    return 1.0 * comment_line / code_line

def fetch_raw_data(url):
    save_path = os.path.join(os.path.join(LOCAL_DATA_PATH, 'raw_data_cache'), url.replace('/', '-').replace(':',''))
    if (os.path.exists(save_path)) and (not RENEW_FLAG):
        try:
            return local_file.read(save_path)
        except:
            pass
    ret = requests.get(url).text
    local_file.write(save_path, ret)
    return ret

def fetch_readme(repo):
	url = 'https://github.com/%s/raw/master/README.md' % repo
	try:
		ret = fetch_raw_data(url)
	except:
		print('Error on fetching readme:', url)
		ret = None
	return ret

def fetch_pom(repo):
    url =  'https://github.com/%s/raw/master/pom.xml' % repo
    try:
        ret = fetch_raw_data(url)
    except:
        print('Error on fetching pom.xml:', url)
        ret = None
    return ret

def get_libs(repo):
    try:
        pom_str = fetch_pom(repo)
        if pom_str is None:
            return []
        xmlstring = re.sub(' xmlns="[^"]+"', '', pom_str, count=1) # TODO(luyao) other solution?
        root = ET.fromstring(xmlstring)
        libs = []
        for dep in root.iter('dependency'):
            libs.append(dep.find('artifactId').text)
        return libs
    except:
        return []

def get_tree_of_libs(libs):
    p = 0
    tot = 0
    ch = {}
    ch[0] = {}
    info = {}
    info[0] = "All"
    for lib in libs:
        t = lib.split('.')
        for x in t:
            if x not in ch[p]:
                tot += 1
                info[tot] = x
                ch[tot] = {}
                ch[p][x] = tot
                p = tot
            else:
                p = ch[p][x]

    def dfs(x):
        if len(ch[x]) == 0:
            return {"name": info[x]}
        child = []
        for c in ch[x]:
            child.append(dfs(ch[x][c]))
        return {"name": info[x], "children": child}

    return dfs(0)


# extract_LOC("..\\data\\test.java")
# readability_score("alibaba/arthas")
# get_tree_of_libs("xgdsmileboy/GenPat")
