# routine to change glyph names in font
#  
'''
takes data from fontforge file to generate a list of unicodes and names
i.e.  Athens,eb08

invoke with:
fontforge -script glyphunicode.py  "Sunxxfont.sfd"	"csvfile name"

'''

import fontforge
import os
import sys
import csv

from tkinter import *
import time

from bfConfig import readCfg, bfVersion, saveCfg
from array2xlsx import array2xlsx
import logging
from bfLog import log_setup

cfg = readCfg()
    
def getUnicode(str):
    try:
        a = chr(int(str,16)).encode('utf-8')
        return a.decode('utf-8')
    except Exception as  e:
        logging.error("fatal error getUnicode %s",e)
        return 1

def readKmnCSV(filename):
    refList = {}
    ixr = cfg["enColumns"]["index_ref"]
    ixn = cfg["enColumns"]["index_name"]
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for r in readCSV:
            ref = r[ixr].strip()
            if ref:
                refList[r[ixn]] = r[ixr]
    return refList


def listGlyphs(font, refList):
    #cfg = readCfg()
    DEBUG = cfg["debug"] == "true"
    IMAGEPOS = cfg["enColumns"]["index_font"]
    #LANGNAMEPOS = cfg["langColumns"]["index_langName"]
    UECPOS = cfg["enColumns"]["index_unicode"]
    ENNAMEPOS = cfg["enColumns"]["index_name"]
    refPos = cfg["enColumns"]["index_ref"]
    print(refPos)
    cnt = 0
    glyphs = []
    for glyph in font:
        gl = [None, None, None, None]
        try:
            if font[glyph].unicode > 57343:
                #if font[glyph].unicode < 57344:    # incase bad characters
                #    continue
            
                unicode = hex(font[glyph].unicode)[2:]
                logging.info("|%s| %s %s",font[glyph].unicode, font[glyph].glyphname, unicode)
                
                if len(unicode) < 4:
                    continue;
                uic = getUnicode(unicode)
                name = font[glyph].glyphname.split('.')[0]
                #print(uic.encode().hex()+' '+unicode+' '+ name)
                #log_info(uic.encode().hex(),unicode, name)
                logging.info('lg:%s %s %s',uic.encode().hex(),unicode, name)
                gl[IMAGEPOS] = uic
                gl[ENNAMEPOS] = name
                gl[UECPOS] = unicode
                if name in refList:
                    gl[refPos] = refList[name]
                else:
                    gl[refPos] = ""
                glyphs.append(gl)
                 
        except Exception as e:
            logging.exception("fatal error listGlyph %s",e)
            #traceback.print_exc()
            return 1,""
            
        if DEBUG:
            cnt = cnt+1
            if cnt>10:
                break
        #time.sleep(0.001)
                
    #sort by name        
    name_sort = sorted(glyphs, key=lambda x: x[ENNAMEPOS].lower())
    return 0, name_sort

def writeGlyphs(glyphs, outfile):
    logging.info('wrtglphs %s',outfile)
    fw = open(outfile, 'w' ,encoding='utf8', newline='')
    csvWriter = csv.writer(fw)
    count = 0
    for g in glyphs:
        try:
            csvWriter.writerow(g)
        except Exception as e:
            logging.exception("fatal error writeGlyphs %s",e)
            #traceback.print_exc()
            return 2
        #time.sleep(0.001)
    fw.close()   
    return 0

def main(*ffargs):
    lgh = log_setup('Log/'+__file__[:-3]+'.log') 
    logging.info('version %s', bfVersion)
    args = [] 
    for a in ffargs[0]:
        logging.debug('input ffargs %s',a)
        args.append(a)

    rc = 0
    if len(args) > 2: 
        fontName  = args[1]
        kmfile = args[2]
        outfile = args[3]
        try:
            refList = readKmnCSV(kmfile)
            font = fontforge.open (fontName)
            cfg["sunFontName"] = font.fontname
            saveCfg(cfg)        #make font name
            rc,glyphs = listGlyphs(font, refList)
            if rc == 0:
                rc = writeGlyphs(glyphs, outfile)
            if rc == 0:
                array2xlsx(glyphs, outfile[:-4]+'.ods')

        except Exception as e:
            #log_err("fatal error ",e)
            #traceback.print_exc()
            #logging.exception("Deliberate divide by zero traceback")
            logging.exception(e)
            rc = 1
    else:
        logging.warning("\n  SYNTAX: fontforge -script sfd2csv.py fontforgefile.sfd keyman_csvfile csvfile.csv")
        logging.warning("  i.e. fontforge -script sfd2csv.py fontfile.sfd keyman.csv pwlist.csv")
        logging.warning("  Takes data from fontforge file to generate a csv file of symbols and names,")
        logging.warning("  unicodes and names")
        logging.warning("  i.e. symbol,eb08,Athens, reference")
        rc = 1
        
    if rc != 0:
        logging.error("failed status = %s",rc)
    else:
        logging.info("Done!  The csv file is in %s", outfile)
    
    #closeLogFile(lgh)
    #sys.exit(rc)
    return rc
    
if __name__ == "__main__":

    logging.info(': '.join(sys.argv))
    rc = main(sys.argv) 
    sys.exit(rc)