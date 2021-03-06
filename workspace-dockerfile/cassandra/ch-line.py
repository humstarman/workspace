#!/usr/bin/python

import os
import sys
from optparse import OptionParser
import logging  
import logging.handlers  
import time
 
def set_logger():
    name = sys.argv[0].strip().split(r"/")[-1].strip().split('.')[0]
    LOG_DIR=options.LD
    LOG_FILE = os.path.join(LOG_DIR,"%s.log" % name)
    logger = logging.getLogger("%s" % name)

    logger.setLevel(logging.INFO)
    if options.LL.upper() in ["DEBUG",]:
        logger.setLevel(logging.DEBUG)       
    elif options.LL.upper() in ["INFO",]:
        logger.setLevel(logging.INFO) 
    elif options.LL.upper() in ["WARN","WARNING"]:
        logger.setLevel(logging.WARN)  
    elif options.LL.upper() in ["ERROR",]:
        logger.setLevel(logging.ERROR)  
    elif options.LL.upper() in ["CRITICAL",]:
        logger.setLevel(logging.CRITICAL)  
    else:
        pass
    
    #fh = logging.FileHandler(LOG_FILE)
    fh = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) 
    ch = logging.StreamHandler()  
    
    #fmt = "%(asctime)s-%(name)s-%(levelname)s-%(message)s-[%(filename)s:%(lineno)d]"
    fmt = '%(asctime)s - %(name)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)

    fh.setFormatter(formatter)   
    ch.setFormatter(formatter)

    logger.addHandler(fh)   
    logger.addHandler(ch)

    return logger

def parse_opts(parser):
    parser.add_option("-f","--file",action="store",type="string",dest="file",default="",help="the file to change")
    parser.add_option("-1","--from",action="store",type="string",dest="f",default="",help="change line from")
    parser.add_option("-2","--to",action="store",type="string",dest="t",default="",help="change line to")
    parser.add_option("-m","--mod",action="store",type="string",dest="m",default="g",help="the mode of replacement")
    parser.add_option("--ll",action="store",type="string",dest="LL",default="INFO",help="the log level")
    parser.add_option("--log_dir",action="store",type="string",dest="LD",default=r"/tmp",help="the dir to store log")
    parser.add_option("--cll",action="store",type="string",dest="CLL",default="INFO",help="the console log level")
    parser.add_option("--fll",action="store",type="string",dest="FLL",default="DEBUG",help="the file log level")
    (options,args) = parser.parse_args()

    return options

# mk global var: options & logger
options = parse_opts(OptionParser(usage="%prog [options]"))
logger = set_logger()

def timer(func):
    def wrapper(*args,**kwargs):
        t1 = time.time()
        ret = func(*args,**kwargs)
        t2 = time.time()
        logger.debug("Elapsed: %s sec." % (str(t2-t1)))
        return ret
    return wrapper

def do_replace():
    m = int(options.m) if options.m=='1' else options.m
    x = options.f
    y = options.t
    with open(options.file, "r") as f1:
        lines = f1.readlines()

    with open(options.file, "w") as f2:
        n = 0
        if m == 1:
            for line in lines:
                if x in line:
                    line = line.replace(x,y)
                    f2.write(line)
                    n += 1
                    break
                f2.write(line)
                n += 1
            for i in range(n,len(lines)):
                f2.write(lines[i])
        elif m == 'g':
            for line in lines:
                if x in line:
                    line = line.replace(x,y)
                f2.write(line)
        else: logger.error("Wrong mod, use -m/--mod to specify.")

@timer
def main():
  logger.info("Change from: %s;" % options.f)  
  do_replace()
  logger.info("To: %s." % options.t)  

if __name__ == "__main__":
    main()
