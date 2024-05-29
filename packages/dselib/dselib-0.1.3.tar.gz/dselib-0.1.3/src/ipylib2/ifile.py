# -*- coding: utf-8 -*-
import os  
import re 
import json 




def find_file(topdir, filename):
    _files = []
    for root, dirs, files in os.walk(top=topdir, topdown=True):
        for file in files:
            if re.search(filename, file) is not None:
                # OS 자동임시저장 파일 제거
                if re.search('^~', file) is None:
                    _files.append(os.path.join(root, file))
                else:
                    pass 
            else: 
                pass 
    return _files
            

def get_files(topdir, type='csv', fullpath=False):
    _files_ = []
    for root, dirs, files in os.walk(top=topdir, topdown=True):
        for file in files:
            if re.search(f'\.{type}$', file) is not None:
                if fullpath:
                    file = os.path.join(root, file)
                else:
                    pass 
                _files_.append(file)
            else: 
                pass 
    return _files_


def read_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        js = json.loads(f.read())
        f.close()
        return js 
