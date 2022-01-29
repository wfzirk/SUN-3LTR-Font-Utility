import sys
from zipfile import ZipFile 
import os 
import csv
from bfConfig import readCfg, bfVersion
from util import convert2text, convert2odt
import logging
from bfLog import log_setup


def createFileList(cfg):
    logging.info('createFileList')
    fileList = []
    alias = cfg["alias"]
    returncode = 0

    
    if alias == "ENG":
    
        sfdfile = cfg['sfdFile'].strip()
        fileList.append([sfdfile,"SFD file for generating dictionaries"])
        kmnfile = cfg['kmnFile'].strip()
        fileList.append([kmnfile,"KMN file for generating dictionaries"])
        cpstr = sfdfile+'  '+os.getcwd()
        cpstr = cpstr.replace('/', '\\')
        logging.info('copy /y '+cpstr)
        os.system('copy /y '+cpstr)
        cpstr = kmnfile+'  '+os.getcwd()
        cpstr = cpstr.replace('/', '\\')
        os.system('copy /y '+cpstr)
        
        pwf = cfg["pwFile"][:-4]+'.ods'
        fileList.append([pwf,"Primary words dictionary created from "+os.path.basename(cfg["sfdFile"])])
        pwf = cfg["pwFile"][:-4]+'.csv'
        fileList.append([pwf,"Primary words dictionary created from "+os.path.basename(cfg["sfdFile"])]) 
        kmn = cfg["kmncsv"][:-4]+'.ods'
        fileList.append([kmn,"Complete dictionary created from "+os.path.basename(cfg["kmnFile"])])
        kmn = cfg["kmncsv"][:-4]+'.csv'
        fileList.append([kmn,"Complete dictionary created from "+os.path.basename(cfg["kmnFile"])])
        alt = cfg["altcsv"][:-4]+'.csv'
        fileList.append([alt,"Alternate word list created from "+os.path.basename(pwf)+" and "+os.path.basename(kmn)])
        
    else:
        pwlf = cfg["pwLangFile"][:-4]+'.ods'
        fileList.append([pwlf, "primary words dictionary for given language"])
        pwlf = cfg["pwLangFile"][:-4]+'.csv'
        fileList.append([pwlf, "primary words dictionary for given language"])
        #fileList.append(["", "generated from the "+cfg["trlangFile"]])
        fileList.append([cfg["csv2kmnFile"], "kmn file generated from merging "+cfg["pwFile"]+ "and "+cfg["pwLangFile"]])
        
    fileList.append([cfg["backFont"]+".sfd", "Fontforge file created from "+cfg["pwFile"]])
    fileList.append([cfg["backFont"]+".ttf", "ttf file created from "+cfg["backFont"]+".sfd"])
    fileList.append([cfg["backFont"]+".woff", "woff file created from "+cfg["backFont"]+".sfd"])
    fileList.append([cfg["compactFile"], "Primary Dictionary in compact form for printing with less paper"])
    #fileList.append([cfg["synxref"], "Cross reference including synonyms and image contents"])
    fileList.append([cfg["back2doc"], "All the words printed from the backfont for verification"])
    fileList.append([cfg["readMe"], "This File"])
    
    # remove directory from filename
    for file in fileList:
        f = os.path.basename(file[0])
        file[0] = f 
        logging.info('f %s',f)
    return fileList
    

def createReadMe(cfg, fileList):
    f = os.path.basename(cfg["readMe"])[:-4]+".csv"
    logging.info('createReadMe %s', f)
    try:
        fw = open(f, 'w' ,encoding='utf8')
        csvWriter = csv.writer(fw, delimiter=',', lineterminator='\n')
        for row in fileList:
            csvWriter.writerow(row)
        
        fw.close()
        #convert2odt(f)
    except Exception as e:
        #logging.error('Exception %s',e)
        logging.exception('CreateReadme exception %s',e)

        return(1)
        
    return(0)


def writeZip(cfg,fileList):
    zf = os.path.basename(cfg["zipFile"])
    #zf = cfg["zipFile"]
    logging.info('version %s', bfVersion)
    try:
        with ZipFile(zf,'w') as zip: 
            # writing each file one by one 
            for file in fileList: 
                logging.info("Adding file %s to zip",file[0])
                zip.write(file[0],file[0])
            zip.close()
    except Exception as e:
        #logging.error('Exception %s',e)
        logging.exception('exception %s',e)
        print(e)
        return(1)           

    logging.info('All files zipped successfully!')
    return 0

def main(*ffargs):
    #print('file',__file__)
    #base=os.path.basename(__file__)
    lgh = log_setup('Log/'+__file__[:-3]+'.log') 
    logging.info('version %s', bfVersion)

    rc = 0
    curdir = os.getcwd()
    try:
        cfg = readCfg()
        #removeFiles = cfg["debug"]
        
        # change to dist directory to so zip file won't have sub directory

        os.chdir('dist')
        fileList = createFileList(cfg)
        #logging.info('createlist %s', rc)
        if fileList:
            rc = createReadMe(cfg,fileList)
            
            if rc == 0:
                rc = writeZip(cfg, fileList)
            '''    
            if rc == 0:
                if removeFiles:
                    # delete original files
                    for file in fileList:
                        os.remove(file[0])
            '''
    except Exception as e:
        logging.exception('exception %s',e)
        rc = 1
        
    os.chdir(curdir)    # CHANGE back to runninc dir for future commands  
    if rc == 0:
        logging.info("Done!  The zipfile file is in %s", cfg["zipFile"])
    else:
        logging.error("Error could not complete commands status = %d",rc)
    #closeLogFile(lgh)
    #sys.exit(rc)
    return rc


if __name__ == "__main__": 
    #logging.info('main %s',sys.argv)
    logging.info(': '.join(sys.argv))
    rc = main() 
    sys.exit(rc)
   