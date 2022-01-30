import re
import csv
import pandas as pd

# Helper file for formatting data
with open('nasdaq_screener_1.csv') as f:
    for line in f:
        x = re.compile(r'''\s*([^,"']+?|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')\s*(?:,|$)''', re.VERBOSE)
        y = x.findall(line)
        print(y)

with open('nasdaq_screener_3.csv') as g:
    # read = csv.reader(g, delimiter=',')
    list1 = []
    for line in g:
        print(line.split(',')[0] + ',' + line.split(',')[1])