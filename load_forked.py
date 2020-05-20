#!/usr/bin/env python

"""

basic structure I use to build packages

"""

import sys
if sys.version[0:3] < '2.6':
    print "Python version 2.6 or greater required (found: %s)." % \
        sys.version[0:5]
    sys.exit(-1)


import math, os, pprint, re, shlex, shutil, socket, stat, time
from shutil import copyfile
from datetime import datetime
from signal import alarm, signal, SIGALRM, SIGKILL, SIGTERM
from subprocess import Popen, PIPE, STDOUT
import argparse
from ConfigParser import RawConfigParser
from process_commands import process_commands
import json

#---- Gobal defaults ---- Can be overwritten with commandline arguments 

SOME_TEXT="this is a test"
TIME_TO_NOTIFY = 10
NDEEP=2

#----------------------------------------

class load_forked:
    """ application class """

    def __init__(self, args):
        self.args = args
        self.ndeep = args.ndeep
        self.some_text = args.some_text
        self.proc_c = process_commands(args.verbosity)

#------------------------
    def _unixT(self):
        return int(time.mktime((datetime.now()).timetuple()))

#-----------------------------------

    def f(self,x):
        icount=-5000000
        while icount < 5000000:
            x*x
            icount+=1


#-----------------------------------

    def get_utime(self,o):

        ar=o.split(" ")
        for item in ar:
            if "elapsed" in item:
                y = item.replace("elapsed",'')
                return y
        return "not found"


#-----------------------------------

#-----------------------------------
    def go(self):

#       A tally for keeping count of various stats
        tally = dict(pico_cp_tries=0, pico_cp_succ = 0, pico_cp_fail = 0, 
                    hpss_tries = 0, hpss_succ = 0, hpss_fail =0)
        self.proc_c.log("depth = %d" % (self.ndeep), 0)
        
       # cmd="time /osg_nodes/aliprod/bin/load_cpu.py"
        cmd="time ./load_cpu.py"

        for i in range(self.ndeep):
            print '**********%d***********' % i
            pid = os.fork()
            if pid == 0:
                # We are in the child process.
                print "%d (child) just was created by %d." % (os.getpid(), os.getppid())
                s, o, e = self.proc_c.comm(cmd)
                ut=self.get_utime(o)
                print "output = %s, elapsed time= %d in process=%d" % (ut, e, os.getpid()) 
            else:
                # We are in the parent process.
                print "%d (parent) just created %d." % (os.getpid(), pid)
                if i == 0:
                    print "will run f directly"
                    self.f(3.3)
                else: 
                    print "will run command"
                    s, o, e = self.proc_c.comm(cmd)
                    ut=self.get_utime(o)
                    print "output = %s, elapsed time= %d in process=%d" % (ut, e, os.getpid())
                os.wait()


def main():
    """ Generic program structure to parse args, initialize and start application """
    desc = """ prepare files for transfer """
    
    p = argparse.ArgumentParser(description=desc, epilog="None")
    p.add_argument("--some-text",dest="some_text",default=SOME_TEXT,help="some test like file or directory name")

    p.add_argument("--time-to-notify",dest="time_to_notify",default=TIME_TO_NOTIFY,help="how frequent to email notice")
    p.add_argument("-v", "--verbose", action="count", dest="verbosity", default=0,                                                                                                 help="be verbose about actions, repeatable")
    p.add_argument("--config-file",dest="config_file",default="None",help="override any configs via a json config file")
    p.add_argument("-n",action="count",dest="ndeep",default=NDEEP,help="how deep do the forks go")


    args = p.parse_args()

#-------- parse config file to override input and defaults
    val=vars(args)
    if not args.config_file == "None":
        try:
            print "opening ", args.config_file
            with open(args.config_file) as config_file:
                configs=json.load(config_file)
            for key in configs:
                if key in val:
                    if isinstance(configs[key],unicode):
                        val[key]=configs[key].encode("ascii")
                    else:
                        val[key]=configs[key]
        except:
            p.error(" Could not open or parse the configfile ")
            return -1

    try:
        myapp = load_forked(args)
        return(myapp.go())
    except (Exception), oops:
        if args.verbosity >= 2:
            import traceback
            traceback.print_exc()
        else:
            print oops
            return -1
                                                                                                                                                                
if __name__ == "__main__":                      
    sys.exit(main())


