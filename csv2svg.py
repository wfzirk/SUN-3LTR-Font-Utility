#!/usr/bin/env fontforge -lang=py
# http://www.typophile.com/node/81351
# http://fontforge.github.io/scripting.html#Example
# https://fontforge.github.io/python.html
# https://stackoverflow.com/questions/14813583/set-baseline-with-fontforge-scriping
# https://www.reddit.com/r/neography/comments/83ovk7/creating_fonts_with_inkscape_and_fontforge_part10/

import fontforge
import sys
import os
import csv
import subprocess
import time
import glob
import logging
from bfLog import log_setup
from bfConfig import readCfg, bfVersion
from util import convert2csv, convertfiletype 
 
cnt = 0
#imagemagic command  = 'convert -font Arial -pointsize 72 caption:%inp4% oxl.pnm'
def makeSVG(fontName, uniName, name, alias, debug):
    global cnt
   #log_info('  makesvg', fontName, ',',uniName, ',',name,',', alias)
    if uniName == 'e37e':
        svgFile = "e37e_period.svg"
        logging.info("using existing file %s",svgFile)
        #svgCopy(svgFile)
        return 0
    elif uniName == 'e390':
        svgFile = "e390_possesive.svg"
        logging.info("using existing file %s",svgFile)
        #svgCopy(svgFile)
        return 0
    elif uniName == 'ed11':
        svgFile = "ed11_pn.svg"
        logging.info("using existing file %s",svgFile)
        #svgCopy(svgFile)
        return 0
    else:
        if uniName == 'e316':
            name = '?'
            logging.info('generating ? as questionmark')
            
        svgFile = "Svg\\"+alias+"_"+uniName+".svg"
        pnmFile = "tmp.pnm"
        #pattern = "Svg\\*_"+uniName+"+*.svg"
        if glob.glob(svgFile):
            logging.warning('file pattern %s alreadyexists',uniName)
            return 0
        exists = os.path.isfile(svgFile)

        if not exists or debug:
            #cmd = "magick convert" + " -font "+fontName+" -pointsize 72 label:"+'"'+name+'"'+" tmp.pnm"
            cmd = "magick convert" + " -font "+fontName+" -pointsize 72 label:"+'"'+name+'"'+" "+pnmFile
            logging.info('magick convert %s',cmd)
            try:
                status = subprocess.call(cmd, shell=True)                #cmd = "potrace" +" --height 1.0 -s tmp.pnm -o "+'"'+svgFile+'"'
                cmd = "potrace" +" --height 1.0 -s "+pnmFile+" -o "+'"'+svgFile+'"'
                logging.info('   potrace %s %s ',status, cmd)
                if status == 0:
                    status = subprocess.call(cmd, shell=True)
                    #log_info('    ',status, cmd)
                if status != 0:    
                    logging.error('Error processing  %s %s',status, cmd)
                    return(status)
            except Exception as  e:
                logging.exception("fatal error makeSVG file  %s %s", svgFile,e)
                #traceback.print_exc()
                return(2)
        else:
            logging.warning('%d ***duplicate file %s',cnt,svgFile)  #, file=sys.stderr)
            #time.sleep(0.1)
            #log_warn('    ***Must delete existing files first')  #file=sys.stderr)
            #sys.stdout.flush()
            #return()
    cnt += 1
    return(0)

def read_list(fontname, csvFile, namelist=""):
    #cfg = json.load(open('config.json'))
    cfg = readCfg()
    alias = cfg["alias"]
    debug = (cfg["debug"] == "True")    
    print('debug',debug)
    if alias == "ENG":
        ixu = cfg["enColumns"]["index_unicode"]
        ixn = cfg["enColumns"]["index_name"]
    else:
        ixu = cfg["langColumns"]["index_unicode"]
        ixn = cfg["langColumns"]["index_langName"]
    status = 0
    try:
        logging.info('readlist %s %s %s',fontname, csvFile, namelist)
        logging.info('dict columns ixu %s  ixn  %s',ixu,ixn)
        with open(csvFile, encoding='utf8') as csvDataFile:
            csvReader = csv.reader(csvDataFile, delimiter=',', quotechar ='"')
            for row in csvReader:
                #logging.info('%s,%d %d',alias,ixn, ixu)
                logging.info(row)
                logging.debug('%s %s',row[ixn],row[ixu])
                ncol = len(row)
                name = row[ixn].strip()
                unicode = row[ixu].strip().lower()
                if len(name) == 0:
                    continue
                if namelist:
                    if unicode not in namelist:
                        #log_info(ixu,namelist, row[ixu],'not in namelist')
                        continue
                #log_info(name, unicode, ncol)
                if (len(row) < 3) or (len(row[ixu])) != 4: 
                    logging.info('row wrong length row len %s  unicode len %s',len(row),len(row[ixu]))
                    continue

                if len(unicode) < 4:
                    status = makeSVG(fontname, name, name, alias, debug)
                else:
                    status = makeSVG(fontname, unicode, name, alias, debug)
                #time.sleep(0)   # allow interrupts
                if status != 0:
                    return status
                #time.sleep(0.005)
    except Exception as e:
        logging.exception("fatal error read_list %s",e)   # file=sys.stderr)
        #traceback.print_exc()
        return(3)
        
    return status
     
def xconvertfiletype(filename):
    lExt = filename.split(".")[1]
    if lExt == 'csv':
        lcsvFile = filename
    elif lExt == 'ods':
        lcsvFile = convert2csv(filename, 'input')
    elif lExt == 'xlsx':
        lcsvFile = convert2csv(filename, 'input')
    else:
        logging.exception('Wrong type of File only csv, xlsx or ods files accepted  %s',filename)
        lcsvFile = ""
    return lcsvFile

def main(*ffargs):   
    lgh = log_setup('Log/'+__file__[:-3]+'.log') 
    logging.info('version %s', bfVersion)
    args = []
    rc = 0
    for a in ffargs[0]:
        logging.info('%s',a)
        args.append(a)
        

    if len(args) > 2: 
        csvFile = convertfiletype(args[1])
        ttfFont = args[2].lower()
        namelist = ""
        if len(args) > 3:
            index = 0
            for arg in args:
                #log_info(index, arg)
                if index > 2:
                    namelist = namelist+'+'+arg.strip()
                index += 1
                
            if len(namelist) < 4:
                namelist = ""
                
        print('csvfile',csvFile)
        status = read_list(ttfFont, csvFile, namelist.lower())
        logging.info('read_list status %s',status)
        rc = status
    else:
        logging.warning("\nSYNTAX Error")
        logging.warning("\nsyntax: fontforge -script bfv2svg.py csvfile ttffile [unicode list]\n")
        logging.warning("   - script Python script file,  csvfile language fontfile\n")
        logging.warning("   optional space separated unicode list i.e. e000 eda5\n")
        logging.warning("\nCreates svg files in the /svg directory using\n")
        logging.warning("the names in the csv file\n")
        logging.warning("The csv file format \n")
        logging.warning("      glyph, unicode(hex), name\n")
        logging.warning("Optionally limits build to list of unicodes\n")
        rc = 1

    if rc == 0:
        logging.info('Done SVG files are in Svg directory')
    else:
        logging.error('Failed %d',rc)
    
    #closeLogFile(lgh)
    #sys.exit(rc)
    return(rc)

if __name__ == "__main__":
   
    logging.debug('name main %s',sys.argv)
    rc = main(sys.argv) 
    sys.exit(rc)