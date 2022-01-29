import datetime

import signal
import time
from datetime import datetime
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W
import subprocess
.
#import logging
#from bfLog import log_setup

from bfConfig import *

import inspect

def lineno():
    """Returns the current line number in the script."""
    return inspect.currentframe().f_back.f_lineno


cfg = readCfg()
cfg["eFilter"] = ""

class FFcmdThrd(threading.Thread):

    def __init__(self, cmd, cbfstop,
                 group=None, name=None, daemon=True):
        super().__init__(group=group, name=name, daemon=daemon)

        self.cmd = cmd
        self.cbfstop = cbfstop
        
        logging.info('process started')
        self.process = subprocess.Popen(self.cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             text=True)
         
        
    def run(self):

        for line in self.process.stdout:
            if self.cbfstop.is_set():
                # if stopping was requested, terminate the process and bail out
                logging.info('terminate')
                self.process.terminate()
                break

            ConsoleUi.displayText(line)

        try: 
            # give process a chance to exit gracefully
            logging.debug('Exiting')
            self.process.wait(timeout=3)
        #except TimeoutExpired:
        except Exception as e:
            # otherwise try to terminate it forcefully
            logging.error('timeout expired')
            self.process.kill()
            
        self.stop()
        logging.debug('Stopped returncode %d',self.process.returncode)
        return self.process.returncode
    
    def returncode(self):
        return self.process.returncode
        
    def stop(self):
        #logging.debug('stop called')
        # request the thread to exit gracefully during its next loop iteration
        self.cbfstop.set()
 
    def stopped(self):
        c = self.cbfstop.is_set()
        return c

class ConsoleUi(logging.Handler):
    def __init__(self, parent, update_interval=50, process_lines=500):
        logging.Handler.__init__(self)

        self.update_interval = update_interval
        self.process_lines = process_lines
        self.parent = parent
        #self.after(self.update_interval, self.fetch_lines)
        
        # Create a ScrolledText wdiget
        self.scrolled_text = ScrolledText(self.parent, state='disabled', height=20)
        self.scrolled_text.grid(row=0, column=0, sticky=(N, S, W, E))
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='orangered')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
        self.scrolled_text.tag_config('OTHER', foreground='blue')
       
        #ConsoleUi.display = self.display
        ConsoleUi.displayText = self.displayText
        ConsoleUi.clearDisp = self.clearDisp

    def emit(self, record):
        msg = self.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)

    def clearDisp(self, *args):
        print('clearDisp')
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.delete(0.0, tk.END)
        self.scrolled_text.configure(state='disabled')
    
    def displayText(self, *args):       # for text files
        text = ' '.join([str(a) for a in args])
        print(text, end='')
        self.scrolled_text.configure(state='normal')
        if ' ERROR ' in text:
            tag = 'ERROR'
        elif ' DEBUG ' in text:
            tag = 'DEBUG'
        elif ' INFO ' in text:
            tag = 'INFO'
        elif ' WARNING ' in text:
            tag = 'WARNING'
        elif ' CRITICAL ' in text:
            tag = 'CRITICAL'
        else:
            tag = 'OTHER'
            text = text+'\n'    
        self.scrolled_text.insert(tk.END, text, tag)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)
        self.scrolled_text.update_idletasks()
    

class CBFrame: #(threading.Thread):
    
    alias = cfg["alias"]
    chkbs = []  # array of checkboxes

    def __init__(self, frame):
        threading.Thread.__init__(self)
        self.frame = frame      
        self.after = frame.after
        self.cbfstop = threading.Event()
        #self.process = None

        CBFrame.runCmds = self.runCmds
        CBFrame.stop = self.stop
        #CBFrame.stop_event = threading.Event()
        top_frame = ttk.Labelframe(self.frame, text="Selection", height=35)
        top_frame.pack(side=tk.TOP, fill="both", expand="yes")
        bot_frame = ttk.Labelframe(self.frame, text="", height=5)
        bot_frame.pack(side=tk.BOTTOM, fill="both", expand="yes")
        
        #cbstyle = ttk.Style()
        # Create style used by default for all Frames
        
        cb1 = CBFrame.addCB(top_frame, 'kmn2csv') #, kmn2csvMain)  
        cb2 = CBFrame.addCB(top_frame, 'sfd2csv') #, sfd2csvMain)  
        cb3 = CBFrame.addCB(top_frame, 'langpri') #, langpriMain)  
        cb4 = CBFrame.addCB(top_frame, 'csv2kmn') #, csv2kmnMain)  
        cb5 = CBFrame.addCB(top_frame, 'csv2svg') #, csv2svgMain)  
        cb6 = CBFrame.addCB(top_frame, 'svg2font') #, svg2fontMain ) 
        cb7 = CBFrame.addCB(top_frame, 'back2doc') #, back2docMain) 
        cb8 = CBFrame.addCB(top_frame, 'compact') #, compactMain)  
        cb9 = CBFrame.addCB(top_frame, 'bfzip') #, bfzipMain)
        
        cBtn1 = tk.Button(bot_frame, text="set All",width=5, padx=3)
        cBtn1.grid(row=0,column=0,sticky=tk.W)
        cBtn1.bind("<1>", CBFrame.setAll)
        
        cBtn2 = tk.Button(bot_frame, text="clr All", width=5, padx=3)
        cBtn2.grid(row=0,column=1, sticky=tk.W)
        cBtn2.bind("<1>", CBFrame.clrAll)

    def addCB(frame, funcName, func=""):
        style = ttk.Style()
        style.configure('Green.TCheckbutton', foreground='green')
        ckbtn = ttk.Checkbutton(frame, text=funcName)   #, anchor=tk.W)
        ckbtn.state(['!disabled','!selected','!alternate']) # clear the checkbox
        ckbtn.pack(side=tk.TOP, expand=1, fill=tk.X)
        ckbtn.configure(style='TCheckbutton')
        #print('addcb',ckbtn)
        #print('style', ttk.Style(ckbtn))
        cbarry = [ckbtn, funcName, func] 
        CBFrame.chkbs.append(cbarry)
        CBFrame.cbState(cbarry[0])
                 
    def clr():
        ConsoleUi.clearDisplay()
        
    def cbState(chk):
        ste = bfCmds(cfg, chk.cget("text"))[0]
        #print('cbstate',CBFrame.alias, ste, chk.cget("text"))
        s = False
        if ste == 'both':
            s = True
        elif CBFrame.alias == "ENG" and ste == CBFrame.alias:
            s = True
        elif ste != "ENG" and CBFrame.alias != "ENG":
            s = True
        if s:
            chk.state(['!disabled','!selected','!alternate'])
        else:
            chk.state(['disabled','!selected','!alternate'])

    def setState():
        CBFrame.alias = cfg["alias"]
        for i in CBFrame.chkbs:
            CBFrame.cbState(i[0])
            
    def clrAll(e):
        CBFrame.alias = cfg["alias"]
        #CBFrame.cbCfg()
        for i in CBFrame.chkbs:
            #i[0].configure(style='TCheckButton')
            i[0].state(['!selected','!alternate'])
                   
    def setAll(e):
        CBFrame.alias = cfg["alias"]
        #CBFrame.cbCfg()
        for i in CBFrame.chkbs:
            #i[0].configure(style='TCheckButton')
            i[0].state(['selected', '!alternate'])
                
    def run(self):
        logging.debug('run,running')
        
    def stop(self, *args):
        logging.error('cbframe.stop ABORT')
        self.cbfstop.set()
        
    def runCmds(self, *args):  #, *args):
        #run in subprocess def runCmds
        updateCfg(cfg)
        debug = (cfg["debug"] == "True")     
        print('updatecfg', cfg["eFilter"], debug)  
       
        ConsoleUi.clearDisp()

        #cmdList = []
        rc = -1
        for i in CBFrame.chkbs: 
            cb = i[0]
            #print('cb',cb.configure())
            scrName = i[1]
            func = i[2]
    
            sel = cb.instate(['selected','!disabled'])   # [ckbs, funcname, func ]
            #ConsoleUi.displayText('cbstate %s', cb.state(), sel)
            if not sel:
                continue

            cb.configure(style='Green.TCheckbutton')
            cb.state(['!alternate'])
            cb.update_idletasks()
            
            cmd = bfCmds(cfg, cb.cget("text"))[1]
            func = i[2]
    
            ffcmd = ['cmd', '/c', 'fontforge', '-quiet', '-script']

            for c in cmd:
                ffcmd.append(c)
            logging.info('cmd called %s', cmd[0])
            
            ffstr = ''
            for i in ffcmd:
                ffstr = ffstr+' '+i
            '''
            rc = RunFF(ffcmd, self.frame)
            #ConsoleUi.displayText(datetime.now(),lineno(),'running ', cmd[0],'\n') 
            '''
   
            self.cbfstop.clear()
            reader = FFcmdThrd(ffcmd, self.cbfstop)
            reader.start()

            self.after(1000)
            logging.debug('wait for command complete')
            while not reader.stopped(): 
                self.frame.update()   #.idletasks()
                self.after(0)
            #self.frame.update.idletasks()
            rc = reader.returncode()
            logging.info('cbf completed returncode %s',reader.returncode()) 
            del reader
  
            cb.configure(style='TCheckbutton')
            cb.state(['!alternate'])
            cb.update_idletasks()
            logging.debug('cbf.next %s', rc )
            if rc:
                break
        #caller.update_idletasks()
        return rc
 

class InputUi:
      
    def versionClicked(self, *args):
        #print('version clicked', self.e0.get())
        #sv = InputUi.e0.get()
        #b = sv
        cfg["version"] = self.e0.get()
        #print('versionclicked',sv, cfg["version"])
        self.updateVars(self)
        
    def langClicked(self, *args):
        sv = self.e1.get()
        sv = sv.capitalize()
        cfg["language"] = sv
        cfg["alias"] = langParms[sv]
        self.updateVars()

    def aliasClicked(self, *args):
        #global cfg
        a = self.e2.get().upper()
        #lookup = {value: key for key, value in cg.langParms}
        found = False
        for k in langParms:
            value = langParms[k]
            if value == a:
                found = True
                break
        #print('aliasclicked',k,value, found)
        if found:
            cfg["language"] = k
            cfg["alias"] = a
            self.updateVars()  

    def efltrClicked(self, *args):
        cfg["eFilter"] = self.efltr.get()
        #updateCfg(cfg)
            
        
    def ttfClicked(self,*args):
        cfg["ttf"] = filedialog.askopenfilename(filetypes = (("Text files","*.ttf"),("all files","*.*")))
        self.updateVars()
     
    def sfdClicked(self, *args):
        cfg["sfdFile"] = filedialog.askopenfilename(filetypes = (("Text files","*.sfd"),("all files","*.*")))
        self.updateVars()
        
    def kmnClicked(self, *args):
        cfg["kmnFile"] = filedialog.askopenfilename(filetypes = (("Text files","*.kmn"),("all files","*.*")))
        self.updateVars()
        
    def trlClicked(self, *args):
        cfg["trlangFile"] = filedialog.askopenfilename(filetypes = (("Text files","*.ods"),("all files","*.*")))
        self.updateVars()
    
    def __init__(self, frame):
        self.frame = frame
 
        self.pwFile = tk.StringVar()
        self.langFile = tk.StringVar()
        self.backFont = tk.StringVar()
        self.kmncsv = tk.StringVar()
        self.back2doc = tk.StringVar()
        self.compactFile = tk.StringVar()
        InputUi.updateVars = self.updateVars
        
        top_frame = ttk.Labelframe(self.frame, text="Inputs", height=10)
        top_frame.pack(side=tk.TOP, fill="both", expand="yes")
        bot_frame = ttk.Labelframe(self.frame, text="Outputs", height=10)
        bot_frame.pack(side=tk.BOTTOM, fill="both", expand="yes")
        
        
        
        row = 1
        lbl0 = ttk.Label(top_frame, text="Version", width=8, anchor=tk.W)
        lbl0.grid(row=row, column=0, sticky=tk.W)
        self.e0 = ttk.Entry(top_frame, width=10)   #, relief=tk.RIDGE) #, textvariable=bfClass.version)
        self.e0.grid(row=row, column=1, sticky=tk.W)
        self.e0.bind('<KeyRelease>', self.versionClicked)
        
        row = 2
        lbl1 = ttk.Label(top_frame, text="Language", width=10, anchor=tk.W)  #, padx=1,pady=1)
        lbl1.grid(row=row, column=0, sticky=tk.W)
        self.e1 = tk.Entry(top_frame, width=10)  #, textvariable=bfClass.language)
        self.e1.grid(row=row, column=1, sticky=tk.EW)
        self.e1.bind('<KeyRelease>', self.langClicked)

        lbl2 = tk.Label(top_frame, text="Alias",width=4, anchor=tk.W)
        lbl2.grid(row=row, column=2, sticky=tk.E)
        self.e2 = tk.Entry(top_frame, width=3)
        self.e2.grid(row=row, column=3, sticky=tk.W)
        self.e2.bind('<KeyRelease>', self.aliasClicked)

        
        row = 3
        lbl3a = ttk.Label(top_frame, text="Font File", width=8, anchor=tk.W)
        lbl3a.grid(column=0, row=row, sticky=tk.W)   #, columnspan=1)
        self.ttf = tk.Entry(top_frame,width=28)
        self.ttf.grid(column=1, row=row, sticky=tk.W, columnspan=3)
        #ttf.insert(0, bfClass.ttf)
        self.ttf.bind("<1>", self.ttfClicked)
        
        row = 4
        lbl3 = ttk.Label(top_frame, text="SFD File")
        lbl3.grid(column=0, row=row, sticky=tk.W, columnspan=1)
        self.sfd = ttk.Entry(top_frame,width=28)
        self.sfd.grid(column=1, row=row, sticky=tk.W, columnspan=4 )
        self.sfd.bind("<1>", self.sfdClicked)

        row = 5
        lbl4 = tk.Label(top_frame, text="KMN File")
        lbl4.grid(column=0, row=row, sticky=tk.W, columnspan=1)
        self.kmn = tk.Entry(top_frame,width=28)
        self.kmn.grid(column=1, row=row, sticky=tk.W, columnspan=4 )
        #kmn.insert(0, bfClass.kmnFile)
        self.kmn.bind("<1>", self.kmnClicked)

        row = 6
        lbl6 = tk.Label(top_frame, text="TRLang File")
        lbl6.grid(column=0, row=row, sticky=tk.W, columnspan=1)
        self.trl = tk.Entry(top_frame,width=28)
        self.trl.grid(column=1, row=row, sticky=tk.W, columnspan=4 )
        #trl.insert(0, bfClass.trlangFile)
        self.trl.bind("<1>", self.trlClicked)
        
        row = 7
        lbl7 = tk.Label(top_frame, text="Sun Font")
        lbl7.grid(column=0, row=row, sticky=tk.W, columnspan=1)
        self.fnt = tk.Entry(top_frame,width=28)
        self.fnt.grid(column=1, row=row, sticky=tk.W, columnspan=4 )
        self.fnt.insert(0, cfg["sunFontName"])
        #self.trl.bind("<1>", self.trlClicked)
        
        #outputs bottom frame widgets

        row = 1
        disp0 = ttk.Label(bot_frame, text="PW File")
        disp0.grid(row=row, column=0, sticky=W)
        disp0 = ttk.Label(bot_frame, textvariable=self.pwFile)
        disp0.grid(row=row, column=1, sticky=W)
        row = 2
        disp1 = ttk.Label(bot_frame, text="pwLang File")
        disp1.grid(row=row, column=0, sticky=W)
        disp1 = ttk.Label(bot_frame, textvariable=self.langFile)
        disp1.grid(row=row, column=1, sticky=W)
        row = 3
        disp2 = ttk.Label(bot_frame, text="Back Font")
        disp2.grid(row=row, column=0, sticky=W)
        disp2 = ttk.Label(bot_frame, textvariable=self.backFont)
        disp2.grid(row=row, column=1, sticky=W)
        row = 4
        disp3 = ttk.Label(bot_frame, text="kmn_csv File")
        disp3.grid(row=row, column=0, sticky=W)
        disp3 = ttk.Label(bot_frame, textvariable=self.kmncsv)
        disp3.grid(row=row, column=1, sticky=W)
        row = 5
        disp4 = ttk.Label(bot_frame, text="back2doc File")
        disp4.grid(row=row, column=0, sticky=W)
        disp4 = ttk.Label(bot_frame, textvariable=self.back2doc)
        disp4.grid(row=row, column=1, sticky=W)
        row = 6
        disp5 = ttk.Label(bot_frame, text="Compact File")
        disp5.grid(row=row, column=0, sticky=W)
        disp5 = ttk.Label(bot_frame, textvariable=self.compactFile)
        disp5.grid(row=row, column=1, sticky=W)

        self.updateVars()
        
    def updateVars(self, *args):
        print('update vars',cfg["alias"], 'vars updated')
        cfg["sunFontName"] = os.path.basename(cfg["sfdFile"])[:-4]
        updateCfg(cfg)
        CBFrame.setState()
        self.e0.delete(0,tk.END)
        self.e0.insert(0,cfg["version"])
        
        self.e1.delete(0,tk.END)
        self.e1.insert(0,cfg["language"])
        self.e2.delete(0,tk.END)
        self.e2.insert(0,cfg["alias"])
        
        ttfName = os.path.basename(cfg["ttf"])
        self.ttf.delete(0, tk.END)
        self.ttf.insert(0, ttfName)
        sfdName = os.path.basename(cfg["sfdFile"])
        self.sfd.delete(0, tk.END)
        self.sfd.insert(0, sfdName)
        kmnName = os.path.basename(cfg["kmnFile"])
        self.kmn.delete(0, tk.END)
        self.kmn.insert(0, kmnName)
        trlName = os.path.basename(cfg["trlangFile"])
        self.trl.delete(0, tk.END)
        self.trl.insert(0, trlName)
        
        self.fnt.delete(0, tk.END)
        self.fnt.insert(0, sfdName[:-4])
        
        self.pwFile.set(cfg["pwFile"])
        self.langFile.set(cfg["pwLangFile"])
        self.backFont.set(cfg["backFont"])
        self.kmncsv.set(cfg["kmncsv"])
        self.back2doc.set(cfg["back2doc"])
        self.compactFile.set(cfg["compactFile"])
    

class ControlUi:

    def __init__(self, frame):
        self.frame = frame
        self.after = frame.after
        #self.cnt = 0
        #self.frame.height=0
        cBtn2 = tk.Button(self.frame, text="Quit",width=5, height=2,padx=3)
        #cBtn2.grid(row=0,column=0,sticky=tk.W)
        cBtn2.pack(side=tk.LEFT)
        cBtn2.bind("<1>", self.aquit)
     
        cBtn3 = tk.Button(self.frame, text="Clear\nDisplay",width=5,height=2, padx=3)
        #cBtn3.grid(row=0,column=1,sticky=tk.W)
        cBtn3.pack(side=tk.LEFT)
        cBtn3.bind("<1>", ConsoleUi.clearDisp)
        
        self.cBtn4 = tk.Button(self.frame, text="Run",width=5,height=2, padx=3)
        #self.cBtn4.grid(row=0,column=2,sticky=tk.W)
        self.cBtn4.pack(side=tk.LEFT)
        self.cBtn4.config(relief=tk.RAISED)
        self.cBtn4.bind("<ButtonRelease>", self.start)
        
        self.fltrentry = tk.Entry(self.frame, text="unicode list here", width=45)
        self.fltrentry.pack(side=tk.RIGHT)
        self.fltrchkbx = tk.Label(self.frame, text='X', width=1)
        self.fltrchkbx.pack(side=tk.RIGHT)
        self.fltrchkbx.bind("<1>", self.clrFltr)
        self.fltrlabel = tk.Label(self.frame, text="Filter")
        self.fltrlabel.pack(side=tk.RIGHT)
        if cfg["eFilter"]:
            self.fltrentry.insert(0, cfg["eFilter"])
        
    def clrFltr(self, event):
        self.fltrentry.delete(0, tk.END)

    def start(self, event):
        ef = self.fltrentry.get()
        cfg["eFilter"] = ef
        #InputUi.updateVars()
        x = self.cBtn4["state"]

        if not self.cBtn4["state"] == tk.DISABLED:
            print('***** not disabled  ******')
            self.cBtn4.configure(relief=tk.SUNKEN, state=tk.DISABLED)
            rc = CBFrame.runCmds()
            logging.info('run button  %s',rc)
        
            self.cBtn4.configure(relief=tk.RAISED, state=tk.NORMAL)
        else:
            print('**** disabled ****')
 
    def aquit(self, *args):
        print('aquit stop')
        CBFrame.stop()
        self.frame.quit()


class App:

    def __init__(self, root):
        self.root = root
        root.title('SUN Font Utility '+sys.argv[0]+'      '+cfg["bfVersion"])
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # Create the panes and frames
        vertical_pane = ttk.PanedWindow(self.root, orient=VERTICAL)
        vertical_pane.grid(row=0, column=0, sticky="nsew")
        
        horizontal_pane = ttk.PanedWindow(vertical_pane, orient=HORIZONTAL)
        vertical_pane.add(horizontal_pane)
        
        form_frame = ttk.Labelframe(horizontal_pane, text="")
        form_frame.columnconfigure(1, weight=1)
        horizontal_pane.add(form_frame, weight=1)
        
        form_frame1 = ttk.Labelframe(horizontal_pane, text="Commands")
        form_frame1.columnconfigure(1, weight=1)
        horizontal_pane.add(form_frame1, weight=1)

        console_frame = ttk.Labelframe(horizontal_pane, text="Console")
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        horizontal_pane.add(console_frame, weight=1)
        
        control_frame = ttk.Labelframe(vertical_pane, text="Control")
        vertical_pane.add(control_frame, weight=1)
 
        # Initialize all frames
        self.Input = InputUi(form_frame)
        self.Cbf = CBFrame(form_frame1)
        #self.Cbf.start()
        
        self.console = ConsoleUi(console_frame)
        self.control = ControlUi(control_frame)
        
         # Create textLogger
        logging.= logging.getlogging.)
        guiHandler = self.console
        guiHandler.setFormatter(CustomFormatter())
        logging.addHandler(guiHandler)
        logging.setLevel(logging.DEBUG)
        logging.info('version %s', cfg["bfVersion"])    
        

        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.root.bind('<Control-q>', self.quit)
        signal.signal(signal.SIGINT, self.quit)

    def quit(self, *args):
        print('quit called')
        self.root.destroy()

def main():
    lgh = setLogFile('Log/'+__file__[:-3]+'.log')  
    root = tk.Tk()
    app = App(root)
    app.root.mainloop()
    #closeLogFile(lgh)

if __name__ == '__main__':
    main()
