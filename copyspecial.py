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
                        ('\n\n\tError: Two files found' +
                         'with same filename:{}\t\n'.format(file)))
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
        print('\tPath:\t{}'.format(file))
    print('\n\tFiles Found: {}'.format(files_found))
    print('\tFiles Searched: {}\n'.format(files_searched))


def copy_files(paths, dest_dir):
    copied_files = 0

    # copy files and attempt to preserve file metadata
    for file in paths:
        try:
            shutil.copy2(file, dest_dir)
            copied_files += 1
        except FileNotFoundError:
            os.makedirs(os.path.abspath(dest_dir))
            shutil.copy2(file, dest_dir)
            copied_files += 1

    print('\n\tFiles Copied:\t{}\n'.format(copied_files))


def zip_files(paths, dest_file):
    print("\n\tThe command I'm executing:")
    print("\tzip -j {} {}\n".format(dest_file, ' '.join(paths)))
    # produce shell command to make/overwrite zip file
    # containing all special files
    subprocess.call(['zip', '-j', str(dest_file)] + paths)


def main():
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
        zip_files(file_paths, to_zip)
    elif to_dir:
        copy_files(file_paths, to_dir)
    elif to_zip:
        zip_files(file_paths, to_zip)
    else:
        print_file_paths(file_info)


if __name__ == "__main__":
    main()
