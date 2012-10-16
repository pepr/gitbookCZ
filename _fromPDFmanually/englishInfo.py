#!python3
'''\
Script for extraction of chapter titles, section titles, subsection 
titles, ... from the English original text sources. The text directory
is relative to this one -- see the body of the program.
'''

import os
import re
import sys

def sourceFiles(text_dir):

    # Check the existence of the directory.
    assert os.path.isdir(text_dir)

    # Get the list of subdirectories with the source files.    
    subdirs = []
    for sub in sorted(os.listdir(text_dir)):
        d = os.path.join(text_dir, sub)
        if os.path.isdir(d):
            subdirs.append(d) 
                             
    # Loop through subdirs and walk the sorted filenames.                        
    return subdirs


def extractEN():

                             
    toc = []
    page_headers = []
    headings = []

    # TOC line example: "1.1 Správa verzí -- 17"
    # where '--' is the Em-dash.
    patNum = r'(?P<num>(?P<num1>\d+)\.(?P<num2>\d+)?(\.(?P<num3>\d+))?)'
    patTOC = patNum + r'\s+(?P<title>.+?)(\s+\u2014)?(\s+(?P<pageno>\d+)\s*)'

    rexTOC = re.compile(r'^' + patTOC + r'$')
    rexHeadingU = re.compile(r'^\u2014\s+(?P<title>.+?)(\s+(?P<pageno>\d+)\s*)$')

    page_header = None  # init -- the page header string (just below form feed)

    with open(fname, encoding='utf-8') as f:

        status = 0
        while status != 888:

            line = f.readline()
            if line == '':
                status = 888                    # EOF

            if status == 0:             # -------
                if line.startswith('\f'):       # FormFeed
                    status = 1

            elif status == 1:           # ------- the page header lines before TOC
                page_headers.append(line.rstrip())

                m = rexHeadingU.match(line)
                if m and m.group('title') == 'Obsah':
                    status = 2                  # start collecting TOC
                else:
                    status = 0                  # wait for next FF

            elif status == 2:           # ------- collecting TOC
                if line.startswith('\f'):       # FormFeed ends the TOC
                    status = 3
                else:
                    m = rexTOC.match(line)
                    if m:
                        toc.append((m.group('num'), m.group('title')))

            elif status == 3:           # ------- the page header lines after TOC
                page_header = line.rstrip()
                page_headers.append(page_header)
                status = 4                      # wait for next FF

            elif status == 4:           # ------- text lines
                if line.startswith('\f'):       # FormFeed
                    status = 3
                else:
                    m = rexTOC.match(line)      # TOC-like line in the text
                    if m:
                        headings.append(line.rstrip())


    return toc, page_headers, headings



if __name__ == '__main__':

    # Auxiliary subdirectory for the extracted information.
    # Create it if it does not exist.
    aux_dir = os.path.abspath('info_aux_en')
    if not os.path.isdir(aux_dir):
        os.mkdir(aux_dir)

    # Get the directory with the text sources of the origina.
    text_dir = os.path.abspath('../../gitbook/text')
    
    toc = extractEN(text_dir)
    print(toc)
    sys.exit(1)
    
    # TOC
    with open(os.path.join(aux_dir, 'TOC.txt'), 'w', encoding='utf-8') as f:
        for num, title in toc:
            f.write('{} {}\n'.format(num, title))

