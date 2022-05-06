# https://stackoverflow.com/questions/867866/convert-unicode-codepoint-to-utf8-hex-in-python

import fontforge
import os
import sys
import csv
#import traceback
from util import getUnicode, convert2csv, convertfiletype 
import logging
from bfLog import log_setup
from bfConfig import readCfg, bfVersion 
 
def read_csv(namelist, outfile):
    try:
        #cfg = json.load(open('config.json'))
        cfg = readCfg()
        if cfg["alias"] == "ENG":
            ixu = cfg["enColumns"]["index_unicode"]
        else:
            ixu = cfg["langColumns"]["index_unicode"]
        logging.info('read_csv namelist:%s outfile:%s',namelist,outfile)
        fr = open(namelist, 'r', encoding='utf8')
        fw = open(outfile, 'w' , encoding='utf8')
        csvReader = csv.reader(fr, delimiter=',')
        for row in csvReader:
            logging.info(row);
            if (len(row) < 3) or (len(row[ixu])) != 4: 
                    logging.info('row wrong length row len %s  unicode len %s',len(row),len(row[ixu]))
                    continue
            uic = row[ixu].strip()
            if uic != "":
                unicode = getUnicode(uic)
                fw.write(unicode)
        fr.close
        fw.close()
        return 0
    except Exception as e:
        logging.exception('exception %s',e)
        #traceback.print_exc()
        return(1)
     
def xconvertfiletype(filename):
    lExt = filename.split(".")[1]
    if lExt == '.csv':
        lcsvFile = filename
    elif lExt == 'ods':
        lcsvFile = convert2csv(filename, 'input')
    elif lExt == 'xlsx':
        lcsvFile = convert2csv(filename, 'input')
    else:
        logging.exception('Wrong type of File only csv, xlsx or ods files accepted')
        lcsvFile = ""
    return lcsvFile
 
def main(*ffargs):  
    lgh = log_setup('Log/'+__file__[:-3]+'.log') 
    
    logging.info('version %s', bfVersion)
    args = []
    for a in ffargs[0]:
        logging.debug(a)
        args.append(a)

    if len(args) == 3: 
        infile = convertfiletype(args[1])
        outfile = args[2]
        
    else:
        logging.warning("\nsyntax: fontforge -script back2doc.py output.txt")
        logging.warning("\nCreates a backfont text file for verification of word alignment")
        return 1

    rc = read_csv(infile, outfile)
    if rc == 0:
        #convett2odt(outfile)
        logging.info("Done!  The backdoc file is in %s", outfile)
    else:
        logging.error('Failed %d',rc)
    
    #closeLogFile(lgh)
    #sys.exit(rc)
    return(rc)

if __name__ == "__main__":
   
    logging.info(': '.join(sys.argv))
    rc = main(sys.argv) 
    sys.exit(rc)