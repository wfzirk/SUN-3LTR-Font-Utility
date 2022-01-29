# create list of alternative words based on unicode
# requires input list sorted by unicode
# syntax:  alternative.py primary.csv kmn.csv out.csv

import sys
import csv
import logging
from bfLog import log_setup
from bfConfig import bfVersion

PUNICOL = 2     # unicode column in primary
KUNICOL = 2     # unicode column in kmn
PNAMECOL = 1    # name column in primary
KNAMECOL = 1    # name column in kmn

def read_pri(f):
    logging.info('read pri %s', f)
    pd = {}
    with open(f, encoding='utf8', newline='') as csvfile:
        data = list(csv.reader(csvfile))
        for i in data:
            #symbol = i[PGLYPHCOL]
            unicode = i[PUNICOL].strip().lower()
            name = i[PNAMECOL]
            pd[unicode] = [name]
            logging.debug('%s %s', unicode, name)
    return pd
 
def read_kmn(f, pd):   #, pri):
    logging.info('read kmn %s', f)
    
    with open(f, encoding='utf8', newline='') as csvfile:
        data = list(csv.reader(csvfile))
        for i in data:
            unicode = i[KUNICOL].strip().lower()
            name = i[KNAMECOL]
            if unicode in pd:
                if pd[unicode][0] == name:
                    continue
                pd[unicode].append(name)
                logging.debug('%s %s', unicode, name)
            else:
                pd[unicode] = [unicode]
                pd[unicode].append("**ERROR does not exist***")
                logging.error('%s %s does not exist', unicode, name)
    return pd 

def writeAlt(outfile, data):
    ary = []
    logging.info('saving data')
    for r in data:
        row = data[r]
        logging.debug('%s %s %s',r, len(row),row)
        row = data[r]
        if len(row) > 1:       # more than one name for unicode
            unicode = r
            name = row[0]         
            row.pop(0)
            logging.debug('%s %s %s',unicode, name, row)
            altname = ""
            for d in row:
                altname=altname+','+d
            #x = unicode+','+ name +',"'+ altname.strip(',')+'"'
            line = []
            #ary.append([unicode+','+ name +',"'+ altname.strip(',')+'"'])
            line.append(unicode)
            line.append(name)
            line.append(altname.strip(','))
            ary.append(line)
            
    name_sort = sorted(ary, key=lambda x:x[1].lower())
    with open(outfile, 'w', encoding='utf8') as f:
        for v in name_sort:
            f.write(v[0]+','+ v[1] +',"'+ v[2]+'"\n')
    logging.info('saved to %s',outfile)
    
if len(sys.argv) > 3: 
    lgh = log_setup('Log/'+__file__[:-3]+'.log')
    logging.info('version %s', bfVersion)
    priData = read_pri(sys.argv[1])    #primary word list
    
    kmnData = read_kmn(sys.argv[2], priData)   # kmn file list
    
    writeAlt(sys.argv[3], kmnData)    # outfile

else:
    print("\nsyntax: fontforge -script alternative.py primary.csv kmn.csv output.csv")
    print("Creates a list of unicodes and names with alternative names")

print ('\n*** done ****')


