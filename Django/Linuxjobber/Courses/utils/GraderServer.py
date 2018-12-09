#!/usr/bin/python
#
VERSION = "v2.0"
#
import sys,os,shutil
import time
import logging
import logging.config
from datetime import date, timedelta
import socket
import pickle
import subprocess
import MySQLdb
import ConfigParser
import multiprocessing
import requests
import pwd
import grp
import json
import tarfile


# Define important global variables
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lab_id = UserID = 0
qery1 = 0
lab_tp, noposting = ussr = passwd = dbname = ip = PORT = admin_email = git_url = posting_address = service_user = comm_md = host_mode = ntLoc = "LINUX", ""
packList = {}


# Obtain the working directory and the required directories
WORKING_DIR = os.path.abspath(os.path.join(os.getcwd(), os.path.dirname(sys.argv[0])))
CONF_DIR = ("%s/conf" % WORKING_DIR)
LOGS_DIR = ("%s/logs" % WORKING_DIR)
if not os.path.isdir(CONF_DIR): sys.exit("Configuration directory missing")
if not os.path.isdir(LOGS_DIR): os.makedirs(LOGS_DIR)

# obtain machine Private IP
DEV_IP = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

# Load and define the application configuration
parser = ConfigParser.SafeConfigParser()
gn_conf = "%s/genconf.ini" % CONF_DIR
lg_conf = "%s/logging.ini" % CONF_DIR
db_conf = "%s/db.ini" % CONF_DIR
for fl in [gn_conf,lg_conf,db_conf]:
    if not os.path.isfile(fl):
        sys.exit("A configuration file ( %s ) is missing!! Provide it and try again" % fl)
    # <------ LOGGING ------> 
logging.LOG_FILE = ("%s/graderserver.log" % LOGS_DIR)
logging.config.fileConfig(lg_conf)
logger = logging.getLogger("grader_server")
extra = {'VERSION':VERSION}
logger = logging.LoggerAdapter(logger,extra)
# <------ GENERAL ------> 
gc = open(gn_conf,'r')
parser.readfp(gc)
try:
    PORT,admin_email,posting_address,service_user,comm_md,host_mode,ntLoc = int(parser.get('app_management', 'port')),parser.get('app_management', 'admin_email'), parser.get('app_management', 'def_posting_address'), parser.get('app_management', 'service_user'), parser.get('repo_admin', 'comm_mode'), parser.get('repo_admin', 'host_mode'), parser.get('repo_admin', 'nt_loc')
    try:
        git_url = parser.get('repo_comm_%s' % comm_md, 'url')
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as uerror:
        logger.debug("repo communication data not properly set! url not provided, using default!")
        git_url = parser.get('repo_admin', 'def_url') if "ssh" in parser.get('repo_admin', 'comm_mode') else parser.get('repo_admin', 'defh_url')
except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as error:
    logger.debug("Terminating startup due to the following error:: %s" % error)
    sys.exit("%s in the general config file" % error)
if "_nothing" in ntLoc or not os.path.isdir(ntLoc):
    logger.debug("The notes location wasn't provided or provided path doesn't exist. Using current directory")
    ntLoc = WORKING_DIR
gc.close()
    # <------ DB ------> 
dbf = open(db_conf,'r')
parser.readfp(dbf)
try:
    ussr,passwd,dbname,ip = parser.get('credentials', 'user'), parser.get('credentials', 'password'), parser.get('credentials', 'dbname'), parser.get('credentials', 'dbip')
except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as error:
    logger.debug("Terminating startup due to the following error:: %s" % error)
    sys.exit("%s in the database config file" % error)
dbf.close()

#
#    Ensure the log files are still writeable by the service_user
#
uid = pwd.getpwnam(service_user).pw_uid
gid = grp.getgrnam(service_user).gr_gid
os.chown("%s/graderserver.log" % LOGS_DIR, uid, gid)
## ---- CleanUp logs --- ##
###    Delete logs older than 3days
now = time.time()
for f in os.listdir(LOGS_DIR):
    f = os.path.join(LOGS_DIR, f)
    if os.stat(f) < 3 * 86400 and os.path.isfile(f):
        os.remove(f)

#####    Data validator    #####
def validate(kd,ty,dt):
    return True


#####    Command executor for Python Labs    #####
def execPyCmd(cmds):
    result = {}
    global ptpack
    try:
        versCheck = subprocess.check_output("python3 -V",shell=True,stderr=subprocess.STDOUT,bufsize=-1).strip()
        ptpack = "python3" if "command not found" not in versCheck and versCheck.startswith("Python ") else "python2"
    except Exception as error:
        logger.info("Using python2 to grade student as python3 wasn't found due to {}".format(error))
        ptpack = "python2"
    for task_id, (xptd,codde) in cmds.items():
        try:
            proc = subprocess.Popen(codde.replace("python~",ptpack),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=-1)
            proc.wait()
            streamdata, error_obt = proc.communicate()
            logger.debug("grading-script execution for task (%i) finished with returncode %i\nerror: %s" % (task_id,proc.returncode,error_obt))
            task_reslt = [x for x in streamdata.split("\n") if x ]
            cmd_result = "passed!" if xptd in streamdata else "failed!" if ( error_obt == "" or None ) else "failed! And there was an error:\n%s\n" % error_obt
            ## explanation contains list entries in task_reslt before "Overall; " is found (if len(task_reslt)>1 or just task_reslt.replace"Overall; " with "" ); and overall contains the entries from_and including "Overall; " (if len(task_reslt)>1 or just task_reslt.replace"Overall; " with "" )
            result[task_id] = {"status":cmd_result,"explanation":[x.replace("Overall; ","") for x in task_reslt if x] if len(task_reslt) == 1 else task_reslt[:next((i for i, string in enumerate(task_reslt) if "Overall; " in string),-1)],"overall": [next(x.replace("Overall; ","") for x in task_reslt if x)] if len(task_reslt) == 1 else "\n".join(task_reslt[next(i for i, string in enumerate(task_reslt) if "Overall; " in string):]).replace("Overall; ","").replace("; ","\n").split("\n")}
            ## explanation contains list entries in task_reslt before "Overall; " is found (if len(task_reslt)>1 or just task_reslt.replace"Overall; " with "" ); and overall contains the entries(as a String) from_and including "Overall; " (if len(task_reslt)>1 or just task_reslt.replace"Overall; " with "" )
#             result[task_id] = {"status":cmd_result,"explanation":[x.replace("Overall; ","") for x in task_reslt if x] if len(task_reslt) == 1 else task_reslt[:next((i for i, string in enumerate(task_reslt) if "Overall; " in string),-1)],"overall":next(x.replace("Overall; ","") for x in task_reslt if x) if len(task_reslt) == 1 else "\n".join(task_reslt[next(i for i, string in enumerate(task_reslt) if "Overall; " in string):]).replace("Overall; ","")}
            ## old computation ---- explanation includes the whole output, and overall is empty if length of task_result not == 1
#             result[task_id] = {"status":cmd_result,"explanation":[x.replace("Overall; ","") for x in task_reslt if x] if len(task_reslt) == 1 else task_reslt[:-1],"overall":task_reslt[-1] if len(task_reslt) == 1 else ""}
        except Exception as e:
            logger.debug("An exeception encountered: ({})".format(e))
    return result

#####    Handler for Python Labs    #####
def python_handle(typ,user_id,lab_no,labname,username):
    global error_obt,comoutput
    error_obt = comoutput = ""
    user_dirname = username.split("@")[0]
    if not os.path.isdir("%s/remote_lab_files/%s" % (ntLoc,labname)):
        os.makedirs("%s/remote_lab_files/%s" % (ntLoc,labname))
    os.chdir("%s/remote_lab_files/%s" % (ntLoc,labname))
    try:
        if not os.path.isdir("%s/.git" % os.getcwd()):
            subprocess.call("git init .",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=-1)
        is_ini = subprocess.check_output("git remote show",shell=True,stderr=subprocess.STDOUT,bufsize=-1)
        if not "origin" in is_ini:
            prcss = subprocess.Popen("git remote add origin %s" % git_url,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=-1)
            prcss.wait()
            comoutput, error_obt = prcss.communicate()
        if (error_obt == "" and comoutput == "" or "already exists" in comoutput):
            logger.info("repo already exists or has been created")
            try:
                outputs = subprocess.check_output("git fetch origin",shell=True,stderr=subprocess.STDOUT,bufsize=-1)
                logger.debug("fetch result:->> %s" % outputs)
                fetch_query = subprocess.Popen("git checkout origin/%s -- %s" % (labname,user_dirname),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=-1)
                logger.debug("Data fetch from repo has completed!! Error::->> %s" % fetch_query.communicate()[1])
            except Exception as exce:
                logger.debug("Error encountered while fetching data from repo::--> ({})".format(exce))
                js = {'userID':user_id,'lab_id':lab_no,'error_status':"Error encountered while fetching data from repo:--> ({})".format(exce)}
                do_some_stuffs_with_input(js, username)
            if not os.path.isdir(user_dirname):
                logger.debug("Could not find data for user-( %i ) on lab-> %s" % (user_id,labname))
                js = {'userID':user_id,'lab_id':lab_no,'error_status':"Could not find data for user-( %i ) on lab-> %s" % (user_id,labname)}
                do_some_stuffs_with_input(js, username)
            else:
                os.chdir(user_dirname)
                result = execPyCmd(fetch_instrct(typ, lab_no))
                logger.debug("<-------- lab(%i) result for user with ID: %i and repo login: %s -------->\n<-------- result: %s -------->" % (lab_no,user_id,username,result))
                result['userID'] = user_id
                result['lab_id'] = lab_no
                do_some_stuffs_with_input(result, username)
            os.chdir("%s/remote_lab_files/%s" % (ntLoc,labname))
            if os.path.isdir(user_dirname):
                with tarfile.open(user_dirname + '_' + time.strftime("%Y-%m-%d_%H_%M_%S") + '.tar.gz', mode='w:gz') as archive:
                    archive.add(user_dirname)
                shutil.rmtree(user_dirname)
        else:
            logger.debug("Something went wrong as I wasn't able to access the repo\nError encountered:=> %s" % error_obt)
            js = {'userID':user_id,'lab_id':lab_no,'error_status':"Something went wrong as I wasn't able to access the repo\nError encountered:=> %s" % error_obt}
            do_some_stuffs_with_input(js, username)
    except Exception as e:
        logger.debug("A great Wahala!! Here it is---> ({})".format(e))
        js = {'userID':user_id,'lab_id':lab_no,'error_status':"Something went wrong as git initialization failed"}
        do_some_stuffs_with_input(js, username)

#####    Handler for Linux Labs    #####
def handle(connection, address,MAX_BUFFER_SIZE = 4096):
    try:
        logger.debug("Connection ( %r ) established at %r", connection, address)
        while True:
            data = pickle.loads(connection.recv(MAX_BUFFER_SIZE))
            if data == "":
                logger.info("<-------- no data received from host: %s -------->" % address[0])
                logger.info("Socket closed remotely")
                break
            elif 'jquit' in data:
                logger.info("<-------- no data received from host: %s -------->" % address[0])
                logger.info("Remote system sent an EOF")
                break
            elif 'l_ID' in data:
                lab_id = data['l_ID']
                logger.debug("<-------- LabID ( %i ); for labType ( %s ) received from client: %s -------->" % (lab_id,lab_tp,address[0]))
                if lab_tp != "LINUX":
                    logger.debug("<-------- Somehow, client: %s attempted fetching Lab (%i), for invalid labType (%s) -------->" % (address[0],lab_id,lab_tp))
                    break
                instructs = fetch_instrct(lab_tp,lab_id)
                logger.debug("<-------- Sending system instructions fetched to client: %s -------->" % address[0])
                connection.send(pickle.dumps(instructs))
            else:
                UserID = data.pop('UserID')
                logger.debug("<-------- result for user with ID: %d received from client: %s -------->\n<-------- result: %s -------->" % (UserID,address[0],data))
                data['userID'] = UserID
                data['lab_id'] = lab_id
                do_some_stuffs_with_input(data,address[0])
    except:
        logger.exception("Problem handling request")
    finally:
        logger.debug("Closing socket")
        connection.close()

#### ServerObject to be used by chuckService ####
class Server:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        logger.info("<-------- socket created -------->")
        self.socket.bind((self.hostname, self.port))
        logger.debug("<-------- Socket bind complete on device. IP: %s, PORT: %s -------->" % (self.hostname, self.port))
        #Start listening on socket
        self.socket.listen(5)
        logger.debug("<-------- Socket now listening on PORT: %s -------->" % self.port)
        while True:
            conn, address = self.socket.accept()
            logger.debug("<-------- Got connection ( %s ) from a client with details: %s -------->" % (conn, address))
            process = multiprocessing.Process(target=handle, args=(conn, address))
            process.daemon = True
            process.start()
            logger.debug("Started process %r for client: %s" % (process,str(address[0])))


##### fetch instructions from db #####
def fetch_instrct(ltyp,idd):
    logger.info("<-------- Fetching system instructions for lab with type %s; ID %i -------->" % (ltyp,idd))
    db = MySQLdb.connect(ip,ussr,passwd,dbname)
    cursor = db.cursor()
    #qery1 = "SELECT task,task_id,instruction FROM labmap_contents WHERE labmap_id = '%d'" % (idd) if ltyp == "LINUX" else "SELECT xpected,task_id,instruction FROM python_labs WHERE lab_id = '%d'" % (idd)
    qery1 = "SELECT task, task_number, instruction FROM Courses_labtask WHERE lab_id = '%d'" % (idd) 
    try:
        commands = {}
        cursor.execute(qery1)
        instrs = cursor.fetchall()
        for i in instrs:
            tsk = i[0].strip() if ltyp == "PYTHON" else "requires root" if "Obtain root privilege" in i[0] else "adminKnows" # make sure to delete the initial split if the data isn't going to be entered from admin portal.
            tid = i[1]
            cmm = i[2].strip()
            commands[tid] = [tsk,cmm]
        db.close()
        return commands
    except Exception as e:
        logger.debug("Unable to fetch Instructions! Error: ({})".format(e))


#####    send result to server or site    #####
def do_some_stuffs_with_input(inf,remoteAdd):
    global posting_address
    pgc = open(gn_conf,'r')
    parser.readfp(pgc)
    labt = lab_tp.lower()[0:2]
    try:
        posting_address = parser.get('app_management', '%s_posting_address' % labt)
    except ConfigParser.NoOptionError:
        pass
    logger.debug("<-------- cascading result for user: %i, machine (%s) to calling process -------->" % (inf['userID'],remoteAdd) if noposting == "tt" else "<-------- posting result for user: %i, machine (%s) to %s -------->" % (inf['userID'],remoteAdd,posting_address))
    logger.info("Cascade successful" if noposting == "tt" else "Successful posting!!" if requests.post(posting_address,inf).status_code == 200 else "Posting unsuccessful")
    if noposting == "tt": print("%s" % json.dumps(inf))
    

#########################
######    START    ######
#########################

if __name__ == "__main__":
    ##### SECTION LINUX LABS #####
    
    #logger.info(sys.argv[0])
    if len(sys.argv) == 1:
        server = Server(DEV_IP, PORT)
        try:
            logger.info("<--------------> starting socket <-------------->")
            server.start()
        except Exception as e:
            logger.exception("Unexpected exception occurred: ({})".format(e))
        finally:
            logger.info("Shutting down")
            for process in multiprocessing.active_children():
                logger.info("Shutting down process %r", process)
                process.terminate()
                process.join()
    elif len(sys.argv) == 6:
        ##### SECTION PYTHON LABS #####
        lab_tp, noposting, UserID, lab_id, lab_nm, git_user = "PYTHON", sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
        logger.info("<--------------> starting to grade python labs for user {id: %s} <-------------->" % UserID)
        for i in sys.argv:
            sys.exit("Data: '%s' passed in is invalid!" % i) if not validate("kd", "ty", i) else None
        try:
            python_handle(lab_tp,UserID,lab_id,lab_nm,git_user)
        except Exception as e:
            logger.debug("Something terrible happened!\n Exception:: ({})".format(e))
        finally:
            logger.info("Closing shop!")
    else:
        logger.info("Invalid number of parameters in call\nEXPECTED SYNTAX::\n\tGraderServer.py [tt | anythingElse] {UserId} {LabId} {RepoName} {UserEmail}")
