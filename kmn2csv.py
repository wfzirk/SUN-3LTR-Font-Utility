# https://stackoverflow.com/questions/867866/convert-unicode-codepoint-to-utf8-hex-in-python

import fontforge
import os
import sys
import csv

from util import getUnicode
from bfConfig import readCfg, bfVersion 
import logging
from bfLog import log_setup
from array2xlsx import array2xlsx

'''
def getUnicode(str):
    #log_info('getunicode', str)
    a = chr(int(str,16)).encode('utf-8')
    #log_info('getunicode hex:'+str+' unicode:'+ a.hex())  # "+' '+a.decode('utf-8'))
    return a.decode('utf-8')
'''
   
# parse kmn file and generate csv file for documentation

def read_kmn(kmnfile):
    #cfg = json.load(open('config.json'))["enColumns"]
    cfg = readCfg()
    enc = cfg["enColumns"]
    DEBUG = cfg["debug"] == "true"
    cnt = 0
    kmnAry = []
    fr = open(kmnfile, 'r')
    #fw = open(outfile, 'w' ,encoding='utf8')
    csvReader = csv.reader(fr, delimiter='+')
    #csvWriter = csv.writer(fw, delimiter=',', lineterminator='\n')
    kerrors = False
    for row in csvReader:
        l = len(row)
        if l == 3:
            if '>'  in row[1]:
                # 'Aaron' + ' ' > U+Eb0d   c		 Acts 7:40
                csvRow = [None, None, None, None]
                #log_info(row)
                ref = row[2][4:].strip()[1:].strip()
                unicode = row[2][:4].lower().strip()
                name = row[0].strip().strip('\"').strip("\'")
                if len(unicode) != 4:
                    logging.error('invalid unicode %s %s',unicode, name)
                    kerrors = True
                if unicode[:1] != 'e':
                    logging.error('invalid unicode %s %s',unicode, name)
                    kerrors = True
                #unicode = row[2].split(' ').strip().strip('\"').strip("\'").lower()
                uic = getUnicode(unicode)
                name = row[0].strip().strip('\"').strip("\'")
                csvRow[enc["index_font"]] = uic
                csvRow[enc["index_name"]] = name
                csvRow[enc["index_unicode"]] = unicode
                csvRow[enc["index_ref"]] = ref
                logging.info('%s %s %s %s',uic.encode().hex(), name, unicode, ref)
                kmnAry.append(csvRow)
                #csvWriter.writerow(csvRow)

    fr.close()
    
    if kerrors:
        return 1
        
    name_sort = sorted(kmnAry, key=lambda x: x[enc["index_name"]].lower())
    
    # note: need to sort this by name

    return name_sort


def main(*ffargs):
    lgh = log_setup('Log/'+__file__[:-3]+'.log') 
    logging.info('version %s', bfVersion)
    rc = 0

    args = []
    cnt = 0
    for a in ffargs[0]:
        logging.debug('%d %s',cnt,a)
        args.append(a)
        cnt += 1
        print('args',cnt,a)
        
    if len(args) == 3: 
        namelist = args[1]
        outFile = args[2]
        try:
            kmnAry = read_kmn(namelist)
            
            if kmnAry:
                if kmnAry == 1:
                    rc = 1
                else:    
                    cfg = readCfg()
                    array2xlsx(kmnAry, outFile[:-4]+'.ods', csv=True)
            else:
                rc = 1
        except Exception as e:
            logging.exception("fatal error %s",e)
            rc = 3
    else:
        logging.error("\nsyntax: fontforge -script kmn2csv.py %kmn%.kmn kmn%kmn%.csv")
        logging.error("  i.e. - script Python script file,  SUN7_251.kmn kmnSUN7_251.csv")
        rc = 1
    
    if rc == 0:
        logging.info('done file is in %s',outFile[:-4]+'.ods')
    else:
        logging.error("failed status = %s",rc)
    
    #closeLogFile(lgh)
    #sys.exit(rc)
    return(rc)

if __name__ == "__main__":
   
    logging.info(': '.join(sys.argv))
    rc = main(sys.argv)    
    sys.exit(rc)