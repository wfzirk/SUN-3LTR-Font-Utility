
# https://www.tcl.tk/man/tcl/TkCmd/ttk_widget.htm
# https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-state-spec.html

import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import scrolledtext
import subprocess
from csv import reader
import re
from bfConfig import *
from autocomp import AutoComplete
'''
root = tk.Tk()

root.title("SUN Font Utility    "+bfVersion)
root.resizable(width=False, height=False)

windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()

positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/5 - windowHeight/2)
 
# Positions the window in the center of the page.
root.geometry("+{}+{}".format(positionRight, positionDown))
 
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=11)
root.option_add("*Font", default_font)

cfg = readCfg()
'''
#cfg["eFilter"] = "" 
    
#lb_entry = {}
# https://www.loc.gov/standards/iso639-2/php/code_list.php
'''
ISO 639-2 Code,	ISO 639-1 Code,	English name of Language,	French name of Language,	German name of Language,	Comment 
    aar,                	aa,                     	Afar,                                           	afar,                       	Danakil-Sprache	          
'''
#cfg = readCfg()

def readData():
    cfg = readCfg()
    print('readData')
    iso639_file = cfg["iso639"]
    if not iso639_file: return None
    
    tmp = iso639_file.split('.')
    ext = tmp[len(tmp)-1]
    if ext == 'tab':
        delimiter = '\t'
    elif ext == 'csv':
        delimiter = ','
    dList = {}
    
    with open('iso639SubList.tab', 'r') as read_obj:
        csv_reader = reader(read_obj, delimiter = delimiter)
        langlist = list(csv_reader)
        x = 0
        for item in langlist:
            lang = item[1]
            alias = item[0].upper()
            # using findall() to get all substrings
            # 0th index gives 1st substring
            res = re.findall("[\dA-Za-z]*", lang)[0]
            if x > 0:
                m = alias+'     \t\t'+res
                dList[m] = alias.strip()
                
            x+=1
    

    with open(iso639_file, 'r') as read_obj:
        csv_reader = reader(read_obj, delimiter = delimiter)
        langlist = list(csv_reader)
        x = 0
        len_max = 0
        for item in langlist:
            lang = item[6]
            alias = item[0].upper()
            # using findall() to get all substrings
            # 0th index gives 1st substring
            res = re.findall("[\dA-Za-z]*", lang)[0]
            if x > 0:
                m = alias+'     \t\t'+res
                dList[m] = lang.strip()
                if len(m) > len_max:
                    len_max = len(m)

            x+=1
    return dict(sorted(dList.items(), key=lambda item: item[0])) 

class BfSetup:
    def __init__(self, master):
        self.master = master
        self.cfg = readCfg()
        print('bfsetup iso639', self.cfg["iso639"])
        
        self.ver_var = tk.StringVar()
        self.ver_var.set(self.cfg["version"]) 
        
        self.iso639_var = tk.StringVar()
        self.iso639_var.set(os.path.basename(self.cfg["iso639"])) 
        
        self.iso639Sub_var = tk.StringVar()
        self.iso639Sub_var.set(os.path.basename(self.cfg["iso639sub"])) 
        
        self.alias_var = tk.StringVar()
        self.alias_var.set(os.path.basename(self.cfg["alias"])) 
        self.alias_var.trace("w", self.update_alias)
        
        self.ttf_var = tk.StringVar()
        self.ttf_var.set(os.path.basename(self.cfg["ttf"]))
        
        self.sfd_var = tk.StringVar()
        self.sfd_var.set(os.path.basename(self.cfg["sfdFile"]))
        
        self.kmn_var = tk.StringVar()
        self.kmn_var.set(os.path.basename(self.cfg["kmnFile"]))
        
        self.alt_var = tk.StringVar()
        self.alt_var.set(os.path.basename(self.cfg["langAltFile"]))
        
        self.trl_var = tk.StringVar()
        self.trl_var.set(os.path.basename(self.cfg["trlangFile"]))
        
        self.bfont_var = tk.StringVar()
        self.bfont_var.set(self.cfg["backFont"])


        top_frame = tk.Frame(master, bg='cyan', width=420, height=25, pady=1)
        center = tk.Frame(master, bg='lightgray', width=415, height=150, padx=5, pady=5)
        ctr_btm = tk.Frame(master, bg='lightblue', width=415, height=200, padx=5, pady=5)
        btm_frame = tk.Frame(master, bg='white', width=420, height=25, pady=3)

        top_frame.grid(row=0, columnspan=2,sticky="ew")
        center.grid(row=1,column=0, sticky="nsew")
        ctr_btm.grid(row=2,column=0, sticky="nsew")
        btm_frame.grid(row=3, columnspan=2, sticky="ew")


        # create the center frames
        center.grid_rowconfigure(0, weight=1)
        center.grid_columnconfigure(1, weight=1)
        center.grid_columnconfigure(2, weight=1)
        center.grid_columnconfigure(3, weight=1)
        center.grid_columnconfigure(4, weight=1)

        #  add widgets to center left
        row = 1
        lbl0 = tk.Label(center, bg='lightblue', text="Version", width=12, anchor=tk.W)
        lbl0.grid(row=row, column=0, sticky=tk.W)
        self.ver = tk.Entry(center, width=32, relief=tk.RIDGE,textvariable = self.ver_var, bg='lightyellow') #, textvariable=bfClass.version)
        self.ver.grid(row=row, column=1, sticky=tk.W)
        self.ver.bind('<KeyRelease>', self.versionClicked)
        tk.Label(center, bg='lightblue', text="i.e. 78_1210", anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)

        row+=1
        tk.Label(center, bg='lightblue', text="ISO639 list", anchor=tk.W).grid(column=0, row=row, sticky=tk.W)   #, columnspan=1)
        self.iso639 = tk.Entry(center,width=42, textvariable = self.iso639_var, bg='lightyellow')
        self.iso639.grid(column=1, row=row, sticky=tk.W, columnspan=3)
        self.iso639.bind("<1>", self.iso639Clicked)
        tk.Label(center, bg='lightblue', text="i.e. iso-639-3.tab",  anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)
        
        row+=1
        tk.Label(center, bg='lightblue', text="ISO639 sub list", anchor=tk.W).grid(column=0, row=row, sticky=tk.W)   #, columnspan=1)
        self.iso639Sub = tk.Entry(center,width=32, textvariable = self.iso639Sub_var, bg='lightyellow')
        self.iso639Sub.grid(column=1, row=row, sticky=tk.W, columnspan=3)
        self.iso639Sub.bind("<1>", self.iso639SubClicked)
        tk.Label(center, bg='lightblue', text="i.e. iso_sublist.tab",  anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)

        row+=1
        lbl1 = tk.Label(center, bg='lightblue', text="Language", width=8, anchor=tk.E, padx=1,pady=1)
        lbl1.grid(row=row, column=0, sticky=tk.W)

        lb_frame = tk.Frame(center, bg='lightgray')
        lb_frame.grid(row=row, column=1, columnspan=1,  sticky=tk.W)

        tk.Label(center, bg='lightgreen', text="i.e. ENG", anchor=tk.W).grid(row=row, column=2, columnspan=2, sticky=tk.N)

        #row+=1
        data = readData()
        #print(data)
        if data:
           ac = AutoComplete(lb_frame, self.alias_var, data)
           #ac.width = 145
        #ac.grid(row=row, column=1)

        lbl2 = tk.Label(center, bg='lightblue', text="Alias",width=4, anchor=tk.W)
        lbl2.grid(row=row, column=3, sticky=tk.E)
        self._alias = tk.Entry(center, textvariable = self.alias_var, bg='lightblue', width=8)
        self._alias.grid(row=row, column=4, sticky=tk.W)
        #_alias.bind("<1>", _aliasClicked)
   
        row = row+2
        lbl3a = tk.Label(center, bg='lightblue', text="Font File", width=8, anchor=tk.W)
        lbl3a.grid(column=0, row=row, sticky=tk.W)   #, columnspan=1)
        self.ttf = tk.Entry(center,width=32, textvariable = self.ttf_var, bg='lightyellow')
        self.ttf.grid(column=1, row=row, sticky=tk.W, columnspan=3)
        self.ttf.bind("<1>", self.ttfClicked)
        tk.Label(center, bg='lightblue', text="i.e. times.ttf",  anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)

        row = row+1
        lbl3 = tk.Label(center, bg='lightblue', text="SFD File")
        lbl3.grid(column=0, row=row, sticky=tk.W, columnspan=1)
        self.sfd = tk.Entry(center, textvariable = self.sfd_var, bg='lightyellow',width=32)
        self.sfd.grid(column=1, row=row, sticky=tk.W, columnspan=4 )
        self.sfd.bind("<1>", self.sfdClicked)
        tk.Label(center, bg='lightblue', text="i.e. sun7_8_1210.sfd",  anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)
        if cfg["alias"] == "ENG":
            self.sfd.configure(state='normal')
        else:
            self.sfd.configure(state='disabled')

        row = row+1
        lbl4 = tk.Label(center, bg='lightblue', text="KMN File")
        lbl4.grid(column=0, row=row, sticky=tk.W, columnspan=1)
        self.kmn = tk.Entry(center, textvariable = self.kmn_var, bg='lightyellow',width=32)
        self.kmn.grid(column=1, row=row, sticky=tk.W, columnspan=4 )
        self.kmn.bind("<1>", self.kmnClicked)
        tk.Label(center, bg='lightblue', text="i.e. sun7_8_1210.kmn",  anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)

        #Alternate word file
        row = row+1
        lbl6a = tk.Label(center, bg='lightblue', text="ALT Word File")
        lbl6a.grid(column=0, row=row, sticky=tk.W, columnspan=1)
        self.alt = tk.Entry(center, textvariable = self.alt_var, bg='lightyellow',width=32)
        self.alt.grid(column=1, row=row, sticky=tk.W, columnspan=4 )
        self.alt.bind("<1>", self.altClicked)
        tk.Label(center, bg='lightblue', text="dict_list_alt1_POR.xlsx",  anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)

        #Translators Dictionary Sun 7_22 on 8_9_2019_fixed.ods
        row = row+1
        lbl6 = tk.Label(center, bg='lightblue', text="TRLang File")
        lbl6.grid(column=0, row=row, sticky=tk.W, columnspan=1)
        self.trl = tk.Entry(center, textvariable = self.trl_var, bg='lightyellow',width=32)
        self.trl.grid(column=1, row=row, sticky=tk.W, columnspan=4 )
        self.trl.bind("<1>", self.trlClicked)
        tk.Label(center, bg='lightblue', text="Tr...Dict...xxx.ods",  anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)

        #Back Font
        row = row+1
        lbl7 = tk.Label(center, bg='lightblue', text="BackFont")
        lbl7.grid(column=0, row=row, sticky=tk.W, columnspan=1)
        self.bfont = tk.Entry(center, textvariable = self.bfont_var,width=32)
        self.bfont.grid(column=1, row=row, sticky=tk.W, columnspan=4 )
        self.bfont.configure(state='disabled')

        text_box = tk.Text(
            ctr_btm,
            height=6,
            bg='lightgray',
            width=50
        )
        text_box.pack(expand=True, fill=tk.X )
        message = '\nNote: \tThe Iso639SubList is a tab or comma separated list of 3 or 4 letters,'
        message = message + '\n\tcolumns are:  Id, Ref_name, Comment.'
        message = message + '\ni.e.\t Id \tRef_Name	\tComment'
        message = message + '\n\tpoa \tPortuguese African\t\tactive translation work underway '
         
        text_box.insert('end', message)
        text_box.config(state='disabled')
        
        cncl = tk.Button(btm_frame, text = "Cancel") 
        cncl.pack(side=tk.RIGHT)
        cncl.bind("<1>", self.bfCancel)

        ext = tk.Button(btm_frame, text = "Save", padx=5) 
        ext.pack(side=tk.RIGHT)
        ext.bind("<1>", self.bfExit)
        
        #self.updateVars()
    def update_alias(self, *args):
        self.cfg["alias"] = self.alias_var.get() 
        updateCfg(self.cfg)
        self.bfont_var.set(self.cfg["backFont"])
        if cfg["alias"] == "ENG":
            enState = 'normal'
            laState = 'disabled'
        else:
            enState = 'disabled'
            laState = 'normal'
            
        self.sfd.configure(state=enState)
        self.trl.configure(state=laState)
        self.alt.configure(state=laState)
        
    def updateVars(self):
        print('updatevars',self.cfg["iso639"])
        updateCfg(self.cfg)

    def bfExit(self, event):
        print('exit')
        self.updateVars()
        #updateCfg(cfg)
        #writeBat(cfg)
        self.master.destroy()
        quit()

    def bfCancel(self,event):
        self.master.destroy()
        quit()

    def versionClicked(self, event):
        self.cfg["version"] = self.ver_var.get()
        print('versionclicked', self.cfg["version"])
     
    def iso639Clicked(self, event):
        print("iso639clicked")
        self.cfg["iso639"] = filedialog.askopenfilename(filetypes = (("Tab files","*.tab"),("CSV files",".csv"),("all files","*.*")))
        self.iso639_var.set(os.path.basename(self.cfg["iso639"])) 

    def iso639SubClicked(self, event):
        print("iso639Subclicked")
        self.cfg["iso639sub"] = filedialog.askopenfilename(filetypes = (("Text files","*.tab"),("CSV files",".csv"),("all files","*.*")))
        self.iso639Sub_var.set(os.path.basename(self.cfg["iso639sub"])) 
     
    def ttfClicked(self,event):
        print('ttfclicked')
        self.cfg["ttf"] = filedialog.askopenfilename(filetypes = (("Text files","*.ttf"),("all files","*.*")))
        self.ttf_var.set(os.path.basename(self.cfg["ttf"]))

    def sfdClicked(self, event):
        print('sfdclicked')
        if self.cfg["alias"] == "ENG":
            self.cfg["sfdFile"] = filedialog.askopenfilename(filetypes = (("Text files","*.sfd"),("all files","*.*")))
        else:
            self.cfg["sfdFile"] = ""
        self.sfd_var.set(os.path.basename(self.cfg["sfdFile"]))
        
    def kmnClicked(self,event):
        print('kmnclicked')
        self.cfg["kmnFile"] = filedialog.askopenfilename(filetypes = (("Text files","*.kmn"),("all files","*.*")))
        self.cfg["trlangFile"] = ""
        self.kmn_var.set(os.path.basename(self.cfg["kmnFile"]))
        self.trl_var.set(os.path.basename(self.cfg["trlangFile"]))

    def trlClicked(self,event):
        print('trlclicked')
        spread_exts = r"*.xlsx *.ods *.csv"
        self.cfg["trlangFile"] = filedialog.askopenfilename(filetypes = (("SpreadSheets",spread_exts),("all files","*.*")))
        self.cfg["kmnFile"]  = ""
        self.cfg["sfdFile"] = ""
        self.kmn_var.set(os.path.basename(self.cfg["kmnFile"]))
        self.sfd_var.set(os.path.basename(self.cfg["sfdFile"]))
        self.trl_var.set(os.path.basename(self.cfg["trlangFile"]))
        
    def altClicked(self, event):
        print('altclicked')
        if self.cfg["alias"] != "ENG":
            spread_exts = r"*.xlsx *.ods *.csv"
            self.cfg["langAltFile"] = filedialog.askopenfilename(filetypes = (("SpreadSheets",spread_exts),("all files","*.*")))
        else:
            self.cfg["langAltFile"] = ""
        self.alt_var.set(os.path.basename(self.cfg["langAltFile"]))
  
def main():
    
    root = tk.Tk()

    root.title("SUN Font Utility    "+bfVersion)
    root.resizable(width=False, height=False)

    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()

    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/5 - windowHeight/2)
     
    # Positions the window in the center of the page.
    root.geometry("+{}+{}".format(positionRight, positionDown))
     
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=11)
    root.option_add("*Font", default_font)
    #updateVars()
    BfSetup(root)
    root.mainloop()


if __name__ == "__main__":

    #updateVars()
    #root.mainloop()
    main()