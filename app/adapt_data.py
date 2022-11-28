import os
import fnmatch
import sys
import argparse

files = []

def startAdaption(path):
    print("... started adaption of files")
    listOfFiles = os.listdir(path)
    pattern = "*.pl"
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            files.append(path + entry)

    for file in files:
        with open(file, 'r') as input :
            filedata = input.read()

        # TBD - find better way to search and replace  
        filedata = filedata.replace('%:- not no_ab(', ':- not no_ab(')
        filedata = filedata.replace(':- not no_ab(', '%:- not no_ab(')

        with open(file, 'w') as output:
            output.write(filedata)

def stuckAtFaults(path):
    listOfFiles = os.listdir(path)
    pattern = "*.pl"
    
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            files.append(path + entry)

    for file in files:
        with open(file, 'r') as input :
            filedata = input.read()

        # TBD - find better way to search and replace  
        filedata = filedata.replace('ab_', 'ab(comp_')
        filedata = filedata.replace('gat', 'gat)')

        filedata = filedata

        with open(file, 'w') as output:
            output.write(filedata)