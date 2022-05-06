'''
create SUN kmn file from SUN csv dictionary.
    
store(&VERSION) '9.0' U+0079
store(&TARGETS) 'any windows macosx linux web iphone ipad androidphone androidtablet mobile desktop tablet'
store(&KEYBOARDVERSION) '090026'
store(&LAYOUTFILE) 'Sun2-layout.js'
store(&NAME) 'sun7_6'
begin Unicode > use(main)

group(main) using keys

'Aaron' + ' ' > U+Eb0d
'Abel' + ' ' > U+EA96
'Abiathar' + ' ' > U+E35F
'abide' + ' ' > U+E17B
....    

'''
import fontforge
import os
import sys
import csv
from bfConfig import readCfg, bfVersion
import logging
from bfLog import log_setup
from util import convert2csv, convertfiletype 

def get_header(name):
    logging.info('get_header %s', name)
    hdr = "store(&VERSION) '9.0' U+0079\n"
    hdr = hdr + "store(&TARGETS) 'any windows macosx linux web iphone ipad androidphone androidtablet mobile desktop tablet'\n"
    hdr = hdr + "store(&KEYBOARDVERSION) '090023'\n"
    hdr = hdr + "store(&LAYOUTFILE) 'Sun2-layout.js'\n"
    hdr = hdr + "store(&NAME) '"+name+"'\n"
    hdr = hdr + "begin Unicode > use(main)\n"
    hdr = hdr + "\ngroup(main) using keys"
    hdr = hdr + "\n\n"
    logging.info(hdr)
    return hdr
    
def build_row(name, unicode, ref):  
    #   'Aaron' + ' ' > U+Eb0d
    comment = ""
    if ref:
        comment = "   c "+ref
    pad = " ".ljust(25-len(name))
    #row = "'"+sname+"' + ' ' > U+"+unicode.lower()+comment
    row = '"'+name+'"'+pad+' + " " > U+'+unicode.lower()+comment
    logging.debug(row)
    return row
    
def read_csv(f):
    #name_has_spaces = 'Log/name_has_spaces.txt'
    #name_is_missing = 'Log/name_is_missing.txt'
    rcfg = readCfg()
    cfg = rcfg["langColumns"]
    name_has_spaces = 'dist/name_has_spaces_'+rcfg["alias"]+'.txt'
    name_is_missing = 'dist/name_is_missing_'+rcfg["alias"]+'.txt'
    
    ixu = cfg["index_unicode"]
    ixn = cfg["index_langName"]
    ixe = cfg["index_name"]
    ixr = 4
    logging.info('read_csv %s %s',f, cfg["index_langName"])
    logging.info('name is  %s  %s',name_is_missing, name_has_spaces)
    csvData = []
    nameError = False
    try:
        with open(f, encoding='utf8', newline='') as csvfile, open(name_has_spaces, "w") as file_spc, open(name_is_missing, "w") as file_missing:
            data = list(csv.reader(csvfile))
            #logging.debug('data %d %d',len(data), len(data[1]))
            #logging.debug(cfg)
            cnt = 0
            for i in data:
                logging.info('%d |%s| %s %s %s', cnt, i[ixu],i[ixn], i[ixe], i[ixr])
                unicode = i[ixu].lower().strip()
                
                if len(unicode) != 4:
                    continue
                if unicode[:1] != 'e':
                    continue
                name = i[ixn].strip()           #.replace("'","''")
                if len(name) == 0:
                    errStr = f"---Name Error---, name is missing ({unicode})"
                    #logging.error("---Name Error---, name contains spaces, %s (%s)", name, unicode)
                    logging.error(errStr)
                    file_missing.write(errStr+'\n')
                    continue
                ref = i[ixr].strip()
                
                if len(ref) == 0:
                    ref = ""
                if ' ' in name:
                    #nameError = True
                    errStr = f"---Name Error---, name contains spaces, {name}, ({unicode})"
                    #logging.error("---Name Error---, name contains spaces, %s (%s)", name, unicode)
                    logging.error(errStr)
                    file_spc.write(errStr+'\n')
                    name = name.replace(" ","_")
                    
                csvData.append(build_row(name, unicode, ref)) 
                cnt += 1
      
    except Exception as  e:
        logging.exception("fatal error read_csv %s",e)
        #traceback.print_exc()
        return []  
        
    if nameError:
        logging.error("One or more words contain spaces view %s file",name_has_spaces)
        return []         
    name_sort = sorted(csvData, key=lambda x: x[ixn].lower())
    return name_sort


# parse kmn file and generate csv file for documentation
def write_kmn(hdr, data, altData, outfile):
    logging.info('write_kmn %s', outfile)
    try:
        #fw = open(outfile, 'w')
        with open(outfile, 'w') as fw:
            fw.write(hdr)
            for i  in data:
                wstr = i+'\n'
                fw.write(wstr)
            fw.write('c ======= alternate words =================\n')   
            if altData:
                for i  in altData:
                    wstr = i+'\n'
                    fw.write(wstr)
        
    except Exception as  e:
        logging.exception("fatal error write_kmn %s",e)
        fw.close()
        return(1)
    
    fw.close()
    return(0)

def xconvertfiletype(filename):
    print( filename)
    lExt = filename.split(".")[1]
    if lExt == 'csv':
        lcsvFile = filename
    elif lExt == 'ods':
        lcsvFile = convert2csv(filename, 'dist')
    elif lExt == 'xlsx':
        lcsvFile = convert2csv(filename, 'dist')
    else:
        logging.exception('Wrong type of File only csv, xlsx or ods files accepted')
        lcsvFile = ""
    return lcsvFile
    
def main(*ffargs):
    lgh = log_setup('Log/'+__file__[:-3]+'.log') 
    logging.info('version %s', bfVersion)
    rc = 0 
    
    args = []
    for a in ffargs[0]:
        logging.debug(a)
        args.append(a)
        
    logging.info(args)

    if len(args) > 2: 
        langDict = convertfiletype(args[1])
        print('langdict',langDict)
        if len(args) == 3:
            outFile = args[2]
            altDict = ""
        else:
            altDict = convertfiletype(args[2])
            outFile = args[3]
        
        csvData = read_csv(langDict)
        if csvData:
            altData = ""
            if altDict:
                altData = read_csv(altDict)
                if altData:    
                    name = outFile.split('.')[0]
                    hdr = get_header(name)
                    rc = write_kmn(hdr, csvData, altData, outFile)
                else:
                    rc = 1
        else:
            rc = 1

    else:
        logging.error("Create SUN kmn file from SUN csv dictionary.")
        logging.error(" i.e   fontforge -script csv2kmn.py infile.csv altfile.csv version alias outfile.kmn")
        rc = 1
        
    if rc == 0:
        logging.info('Done saved kmn file in %s \n', outFile)
    else:
        logging.error('finished with Errors status %d \n',rc)
    
    #closeLogFile(lgh)
    #sys.exit(rc)
    return(rc)
    
if __name__ == "__main__":
   
    logging.info(': '.join(sys.argv))
    rc = main(sys.argv) 
    sys.exit(rc)