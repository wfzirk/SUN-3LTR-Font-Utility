"""
 https://xlsxwriter.readthedocs.io
 https://ask.libreoffice.org/en/question/75384/is-it-possible-to-format-a-libreoffice-spreadsheet-using-a-shell-script/
 Creates a condensed view of the dictionary  with the unicode and name in same column
rem open command prom[t as admin
rem cd to fontforgebuilds dir
rem execute fontforge-console
rem execute ffpython -m pip install --upgrade pip --force-reinstall
rem execute pip install xlsxwriter

   fontforge -script imageref.py infile outfile')
     Example: fontforge -script genesis.csv genout.csv\n')

This program automatically resizes the spreadsheet formats to make 
into a pdf 

"""

import sys
import os
import csv
import xlsxwriter
import logging
from bfLog import log_setup
from util import  convert2ods, convert2pdf, convert2csv, convertfiletype 
from bfConfig import readCfg, bfVersion
import loadFont
import time

cfg = readCfg()
if cfg["alias"] == "ENG":
    IMAGEPOS = cfg["enColumns"]["index_font"]
    NAMEPOS = cfg["enColumns"]["index_name"]
    UECPOS = cfg["enColumns"]["index_unicode"]
else:
    IMAGEPOS = cfg["langColumns"]["index_font"]
    NAMEPOS = cfg["langColumns"]["index_langName"]
    UECPOS = cfg["langColumns"]["index_unicode"]

debug = False

#symbol unicode name
def read_csv_data(path):
    try:
        f = open(path, 'r', encoding="utf-8")
        csvReader = csv.reader(f, delimiter=',', quotechar='"')
        # Assume no column headers
        data_lines = []
        #make sure data us sorted by name
        name_sort = sorted(csvReader, key=lambda x: x[NAMEPOS].lower())
        count = 0
        for row in name_sort:
            #log_info(row, type(row[2]), type(row[1]))
            if debug:
                count += 1
                row[2]=str(count)+' '+row[2]
                if count > 70:
                    break
            if not row[NAMEPOS]:     # if language dict with missing words
                continue
            data_lines.append(row)
            logging.debug(row)
        return 0, data_lines		
    except Exception as e:
        logging.exception('exception %s',e)
        #traceback.print_exc()
        return 1, ""

def createCell(row):
    name = row[NAMEPOS]
    uec = row[UECPOS]
    image = row[IMAGEPOS]
    line = name+'\n('+uec+')'    #,'+syn;
    return line
    

def csv2_4x16(csvArray):
    COLUMNS = 4
    ROWSPERPAGE = 16
    NOPERPAGE = COLUMNS*ROWSPERPAGE

    dlen = len(csvArray)
    rows = []
    cnt = 0
    logging.info('Creating 4 col list length %d',dlen)
    for x in range(0, len(csvArray), 64):
        logging.debug('%s -----',x)
        #line = []
        m = min(x+16, len(csvArray))
        logging.info('processing range %d - %d',x,m)
        for y in range(x, m):
            line=[]
            if y < dlen:
                line.append(csvArray[y][0])
                line.append(createCell(csvArray[y]))
            if y+16 < dlen:
                line.append(csvArray[y+16][0])
                line.append(createCell(csvArray[y+16]))
            if y+32 < dlen:
                line.append(csvArray[y+32][0])
                line.append(createCell(csvArray[y+32]))
            if y+48 < dlen:
                line.append(csvArray[y+48][0])
                line.append(createCell(csvArray[y+48]))
            logging.debug(' %d: %d %s',x,y,line)
            rows.append(line)

    logging.debug('rows %d', len(rows))
    return rows

def arry2xlsx(ary, outFile):
    # https://xlsxwriter.readthedocs.io
    #fout = outFile.split('.')[0]
    fout = outFile[:-4]
    fxlsx = fout+'.xlsx'
    print(cfg["sunFontName"])
    lf = loadFont.loadFontThrd(cfg["sunFontName"]+".ttf")
    lf.run()
    time.sleep(1)
    logging.info('started lf')
    workbook = xlsxwriter.Workbook(fxlsx)
    worksheet = workbook.add_worksheet()
    logging.info('arry2xlsx %s', fxlsx)

    col = 0
    #populate the table
    for row, data in enumerate(ary):
        #log_info('\nws',row,col,data)
        worksheet.write_row(row,col, data)

    
    s_fmt = workbook.add_format()
    s_fmt.set_font_name(cfg["sunFontName"])
    s_fmt.set_font_size(32)
    #s_fmt.set_font_size(12)
    s_fmt.set_align('center')
    s_fmt.set_align('vcenter')
    s_col_width = 7.9
    
    
    d_fmt = workbook.add_format()
    d_fmt.set_font_size(12)
    d_fmt.set_text_wrap()
    d_fmt.set_align('left')
    d_fmt.set_align('vcenter')
    d_col_width = 14.1
    
    worksheet.set_column('A:A', s_col_width, s_fmt)
    worksheet.set_column('C:C', s_col_width, s_fmt)
    worksheet.set_column('E:E', s_col_width, s_fmt)
    worksheet.set_column('G:G', s_col_width, s_fmt)
    
    worksheet.set_column('B:B', d_col_width, d_fmt)
    worksheet.set_column('D:D', d_col_width, d_fmt)
    worksheet.set_column('F:F', d_col_width, d_fmt)
    worksheet.set_column('H:H', d_col_width, d_fmt)

    # create page breaks so data lines up with sort
    pg_brk = []
    for i in range(0, len(ary), 16):
        pg_brk.append(i)
    
    worksheet.set_h_pagebreaks(pg_brk)
    worksheet.set_margins(0.5,0.5)
    worksheet.center_vertically()
    worksheet.center_horizontally()
    
    workbook.close()
    # create pdf
    # Libreoffice needs ods file to generate pdf 
    # does not work properly xlsx->pdf
    convert2ods(fxlsx, 'dist')
    fods = fout+'.ods'
    convert2pdf(fods,'dist')
    exists = os.path.isfile(fxlsx)
    if exists:
        logging.info('delete existing file %s',fxlsx)
        os.remove(fxlsx)
    exists = os.path.isfile(fods)
    #if exists:
    #    log_info('delete existing file',fods)
    #    os.remove(fods)
    lf.stop()
    del lf
  
def xconvertfiletype(filename):
    lExt = filename.split(".")[1]
    if lExt == 'csv':
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
    rc = 0
    for a in ffargs[0]:
        logging.debug( a)
        args.append(a)

    if len(args) ==3: 
        csv_file = convertfiletype(args[1])
        outFile = args[2]
        rc, csv_data = read_csv_data(csv_file)
        logging.debug('read_csv %d %d',rc, len(csv_data))

        if rc == 0:
            #name_sort = sorted(csv_data, key=lambda x: x[LANGNAMEPOS].lower())

            ary = csv2_4x16(csv_data)
            logging.debug('csv24x16 %d', len(ary))
            arry2xlsx(ary, outFile)
            rc = 0
    
    else:
        logging.warning('\n>>  fontforge -script imageref.py infile outfile')
        logging.warning('>>  Example: fontforge -script genesis.csv genout.csv\n')
        logging.warning('Creates a condensed view of the dictionary  with the unicode')
        logging.warning('and name in same cell.');
        rc = 1
  
    if rc == 0:
        logging.info('** done ** files are in %s',outFile)

    else:
        logging.error("Error could not complete commands status = %d",rc)
    

    #closeLogFile(lgh)
    return(rc)


if __name__ == "__main__":
   
    logging.info(': '.join(sys.argv))
    rc = main(sys.argv) 
    sys.exit(rc)    