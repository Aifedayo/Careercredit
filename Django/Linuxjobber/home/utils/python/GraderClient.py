#!/bin/python
#
VERSION = "v1.2"
#
import sys
import os
import time
import subprocess
import socket
import logging
import pickle
import logging.config
from datetime import date, timedelta
import traceback
import pwd
import grp

# Obtain the working directory and the required directories
WORKING_DIR = os.path.abspath(os.path.join(os.getcwd(), os.path.dirname(sys.argv[0])))
CONF_DIR = ("%s/conf" % WORKING_DIR)
LOGS_DIR = ("%s/logs" % WORKING_DIR)
if not os.path.isdir(CONF_DIR): sys.exit("Configuration directory missing")
if not os.path.isdir(LOGS_DIR): os.makedirs(LOGS_DIR)
if not os.path.isfile("%s/logging.ini" % CONF_DIR): sys.exit("The logging configuration file ( logging.ini ) is missing!! Provide it and try again")
logging.LOG_FILE = ("%s/graderclient.log" % LOGS_DIR)
logging.config.fileConfig("%s/logging.ini" % CONF_DIR)
logger = logging.getLogger("grader_client")
extra = {'VERSION':VERSION}
logger = logging.LoggerAdapter(logger,extra)
#
#    Ensure the log files are still writeable by the service_user
#
uid = pwd.getpwnam(sys.argv[1]).pw_uid
gid = grp.getgrnam(sys.argv[1]).gr_gid
os.chown("%s/graderclient.log" % LOGS_DIR, uid, gid)


SERV_IP = ""
PORT = 58500
LAB = 0
UserID = 0
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
global keep_commune
keep_commune = True
global user_, user_hdir


def send_reslt(filnm):
    # function to handle sending user's result
    logger.info("<-------- sending result for LINUX lab { id = %i } to host: %s -------->" % (LAB,SERV_IP))
    soc.send(pickle.dumps(filnm))
    logger.debug("<-------- result for lab sent -------->")

def executeCmd(cmdd):
    try:
        cmd_result = ""
        proc = subprocess.Popen(cmdd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=-1)
        proc.wait()
        streamdata, error_obt = proc.communicate()
        logger.debug("command execution finished with returncode %s, and resulting data: %s; error: %s." % (proc.returncode,streamdata,error_obt))
        cmd_result = "passed" if "true" in streamdata else "failed"
        return cmd_result
    except Exception as e:
        logger.debug("An exeception encountered: ({})".format(e))


def main():
    os.chdir(user_hdir)
    logger.info("<------> connecting to server socket <------->")
    logger.info(SERV_IP)
    logger.info(PORT)
    soc.connect((SERV_IP, PORT))
    soc.send(pickle.dumps({"l_ID" : LAB}))
    logger.info("<------ connected to socket and requested lab instructions ------>")
    try:
        global keep_commune
        while keep_commune:
            received_bytes = soc.recv(4096)
            if received_bytes:
                logger.debug("<-------- data received from host: %s; it must be instructions!! -------->" % SERV_IP)
                recceived = pickle.loads(received_bytes)
                if bool(recceived):
                    result = {}
                    global path
                    result['UserID'] = UserID
                    path = ("{/root,%s}" % user_hdir) if True in ["requires root" in x for v in recceived.values() for x in v] else user_hdir
                    for task_id, (_,codde) in recceived.items():
                        command = codde.replace('~/',"%s/" %path)
                        result[task_id] = executeCmd(command)
                    send_reslt(result)
                    keep_commune = False
            else:
                logger.debug("<-------- no data received from host: %s -------->" % SERV_IP)
                soc.send(pickle.dumps({"jquit":0}))
                soc.close()
            soc.send(pickle.dumps({"jquit":0}))
            soc.shutdown(socket.SHUT_RDWR)
            soc.close()
    except Exception as e:
        logger.debug("I encountered an unexpected error: ({})".format(e))
        traceback.print_exc()


if __name__ == '__main__':
    SERV_IP = sys.argv[2]
    LAB = int(sys.argv[3])
    UserID = int(sys.argv[4])
    try:
        usr_inf = sys.argv[1]
        user_hdir = os.path.expanduser("~"+usr_inf)
        logger.info("Found home directory for the user (%s)" %sys.argv[1] if os.path.isdir(user_hdir) else "%s's home directory doesn't exist")
#         kill_em_all = 0
        kill_em_all = subprocess.check_call("for act in `w | grep \"%s\" | awk '{print $2}'`;do sudo kill -9 `awk '{print $1}' <<< \"$(ps -dN | grep \"$act\")\"`;done" % sys.argv[1],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=-1)
        (logger.info("All current instances of user logged off"),main()) if kill_em_all == 0 else logger.info("Cannot proceed! Couldn't log the user out!")
    except Exception as e:
        logger.debug("Client startup process failed!\n Error: {}".format(e))
