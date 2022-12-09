
#https://stackoverflow.com/questions/30349542/command-libreoffice-headless-convert-to-pdf-test-docx-outdir-pdf-is-not	


import os
import sys
import subprocess
import inspect
import zipfile
import time
from datetime import timedelta
import logging
#from bfLog import log_setup


start_time = ""
def runTime(t = 'start'):
    global start_time
    if t == 'start':
        start_time = time.time()
        ft = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(start_time))
        print('ft',ft)
        return ft
    
    if t == 'stop':
        stop_time = time.time()
        elapsed_time = stop_time - start_time
        td =  timedelta(milliseconds=round(elapsed_time))
        
        msg = (td.seconds,td.microseconds)
        print(msg)
        #msg = "Execution took: %s secs (Wall clock time)" % timedelta(milliseconds=round(elapsed_time))

        return 'Execution time '+str(msg)
    


def lineno():
    """Returns the current line number in our program."""
    #t = time.strftime("%Y-%m-%d %H:%M:%S.%f")
    #return t
    return inspect.currentframe().f_back.f_lineno
    

def getUnicode(_str):
    try:
        a = chr(int(_str,16)).encode('utf-8')
        return a.decode('utf-8')
    except Exception as  e:
        logging.error("fatal error getUnicode %s input %s",e, _str)
        sys.exit(1)
        
def unicode2hex(uic): 
    #print(hex(ord(uic)))
    return(hex(ord(uic)))
   
def convertfiletype(filename):
    print('filename', filename)
    lExt = filename.split(".")[1]
    if lExt == 'csv':
       
        cmd = filename+' dist'
        cmd = cmd.replace('/', '\\')
        cmd = 'copy /y '+cmd
        rc = os.system(cmd)
        lcsvFile = 'dist/'+os.path.basename(filename)
        logging.info('copyfile %d %s ',rc, cmd)

    elif lExt == 'ods':
        lcsvFile = convert2csv(filename, 'dist')
        lcsvFile = 'dist/'+os.path.basename(lcsvFile)
    elif lExt == 'xlsx':
        lcsvFile = convert2csv(filename, 'dist')
        lcsvFile = 'dist/'+os.path.basename(lcsvFile)
    else:
        logging.exception('Wrong type of File only csv, xlsx or ods files accepted')
        lcsvFile = ""
    logging.info('convertfiletype %s ', lcsvFile)
    return lcsvFile
   
def convert2text(filename, outdir=""):
    # https://stackoverflow.com/questions/24704536/how-do-i-convert-doc-files-to-txt-using-libreoffice-from-the-command-line
    # https://wiki.openoffice.org/wiki/Documentation/DevGuide/Spreadsheets/Filter_Options#Filter_Options_for_the_CSV_Filter
    cmd = ["C:\Program Files\LibreOffice\program\soffice",
        "--convert-to",
        "txt:Text",
        filename]

    if outdir:
        cmd.append("--outdir")
        cmd.append(outdir)
        
    logging.info('convert2text %s',cmd)
    try:
        result = subprocess.call(cmd)
        logging.info('convert2text status %s', result)
    except Exception as e:
        logging.exception("fatal error convert2text %S %S %s", result, filename,e)
        #traceback.print_exc()
        return(1)
    txtFile = filename[:-4]+'.txt'
    return txtFile
   
   
def convert2csv(filename, outdir=""):
    # https://wiki.openoffice.org/wiki/Documentation/DevGuide/Spreadsheets/Filter_Options#Filter_Options_for_the_CSV_Filter
    #cmd = "C:\Program Files\LibreOffice\program\soffice"+  " --convert-to csv"+ " --infilter=CSV:44,34,76,1,,,true "+ filename
    cmd = ["C:\Program Files\LibreOffice\program\soffice", "--convert-to", "csv", "--infilter=CSV:44,34,76,1,,,true ", filename]
    #log_info("convert2csv",cmd)
    if outdir:
        cmd.append("--outdir")
        cmd.append(outdir)
        
    logging.info('convert2csv %s',filename)
    try:
        result = subprocess.call(cmd)
        logging.info('convert2csv status %s', result)
    except Exception as e:
        logging.exception("fatal error convert2csv %s %s %s", result, filename,e)
        #traceback.print_exc()
        return(1)
    csvFile = filename.split(".")[0]+".csv"
    return csvFile
        

def convert2ods(filename, outdir=""):	
    cmd = ["C:\Program Files\LibreOffice\program\soffice", "--headless", "--convert-to", "ods", "--infilter=CSV:44,34,76,1,,,true", filename]
    #cmd = "C:\Program Files\LibreOffice\program\soffice"+ " --headless"+ " --convert-to ods"+ " --infilter=CSV:44,34,76,1,,,true "+ filename   # + " --outdir dist"
    if outdir:
        #cmd = cmd+" --outdir "+outdir
        cmd.append("--outdir")
        cmd.append(outdir)
        
    logging.info('convert2ods %s',filename)
    try:
        result = subprocess.call(cmd)
        logging.info('convert2ods status %s', result)
    except Exception as e:
        logging.exception("fatal error convert2ods %s %s %s",result,filename,e)
        #traceback.print_exc()
        return(1)
    #odsFile = filename[:-4]+'.ods'
    odsFile = filename.split(".")[0]+".ods"
    return odsFile

# https://stackoverflow.com/questions/30349542/command-libreoffice-headless-convert-to-pdf-test-docx-outdir-pdf-is-not	
def convert2pdf(filename, outdir=""):	
    #cmd = "C:\Program Files\LibreOffice\program\soffice"+ " --headless"+  " --convert-to pdf "+filename
    cmd = ["C:\Program Files\LibreOffice\program\soffice",
            "--headless",
            "--convert-to", 
            "pdf", 
            filename]
    
    #cmd = "C:\Program Files\LibreOffice\program\soffice" + " --headless" + " --convert-to pdf:calc_pdf_Export " + filename + " --outdir dist"
    if outdir:
        cmd.append("--outdir")
        cmd.append(outdir)
        
    logging.info('convert2pdf %s',filename)
    try:
        result = subprocess.call(cmd)
        logging.info('convert2pdf status %s', result)
    except Exception as e:
        logging.exception("fatal error convert2pdf %s %s %s", result, filename,e)
        #traceback.print_exc()
        return(1)
    #pdfFile = filename[:-4]+'.pdf'
    pdfFile = filename.split(".")[0]+".pdf"
    return pdfFile

def convert2odt(filename, outdir=""):	
    #cmd = "C:\Program Files\LibreOffice\program\soffice"+ " --headless"+  " --convert-to pdf "+filename
    cmd = ["C:\Program Files\LibreOffice\program\soffice",
            "--headless",
            "--convert-to", 
            "odt", 
            filename]
    
    #cmd = "C:\Program Files\LibreOffice\program\soffice" + " --headless" + " --convert-to pdf:calc_pdf_Export " + filename + " --outdir dist"
    if outdir:
        cmd.append("--outdir")
        cmd.append(outdir)
        
    logging.info('convert2odt %s',filename)
    try:
        result = subprocess.call(cmd)
        logging.info('convert2odt status %s', result)
    except Exception as e:
        logging.exception("fatal error convert2odt %s %s %s", result, filename,e)
        #traceback.print_exc()
        return(1)
    #odtFile = filename[:-4]+'.odt'
    odtFile = filename.split(".")[0]+".odt"
    return odtFile
    
