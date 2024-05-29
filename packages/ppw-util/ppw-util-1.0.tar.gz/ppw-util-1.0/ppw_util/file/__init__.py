# -*- coding: utf-8 -*
# #!/usr/bin/python3

# How to use: from ppw_util.file import File
import os

class File:

    _file_path: str = None

    def __init__(self, file_path: str):
        self._file_path = file_path

    def __del__(self):
        pass

    def get_wc(self):
        count = -1
        if(os.path.isfile(self._file_path)):
            for count,line in enumerate(open(self._file_path,'rU')):
                count += 1
        return count

    def process_by_line(self, process_target):
        with open(self._file_path) as f:
            line_num = 0
            while True:
                line_str = f.readline()
                if not line_str: 
                    break
                need_stop = process_target(line_num, line_str)
                if need_stop is True:
                    break
                line_num = line_num + 1

