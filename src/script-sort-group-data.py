import os
import lizard
import csv
import subprocess

# MIT License
#
# Copyright (c) 2021 Matthew Schweiss
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Partially from https://stackoverflow.com/questions/229186/os-walk-without-digging-into-directories-below

def walklevel(path, depth = 1):
    """It works just like os.walk, but you can pass it a level parameter
       that indicates how deep the recursion will go.
       If depth is 1, the current directory is listed.
       If depth is 0, nothing is returned.
       If depth is -1 (or less than 0), the full depth is walked.
    """
    # If depth is negative, just walk
    # Not using yield from for python2 compat
    # and copy dirs to keep consistant behavior for depth = -1 and depth = inf
    if depth < 0:
        for root, dirs, files in os.walk(path):
            yield root, dirs[:], files
        return
    elif depth == 0:
        return

    # path.count(os.path.sep) is safe because
    # - On Windows "\\" is never allowed in the name of a file or directory
    # - On UNIX "/" is never allowed in the name of a file or directory
    # - On MacOS a literal "/" is quitely translated to a ":" so it is still
    #   safe to count "/".
    base_depth = path.rstrip(os.path.sep).count(os.path.sep)
    for root, dirs, files in os.walk(path):
        yield root, dirs[:], files
        cur_depth = root.count(os.path.sep)
        if base_depth + depth <= cur_depth:
            del dirs[:]

"""
with open("inda/2021/ta-groups-2021.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
       print(row)
"""

def get_all_student_files(directory):
    files = []
    students = [ (f.path, f.name) for f in os.scandir(directory) if f.is_dir()]
    return students

# this ugly code is mine :C
"""
with open("inda-repos-students.csv", "w") as csvfile:
    for root, dirs, files in walklevel(".", depth = 2):
        for dir in dirs:
            path = os.path.join(root, dir)
            if len(path.split(sep="/")) < 4:
                continue
            proc = subprocess.call(['lizard', path, '--csv', '--exclude', '"^.*Test.java$"', '-l', 'java'], bufsize=1, universal_newlines=True, stdout=csvfile)
"""
# för varje student repo, gör lizard
# kan jag komponera den korrekta CSV-filen direkt?
    # hitta studenten i rics fil
    # appendera bara gruppnivå och TA på den?

def call_lizard(path, destination):
    """
    INPUT   path: path to all student repos for current course iteration
    OUTPUT  writes to a new file
    """
    with open(destination, "w") as csvfile:
        for student in get_all_student_files(path):
            proc = subprocess.call(['lizard', student[0], '--csv', '--exclude', '"^.*Test.java$"', '-l', 'java'], bufsize=1, universal_newlines=True, stdout=csvfile)

def setup_student_ta_and_experience(path):
    """
    INPUT   path: path där ta-groups-20xx.csv ligger
    OUTPUT  dict: en dictionary där varje student har en (TA, skill level)-tuple
    """
    dict = {}
    with open(path, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # row[0] = student, row[1] = ta, row[2] = experience
            dict[row[0]] = (row[1], row[2])
    return dict

def main():
    path_repos = "/Users/linusostlund/Documents/GitHub/kex/inda" 
    destination = "inda-repos-students.csv"
    dict = setup_student_ta_and_experience("/Users/linusostlund/Documents/GitHub/kex/inda/2021/ta-groups-2021.csv")
    call_lizard(path_repos, destination)

print(os.getcwd())