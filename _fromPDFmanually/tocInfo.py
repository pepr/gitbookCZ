#!python3

'''Skript pro zjištění obsahu knihy v originále a extrakce obsahu z CZ.


'''

import collections
import os
import re

def buildENtoc(fname):
    toc = []
    rex = re.compile(r'^\s*(?P<num>\d+\.(\d+)?)\s+(?P<title>.+?)\s*$')
    with open(fname, encoding='utf-8') as f:
        for line in f:
            m = rex.match(line)
            if m:
                toc.append((m.group('num'), m.group('title')))
    return toc


def buildCZtoc(fname):
    toc = []

    # TOC line example: "1.1 Správa verzí -- 17" where '--' is the Em-dash.
    rex = re.compile(r'^\s*(?P<num>\d+\.(\d+)?)\s+(?P<title>.+?)\s*(\u2014.*)?$')

    page_header = None  # init -- the page header string (just below form feed)

    with open(fname, encoding='utf-8') as f:

        status = 0
        while status != 888:

            line = f.readline()

            if status == 0:
                if line.startswith('\f'):             # FormFeed
                    status = 1

            elif status == 1:                         # the page header line
                page_header = line.rstrip()
                if page_header.startswith('Obsah'):
                    status = 2                        # start collecting TOC
                else:
                    status = 0                        # wait for next FF

            elif status == 2:
                if line.startswith('\f'):             # FormFeed ends the TOC
                    status = 888
                else:
                    m = rex.match(line)
                    if m:
                        toc.append((m.group('num'), m.group('title')))

    return toc



if __name__ == '__main__':

    fname_input = 'scott_chacon_pro_git_CZ.txt'
    text_dir = os.path.abspath('../text')
    print(text_dir)

    # Create the subdirectory for the texts if it does not exist.
    if not os.path.isdir(text_dir):
        os.mkdir(text_dir)

    # Get the English TOC information from the text file (captured as text
    # from the official HTML page).
    tocEN = buildENtoc('tocEN.txt')
    for num, title in tocEN:
        print(num, title)
    print('------------')

    # Get the Czech TOC information from the text file (captured and manually
    # edited PDF with the CZ.NIC translation).
    tocCZ = buildCZtoc('scott_chacon_pro_git_CZ.txt')
    for num, title in tocCZ:
        print(num, title)
    print('------------')

    # Compare the EN and CZ tables of contents.
    for i, (numEN, titleEN) in enumerate(tocEN):
        print(numEN, titleEN)
        print(tocCZ[i][0], tocCZ[i][1])
        print()
    print('------------')

