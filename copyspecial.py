#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Copyspecial Assignment"""

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import re
import os
import shutil
import subprocess
import argparse

__author__ = "Rob Spears (GitHub: Forty9Unbeaten)"


def get_special_files(folder):
    file_dict = {'file_paths': [], 'files_found': 0, 'files_searched': 0}
    file_names = []
    reg_exp = r'__\w+__'

    for root, directories, files in os.walk(folder):
        for file in files:
            # Search files for 'special files'
            # and print error if duplicate filenames
            # are encountered
            if re.search(reg_exp, file):
                if file in file_names:
                    raise Exception(
                        f'\n\n\tError: Two files found with same filename:\t{file}\n')
                else:
                    file_names.append(file)
                    path = os.path.abspath(file)
                    file_dict['file_paths'].append(path)
                    file_dict['files_found'] += 1
        file_dict['files_searched'] += 1
    return file_dict


def print_file_paths(file_dict):
    file_paths = file_dict['file_paths']
    files_found = file_dict['files_found']
    files_searched = file_dict['files_searched']

    for file in file_paths:
        print('\n\tSpecial File Found!')
        print('\t-------------------')
        print(f'\tPath:\t{file}')
    print(f'\n\tFiles Found: {files_found}')
    print(f'\tFiles Searched: {files_searched}\n')


def copy_files(paths, dest_dir):
    copied_files = 0
    for file in paths:
        shutil.copy2(file, dest_dir)
        copied_files += 1
    print(f'\n\tFiles Copied:\t{copied_files}\n')


def main():
    # This snippet will help you get started with the argparse module.
    parser = argparse.ArgumentParser()
    parser.add_argument('--todir', help='dest dir for special files')
    parser.add_argument('--tozip', help='dest zipfile for special files')
    parser.add_argument(
        'srcdir', help='source dir for special files')
    args = parser.parse_args()

    src_dir = args.srcdir
    to_dir = args.todir
    to_zip = args.tozip

    file_info = get_special_files(src_dir)
    file_paths = file_info['file_paths']

    if to_dir and to_zip:
        copy_files(file_paths, to_dir)
    elif to_dir:
        copy_files(file_paths, to_dir)
    elif to_zip:
        pass
    else:
        print_file_paths(file_info)


if __name__ == "__main__":
    main()
