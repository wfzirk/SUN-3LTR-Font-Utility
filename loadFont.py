#
# https://stackoverflow.com/questions/57909525/how-do-i-close-a-file-opened-using-os-startfile-python-3-6


import os
import sys
import subprocess
#import psutil
import time
import logging
from bfLog import log_setup
import threading
'''
class loadFontThrd(threading.Thread):

    def __init__(self, cmd,
                 group=None, name=None, daemon=True):
        super().__init__(group=group, name=name, daemon=daemon)

        self.cmd = cmd
        self._stop = threading.Event()
        
    def run(self):
        logging.info('process started')
        self.process = subprocess.Popen(self.cmd, shell=False)
        print('running', self.process.runcode)


    def stop(self):
        #logging.debug('stop called')
        # request the thread to exit gracefully during its next loop iteration
        self._stop.set()
'''
'''
# https://stackoverflow.com/questions/57909525/how-do-i-close-a-file-opened-using-os-startfile-python-3-6
class xloadFontThrd(threading.Thread):

    def __init__(self, font,
                 group=None, name=None, daemon=True):
        super().__init__(group=group, name=name, daemon=daemon)


        self.cmd = ["fontloader.exe", font]
        #self._stop = threading.Event()
        
    def run(self):
        logging.info('process started')
        self.shell_process = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True) 
        logging.info('process pid %s',self.shell_process.pid)
        #parent = psutil.Process(self.shell_process.pid)
        #while(parent.children() == []):
        #    continue
        #children = parent.children()
        #logging.info('children %s',children)
        #child_pid = children[0].pid
        #logging.info('child pid %s',child_pid)

    def stop(self):
        #logging.debug('stop called')
        # request the thread to exit gracefully during its next loop iteration
        #self._stop.set() 
        logging.info('stop called')
        self.shell_process.stdin.write(b'x')
        logging.info('write stdin')
        self.shell_process.stdin.flush()
        #subprocess.check_output("Taskkill /PID %d /F" % self.shell_process.pid)
'''
 
# https://stackoverflow.com/questions/57909525/how-do-i-close-a-file-opened-using-os-startfile-python-3-6
class loadFontThrd(threading.Thread):

    def __init__(self, font,
                 group=None, name=None, daemon=True):
        super().__init__(group=group, name=name, daemon=daemon)

        self.font = font
        self.cmd = ["fontloader.exe", self.font]
        self._stop = threading.Event()
        self._start = threading.Event()
        
    def run(self):
        logging.info('process started %s',self.cmd)
        self.shell_process = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True) 
        #self.shell_process = subprocess.Popen(self.cmd,  shell=True)
        logging.info('process pid %s',self.shell_process.pid)

    def stop(self):
        logging.info('stop called')
        self.shell_process.stdin.write(b'x')
        logging.info('write stdin')
        #self.shell_process.stdin.flush()
        #subprocess.check_output("Taskkill /PID %d /F" % self.shell_process.pid)

 
if __name__ == "__main__":
    
    #lf = loadFontThrd(["fontloader.exe", "sun7_7_519.ttf"]) 
    lf = loadFontThrd("sun7_7_519.ttf") 
    lf.run()
    logging.info('xalive? %s',lf.is_alive())
    time.sleep(5)
    logging.info('alive? %s',lf.is_alive())
    lf.stop()
    logging.info('1alive? %s',lf.is_alive())
    #lf.join()
    #logging.info('2alive? %s',lf.is_alive())
    time.sleep(1)
    del lf
    #sys.exit(0)
    #shellprocess(["fontloader.exe", "sun7_7_519.ttf"]) 
    time.sleep(20)
    logging.info('done')
    sys.exit(0)
    