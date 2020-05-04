#!/usr/bin/python

import ConfigParser
import ast
import sys
import os, shutil
from email.parser import Parser


#############################################################
#
# email_lab_reports.py 
# run this script without any arguments. It will read config file for values
#
# This file will pull the student's lab reports and send it to the site admin
#  and the specified instructor
#
#############################################################

#
# edit this: set location where you wish to put the configuration file
#
#CONFIG_FILE = '/tools/tool/students.ini'
CONFIG_FILE = '/home/linuxjobber/tools/students.ini'
CONFIG_FILE = 'students.ini'
REPORTS_HOME = '/tools/tool/reports'

################## Do not edit below this line  #######################

def stripDot( username):
#    username = username.replace (".","")
    return username

parser = ConfigParser.SafeConfigParser()
parser.read( CONFIG_FILE)

fundamentalsStudents = ast.literal_eval( parser.get('classroom','FUNDAMENTALS'))
proficiencyStudents = ast.literal_eval( parser.get('classroom','PROFICIENCY'))
onPremStudents = ast.literal_eval( parser.get('classroom','ONPREM'))
instructors = ast.literal_eval( parser.get('classroom','INSTRUCTORS'))

for student in fundamentalsStudents:
    studentEmail= student
    studentUsername = stripDot( student.split("@")[0])

    MSG = """export LJUMAIL=%s && export LJUNAME=%s  && for i in {1..9}; do echo '=============  LAB '$i'  ============='; %s/daily.py 1 k all | grep %s | grep LinuxFundamentalsLab_$i | ack --passthru 'failed'; done | mutt -s 'Current Fundamentals Lab Report for %s ' -- showpopulous@gmail.com folay1881@yahoo.com jeremiahchukwu@gmail.com %s"""  % ( studentEmail, studentUsername, REPORTS_HOME, studentUsername, studentUsername, studentEmail)

    print ("======= running the following command under Fundamentals:")
    print (MSG)

    os.system( MSG)

for student in proficiencyStudents:
    studentEmail= student
    studentUsername = stripDot( student.split("@")[0])

    MSG = """export LJUMAIL=%s && export LJUNAME=%s && for i in {1..17}; do echo '=============  LAB '$i' ============='; %s/daily.py 1 k all | grep %s | grep  LinuxProficiencyLab_$i | ack --passthru 'failed'; done | mutt -s 'Current Proficiency Lab Report for %s ' -- showpopulous@gmail.com folay1881@yahoo.com %s""" % ( studentEmail, studentUsername, REPORTS_HOME, studentUsername, studentUsername, studentEmail)

    print ("======= running the following command under Proficiency:")
    print (MSG)

    os.system( MSG) 

for student in onPremStudents:
    studentEmail= student
    studentUsername = stripDot( student.split("@")[0])

    MSG = """export LJUMAIL=%s && export LJUNAME=%s && for i in {1..12}; do echo '=============  LAB '$i' ============='; %s/daily.py 1 k all | grep %s | grep  OnPremDeployment_$i | ack --passthru 'failed'; done | mutt -s 'Current OnPrem Deployment Lab Report for %s ' -- showpopulous@gmail.com folay1881@yahoo.com %s""" % ( studentEmail, studentUsername, REPORTS_HOME, studentUsername, studentUsername, studentEmail)

    print ("======= running the following command under onPrem:")
    print (MSG)

    os.system( MSG)    


