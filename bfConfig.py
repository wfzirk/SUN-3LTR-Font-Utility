
import os
import sys

import json
import version

bfVersion = version.get_version()

cfg = { 
    "bfVersion":"",
    "iso639":"iso-639-3.tab",
    "iso639sub":"iso639SubList.tab",               
    "filePath": "dist/",
    "version": "",
    "alias": "",
    "language": "",
    "sfdFile": "",
    "kmnFile": "", 
    "trlangFile": "",
    "ttf": "",
    "pwFile": "",
    "pwLangFile": "",
    "backFont": "",
    "kmncsv": "",
    "altcsv": "",
    "back2doc": "",
    "csv2kmnFile": "",
    "compactFile": "",
    "zipFile": "",
    "langAltFile": "",
    "langAltCsv": "",
    "synxref":"",
    "readMe":"",
    "sunFontName": "",
    "enColumns": {"index_font": 0, "index_name": 1, "index_unicode": 2, "index_ref":3},
    "langColumns": {"index_font": 0, "index_name": 1, "index_langName": 2,
                    "index_unicode": 3, "index_ref":4},
    "eFilter": "",
    "debug": "false",
    "language_codes": "ISO639-2_LanguageCodes.csv"  #https://www.loc.gov/standards/iso639-2/php/code_list.php
    }
'''
langParms = {\
    "Russian":"RU",\
    "Spanish":"ES",\
    "French":"FR",\
    "Portuguese":"PT",\
    "English":"eng"}
'''

def updateCfg(cfg):
    #print('updatecfg',cfg["alias"], cfg["version"])
    cfg["pwFile"] = cfg["filePath"]+"pw"+cfg["version"]+"_ENG.csv"                      # this file must be the english base file
    
    basename = os.path.basename(cfg["trlangFile"])
    trlbase = basename.split('.')[0]+'.csv'
    if cfg["langAltFile"]:
        basename = os.path.basename(cfg["langAltFile"])
        altbase = basename.split('.')[0]+'.csv'
        cfg["langAltCsv"] = cfg["filePath"]+altbase
    else:
        cfg["langAltCsv"] = ""
    cfg["pwLangFile"] = cfg["filePath"]+trlbase
    cfg["backFont"] = cfg["filePath"]+"SUNBF"+cfg["version"]+"_"+cfg["alias"]      
    cfg["kmncsv"] = cfg["filePath"]+"kmn"+cfg["version"]+"_ENG.csv"                 # this file must be the english base file
    cfg["altcsv"] = cfg["filePath"]+"alt"+cfg["version"]+"_ENG.csv"                 # this file must be the english base file
    cfg["back2doc"] = cfg["filePath"]+"back"+cfg["version"]+"_"+cfg["alias"]+".txt"
    cfg["compactFile"] = cfg["filePath"]+"compact"+cfg["version"]+"_"+cfg["alias"]+".ods"
    cfg["csv2kmnFile"] = cfg["filePath"]+"sun"+cfg["version"]+"_"+cfg["alias"]+".kmn"
    cfg["zipFile"] = cfg["filePath"]+"SUN"+cfg["version"]+"_"+cfg["alias"]+".zip"
    cfg["readMe"]  = cfg["filePath"]+"readMe.csv"
    cfg["debug"] = "False"
    if "debug" in cfg["eFilter"].lower():
        cfg["debug"] = "True"
    if cfg["eFilter"]:
        cfg["debug"] = "True"
    saveCfg(cfg)   

def bfCmds(cfg, script):
    cmd = {\
        "sfd2csv": ['eng',['sfd2csv.py', cfg["sfdFile"], cfg["pwFile"]]],   
        "langpri": ['lang',['langpri.py', cfg["pwFile"], cfg["trlangFile"], cfg["pwLangFile"]]], 
        "kmn2csv": ['eng',['kmn2csv.py', cfg["kmnFile"], cfg["kmncsv"]]],
        "csv2kmn": ['lang',['csv2kmn.py', cfg["pwLangFile"], cfg["version"], cfg["alias"], cfg["csv2kmnFile"]]],
        "csv2svg": ['both',['csv2svg.py', cfg["pwLangFile"], cfg["ttf"], cfg["eFilter"]]],
        "svg2font": ['both',['svg2Font.py', cfg["pwLangFile"], cfg["ttf"], cfg["alias"],\
             cfg["backFont"], cfg["eFilter"]]],
        "back2doc": ['both',['back2doc.py', cfg["pwLangFile"], cfg["back2doc"]]],
        "compact": ['both',['compact4x16.py', cfg["pwLangFile"], cfg["compactFile"]]],
        "bfzip": ['both',['bfZip.py'] ] 
    }
    return cmd[script]

    
def saveCfg(cfg, force=False):    
    prevcfg = readCfg()
    if prevcfg != cfg or force:
        json.dump(cfg, open('config.json', 'w'),  indent=4)
        writeBat(cfg)
        print('cfg saved')

    
def readCfg():  
    #global cfg
    dumpit = False
    cfgFile = os.path.isfile('config.json')
    if cfgFile:
        rdcfg = json.load(open('config.json'))
        
        if bfVersion != rdcfg["bfVersion"]:
            dumpit = True
        for k in cfg:

            if k not in rdcfg:
                print(k,'not in rdcfg')
                dumpit = True
                break
    else:
        dumpit = True
        
    if dumpit:
        cfg["bfVersion"]=bfVersion
        json.dump(cfg, open('config.json', 'w'),  indent=4)     
        rdcfg = cfg

    return rdcfg

def writeBat(cfg):
    batEnv = "@echo off\n"\
        +"set sfd="+cfg["sfdFile"]+"\n"\
        +"set kmn="+cfg["kmnFile"]+"\n"\
        +"set ver="+cfg["version"]+"\n"\
        +"set ttffont="+cfg["ttf"]+"\n"\
        +"set alias="+cfg["alias"]+"\n"\
        +"set langaltin="+cfg["langAltFile"]+"\n"\
        +"set langin="+cfg["trlangFile"]+"\n"\
        +"set langout=SUNBF"+cfg["version"]+"_"+cfg["alias"]+"\n"\
        +"\n\n@echo off\n"\
        +"@echo sfd file: \t%sfd%\n"\
        +"@echo kmn file: \t%kmn%\n"\
        +"@echo version: \t%ver%\n"\
        +"@echo ttffont: \t%ttffont%\n"\
        +"@echo alias: \t\t%alias%\n"\
        +"@echo langaltin: \t%langaltin%\n"\
        +"@echo langin: \t%langin%\n"\
        +"@echo langout: \t%langout%"

    f = open('doEnv.bat', 'w')
    f.write(batEnv) 
    f.close()

if __name__ == "__main__":
   
    cfg = readCfg()
    saveCfg(cfg, True)
   