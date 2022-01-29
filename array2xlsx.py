''' create xlsx spreadsheet then convert to ODS
    https://xlsxwriter.readthedocs.io
    https://cxn03651.github.io/write_xlsx/format.html

'''
import os
import xlsxwriter
from util import convert2ods, convert2pdf, convert2csv
import logging
#from bfLog import log_setup
from bfConfig import readCfg
import loadFont

# lang2xlsx formats and writes a spreadsheet for xlsx and ods files
def array2xlsx(aryx, outFile, pdf=False, csv=False):
    # https://xlsxwriter.readthedocs.io
    cfg = readCfg()
    logging.info('array2xlsx outfile  %s', outFile)
    lf = loadFont.loadFontThrd(cfg["sunFontName"]+".ttf")
    lf.run()
    
    if isinstance(aryx,dict):
        ary = list(aryx.values())
    elif isinstance(aryx, list):
        ary = aryx
    else:
        logging.error("wrong data type")
        return 1    
    fxlsx = outFile[:-4]+'.xlsx'
    workbook = xlsxwriter.Workbook(fxlsx)
    worksheet = workbook.add_worksheet()

    col = 0
    row = 0
    for i in ary:
        worksheet.write_row(row,col, i)
        row += 1
        
    # format for symbol column
    s_fmt = workbook.add_format()
    s_fmt.set_font_name(cfg["sunFontName"])
    s_fmt.set_font_size(32)
    s_fmt.set_align('center')
    s_fmt.set_align('vcenter')
    s_col_width = 7.9
    
    # format for other columns
    d_fmt = workbook.add_format()
    d_fmt.set_font_size(12)
    d_fmt.set_text_wrap()
    d_fmt.set_align('left')
    d_fmt.set_align('vcenter')
    l_col_width = 25    # language column width
    n_col_width = 18    # english name column width
    u_col_width = 6     #unicode column width
    r_col_width = 18    #reference column width
    
    worksheet.set_column('A:A', s_col_width, s_fmt)     # symbol column
    worksheet.set_column('B:B', n_col_width, d_fmt)     # EN name column
    if cfg["alias"] == "ENG":
        worksheet.set_column('C:C', u_col_width, d_fmt)
        worksheet.set_column('D:D', r_col_width, d_fmt)
    else:
        worksheet.set_column('C:C', l_col_width, d_fmt)
        worksheet.set_column('D:D', u_col_width, d_fmt)
        worksheet.set_column('E:E', r_col_width, d_fmt)
    '''    
    #logging.debug('ary length', len(ary))
    # ,Abilene,Ec4d,Luke 3:1    for kmn2csv
    #determine if 3 or 4 column array
    if len(ary[2]) < 54:
       worksheet.set_column('B:B', d_col_width, d_fmt) 
       worksheet.set_column('C:C', u_col_width, d_fmt)

    else:
        worksheet.set_column('B:C', d_col_width, d_fmt)
        worksheet.set_column('D:D', u_col_width, d_fmt)
    '''
    worksheet.center_vertically()
    worksheet.center_horizontally()
    
    workbook.close()
    convert2ods(fxlsx, 'dist')
    fods = outFile[:-4]+'.ods'
    logging.info('ODS file created %s',fods)
    exists = os.path.isfile(fxlsx)
    if exists:
        logging.info('delete existing xlsx file %s',fxlsx)
        os.remove(fxlsx)
    if csv:
        convert2csv(fods, 'dist')
    if pdf:    
        # Libreoffice needs ods file to generate pdf correctly
        convert2pdf(fods)
        
    lf.stop()
    del lf
