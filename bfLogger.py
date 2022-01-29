
# https://stackoverflow.com/questions/15727420/using-logging-in-multiple-modules
# https://stackoverflow.com/questions/1343227/can-pythons-logging-format-be-modified-depending-on-the-message-log-level
import logging
import logging.handlers


# https://stackoverflow.com/questions/1343227/can-pythons-logging-format-be-modified-depending-on-the-message-log-level


BFLOG = 25
logging.addLevelName(BFLOG, 'BFLOG')

class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    FORMATS = {
        logging.ERROR: "ERROR: %(msg)s",
        logging.WARNING: "WARNING: %(msg)s",
        logging.DEBUG: "DBG: %(module)s: %(lineno)d: %(msg)s",
        "DEFAULT": "%(msg)s",
        #logging.BFLOG: "%msg)s",
    }

    def xformat(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS['DEFAULT'])
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
    
    def format(self, record):
        #log_fmt = self.FORMATS.get(record.levelno)
        #formatter = logging.Formatter(log_fmt)
        formatter = logging.Formatter('%(asctime)s %(levelname)6s %(module)8s:%(lineno)d - %(message)s')
   
        return formatter.format(record)
        
# create logger with script name
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

glbloglvl = logging.INFO
def chgLogLevel(level):
    global glbloglvl
    print('level ', level, glbloglvl)
    
    glbloglvl = logging.DEBUG
    
    #listLoggers()
    '''
    logger = logging.getLogger()
    for handler in logger.handlers:
        #    if isinstance(handler, type(logging.StreamHandler())):
        handler.setLevel(logging.level)
        logger.debug('Debug logging enabled')
    
    listLoggers()
    '''

def setLogFile(name):

    pr = logging.FileHandler(name, mode='w')
    er = logging.FileHandler(name[:-4]+'.err', mode='w')
    dbg = logging.FileHandler(name[:-4]+'.dbg', mode='w')
    pr.setLevel(logging.INFO)
    pr.setFormatter(CustomFormatter())
    er.setLevel(logging.ERROR)
    er.setFormatter(CustomFormatter())
    dbg.setLevel(logging.DEBUG)
    dbg.setFormatter(CustomFormatter())
    logger.addHandler(er)
    logger.addHandler(pr)
    logger.addHandler(dbg)
    
    #listLoggers()
    
    return pr
    
def closeLogFile(prh):
    #print('closelogfile')
    logger.removeHandler(prh)

    
def closeLoggers():
    x = logging._handlers.copy()
    print('*** closeloggers ***',x)
    for i in x:
        print('^^^remove^^^',i)
        log.removeHandler(i)
        i.flush()
        i.close()

def listLoggers():

    #logging.getLogger().removeHandler(logging.getLogger().handlers[0])
    print(logging.getLogger().handlers)
    print('ll',logging.getLogger('bfLogger'))

    print('***listLoggers***')
    print (logging.Logger.manager.loggerDict.keys())
    #print(logging.getLogger().handlers[0])
    rootlogger = logging.getLogger()
    print(rootlogger)
             
    for h in rootlogger.handlers:
        print('h    %s' % h)
    for nm, lgr in logging.Logger.manager.loggerDict.items():   
        print('+ [%-20s] %s ' % (nm, lgr))
        if not isinstance(lgr, logging.PlaceHolder):
            for h in lgr.handlers:
                print('x     ', h)
               
                    
