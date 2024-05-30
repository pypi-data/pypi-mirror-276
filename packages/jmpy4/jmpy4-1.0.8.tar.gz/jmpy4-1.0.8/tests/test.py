# -*- coding: utf-8 -*-
"""
Created on 2020/6/17 8:58 下午
---------
@summary:
---------
@author: Boirs
"""
from multiprocessing import freeze_support

from jmpy.encrypt_py import start_encrypt

input_file_path = "test.py"
if __name__ == "__main__":
    freeze_support()
    start_encrypt(input_file_path=input_file_path, output_file_path=None, ignore_files=None, except_main_file=0)
