
# https://www.tcl.tk/man/tcl/TkCmd/ttk_widget.htm
# https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-state-spec.html

import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import scrolledtext
import subprocess
from csv import reader
from bfConfig import *

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
cfg["eFilter"] = "" 
    
lb_entry = {}
# https://www.loc.gov/standards/iso639-2/php/code_list.php
'''
ISO 639-2 Code,	ISO 639-1 Code,	English name of Language,	French name of Language,	German name of Language,	Comment 
    aar,                	aa,                     	Afar,                                           	afar,                       	Danakil-Sprache	          
'''
#import sys

def get_langlist(lb_entry, csv_file):
    #print('get_langlist')
    csv_file = cfg["language_codes"]
    ALIASCOL = 0    # col 0 = 3 letter alias,  col 1 = 2 letter alias
    if ALIASCOL ==1:
        ACOLLEN = 2   
    else:
        ACOLLEN = 3
    NAMECOL = 2
    with open(csv_file, 'r') as read_obj:
        csv_reader = reader(read_obj)
        x = 0
        for item in list(csv_reader):
            lang = item[NAMECOL]
            alias = item[ALIASCOL].upper()
            if x > 0:
                if len(item[ALIASCOL]) == ACOLLEN:
                    lb_entry[alias+' '+lang] = alias.strip()
                else:           # need to handle multiple alias for language
                    allAlias = alias.split('\n')
                    for a in allAlias:
                        lb_entry[a+' '+lang] = a.replace('(B)','').replace('(T)','').strip()
                    
            x = x+1

    key_sort = dict(sorted(lb_entry.items(), key=lambda item: item[0]))
    return key_sort

def updateVars():
    print('update vars',cfg["alias"],)

    updateCfg(cfg)
    #CB.setState()
    e0.delete(0,tk.END)
    e0.insert(0,cfg["version"])
    
    _alias.delete(0,tk.END)
    _alias.insert(0,cfg["alias"])
    
    if cfg["alias"] == "ENG":
        enState = 'normal'
        laState = 'disabled'
    else:
        enState = 'disabled'
        laState = 'normal'
    ttfName = os.path.basename(cfg["ttf"])
    ttf.delete(0, tk.END)
    ttf.insert(0, ttfName)
    sfdName = os.path.basename(cfg["sfdFile"])
    sfd.delete(0, tk.END)
    sfd.insert(0, sfdName)
    sfd.configure(state=enState)
    kmnName = os.path.basename(cfg["kmnFile"])
    kmn.delete(0, tk.END)
    kmn.insert(0, kmnName)
    kmn.configure(state=enState)
    trlName = os.path.basename(cfg["trlangFile"])
    trl.delete(0, tk.END)
    trl.insert(0, trlName)
    trl.configure(state=laState)
    altName = os.path.basename(cfg["langAltFile"])
    alt.delete(0, tk.END)
    alt.insert(0, altName)
    alt.configure(state=laState)
    return
   
def bfExit(e):
    updateCfg(cfg)
    writeBat(cfg)
    root.destroy()
    quit()

def bfCancel(e):
    root.destroy()
    quit()

def versionClicked(e):
    sv = e0.get()
    b = sv
    cfg["version"] = sv
    print('versionclicked',sv, cfg["version"])
    updateVars()
    
def xefltrClicked(e):
    cfg["eFilter"] = efltr.get()
    updateCfg(cfg)
        
    
def ttfClicked(e):
    cfg["ttf"] = filedialog.askopenfilename(filetypes = (("Text files","*.ttf"),("all files","*.*")))
    updateVars()
 
def sfdClicked(e):
    if cfg["alias"] == "ENG":
        cfg["sfdFile"] = filedialog.askopenfilename(filetypes = (("Text files","*.sfd"),("all files","*.*")))
        updateVars()
    
def kmnClicked(e):
    if cfg["alias"] == "ENG":
        cfg["kmnFile"] = filedialog.askopenfilename(filetypes = (("Text files","*.kmn"),("all files","*.*")))
        updateVars()
    
def trlClicked(e):
    if cfg["alias"] != "ENG":
        spread_exts = r"*.xlsx *.ods *.csv"
        cfg["trlangFile"] = filedialog.askopenfilename(filetypes = (("SpreadSheets",spread_exts),("all files","*.*")))
        updateVars()
    
def altClicked(e):
    if cfg["alias"] != "ENG":
        spread_exts = r"*.xlsx *.ods *.csv"
        cfg["langAltFile"] = filedialog.askopenfilename(filetypes = (("SpreadSheets",spread_exts),("all files","*.*")))
        updateVars()
    


class TextIO:
    def __init__(self, text):
        self.text = text
    def write(self, msg):
        self.text.update_idletasks()
        self.text.insert(END, msg)
        self.text.see(END)
    def flush(self):
        pass 

class srchListBox(tk.Frame):

    def __init__(self, master, lboxList):
        tk.Frame.__init__(self, master)
        self.lboxList = lboxList
        #self.pack()
        self.grid(row=1, column = 1, sticky=tk.W)
        self.create_widgets()

    # Create main GUI window
    def create_widgets(self):
        self.search_var = tk.StringVar()
        self.search_var.set(cfg["alias"])
        self.search_var.trace("w", self.update_list)
        self.entry = tk.Entry(self, textvariable=self.search_var, width=13)
        self.lbox = tk.Listbox(self, width=17, height=8)
        self.entry.grid(row=0, column=0, padx=10, pady=3)
        self.lbox.grid(row=1, column=0, padx=10, pady=3)
        self.lbox.bind("<<ListboxSelect>>", self.langClicked)
        self.entry.bind("<Escape>", self.clearEntry)        
        scrollbar = tk.Scrollbar(lb_frame, orient="vertical", command=self.lbox.yview)
        self.lbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=2, sticky='ns')
        # Function for updating the list/doing the search.
        # It needs to be called here to populate the listbox.
        self.update_list()
        
    def update_list(self, *args):
        search_term = self.search_var.get()
        #print('update_list',search_term)
        
        self.lbox.delete(0, tk.END)

        for item in self.lboxList:
                if search_term.lower() in item.lower():
                    self.lbox.insert(tk.END, item)
    
    def clearEntry(self, *args):
        self.search_var.set("")
        
    def langClicked(self, event):
        # https://www.loc.gov/standards/iso639-2/php/code_list.php
        '''
        ISO 639-2 Code,	ISO 639-1 Code,	English name of Language,	French name of Language,	German name of Language,	Comment 
            aar,                	aa,                     	Afar,                                           	afar,                       	Danakil-Sprache	          
        '''
        selection = event.widget.curselection()
        #print('langclicked',selection)
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            self.search_var.set(data)
            cfg["language"] = data
            cfg["alias"] = lb_entry[data]
            _alias.delete(0, tk.END)
            _alias.insert(0, lb_entry[data])
            
        else:
            self.search_var.set("")
        updateVars()


top_frame = tk.Frame(root, bg='cyan', width=400, height=25, pady=1)
center = tk.Frame(root, bg='lightblue', width=395, height=150, padx=5, pady=5)
ctr_btm = tk.Frame(root, bg='lightblue', width=395, height=200, padx=5, pady=5)
btm_frame = tk.Frame(root, bg='white', width=400, height=25, pady=3)


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
lbl0 = tk.Label(center, bg='lightblue', text="Version", width=8, anchor=tk.W)
lbl0.grid(row=row, column=0, sticky=tk.W)
e0 = tk.Entry(center, width=22, relief=tk.RIDGE) #, textvariable=bfClass.version)
e0.grid(row=row, column=1, sticky=tk.W)
e0.bind('<KeyRelease>', versionClicked)
tk.Label(center, bg='lightblue', text="i.e. 78_1210", anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)

row = row+1
lbl1 = tk.Label(center, bg='lightblue', text="Language", width=8, anchor=tk.E, padx=1,pady=1)
lbl1.grid(row=row, column=0, sticky=tk.W)

lb_frame = tk.Frame(center, bg='lightgray')
lb_frame.grid(row=row, column=1, columnspan=1,  sticky=tk.W)

tk.Label(center, bg='lightgreen', text="i.e. ENG", anchor=tk.W).grid(row=row, column=2, columnspan=2, sticky=tk.N)

csv_file = ('Language Codes.csv') 
lb_entry= get_langlist(lb_entry, csv_file)
lbs = srchListBox(lb_frame, lb_entry)

lbl2 = tk.Label(center, bg='lightblue', text="Alias",width=4, anchor=tk.W)
lbl2.grid(row=row, column=3, sticky=tk.E)
_alias = tk.Entry(center,bg='lightyellow', width=8)
_alias.grid(row=row, column=4, sticky=tk.W)

row = row+2
lbl3a = tk.Label(center, bg='lightblue', text="Font File", width=8, anchor=tk.W)
lbl3a.grid(column=0, row=row, sticky=tk.W)   #, columnspan=1)
ttf = tk.Entry(center,width=22,bg='lightyellow')
ttf.grid(column=1, row=row, sticky=tk.W, columnspan=3)

ttf.bind("<1>", ttfClicked)
tk.Label(center, bg='lightblue', text="i.e. times.ttf",  anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)

row = row+1
lbl3 = tk.Label(center, bg='lightblue', text="SFD File")
lbl3.grid(column=0, row=row, sticky=tk.W, columnspan=1)
sfd = tk.Entry(center,width=22)
sfd.grid(column=1, row=row, sticky=tk.W, columnspan=4 )

sfd.bind("<1>", sfdClicked)
tk.Label(center, bg='lightblue', text="i.e. sun7_8_1210.sfd",  anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)

row = row+1
lbl4 = tk.Label(center, bg='lightblue', text="KMN File")
lbl4.grid(column=0, row=row, sticky=tk.W, columnspan=1)
kmn = tk.Entry(center,width=22)
kmn.grid(column=1, row=row, sticky=tk.W, columnspan=4 )

kmn.bind("<1>", kmnClicked)
tk.Label(center, bg='lightblue', text="i.e. sun7_8_1210.kmn",  anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)

#Alternate word file
row = row+1
lbl6a = tk.Label(center, bg='lightblue', text="ALT Word File")
lbl6a.grid(column=0, row=row, sticky=tk.W, columnspan=1)
alt = tk.Entry(center,width=22)
alt.grid(column=1, row=row, sticky=tk.W, columnspan=4 )

alt.bind("<1>", altClicked)
tk.Label(center, bg='lightblue', text="dict_list_alt1_POR.xlsx",  anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)

#Translators Dictionary Sun 7_22 on 8_9_2019_fixed.ods
row = row+1
lbl6 = tk.Label(center, bg='lightblue', text="TRLang File")
lbl6.grid(column=0, row=row, sticky=tk.W, columnspan=1)
trl = tk.Entry(center,width=22)
trl.grid(column=1, row=row, sticky=tk.W, columnspan=4 )

trl.bind("<1>", trlClicked)
tk.Label(center, bg='lightblue', text="Tr...Dict...xxx.ods",  anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)

cncl = tk.Button(btm_frame, text = "Cancel") 
cncl.pack(side=tk.RIGHT)
cncl.bind("<1>", bfCancel)

ext = tk.Button(btm_frame, text = "Save", padx=5) 
ext.pack(side=tk.RIGHT)
ext.bind("<1>", bfExit)
     

if __name__ == "__main__":

    updateVars()
    root.mainloop()