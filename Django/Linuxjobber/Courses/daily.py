#!/usr/bin/python
import configparser
import MySQLdb
import sys
import subprocess
import datetime

#CONFIG_FILE = '/home/linuxjobber/tools/config.ini'
print(sys.argv)
# CONFIG_FILE = '/home/linuxjobber/tools/config.ini'
# CONFIG_FILE = 'config.ini'
CONFIG_FILE = './Courses/config.ini'
def addToList( instance):
    instance_list = open("aws_instance_list", "a")
    items = instance.split("'")
    for item in items:
        if 'instance_ip' in item:
            ip_only=item.replace("instance_ip=", "")
            instance_list.write( str( ip_only) + "\n")
    instance_list.close()

if len(sys.argv)  == 1:
    print( "Enter a numeric argument")
    exit()
elif sys.argv[1] == "show":
    print( "1 -> linuxjobber","2 -> noobaid")
    print( "1 a -> get lj trainings","2 b -> get nb users","2 c -> expert searches")
    exit()

queries = list()
if sys.argv[1] == "1":
    if sys.argv[2] == "a":
        a = str("call getPageLogs()")
        queries.append( a)
    if sys.argv[2] == "b":
        a = str("select u.id as id,CONCAT(u.first_name,' ',u.last_name) as full_name,u.email, hl.region, hl.country, DATE(u.date_joined) from users_customuser as u left join home_userlocation as hl on hl.user_id=u.id")
        queries.append( a)
    if sys.argv[2] == "c":
        a = str("select aw.id,aw.user_id,CONCAT(u.first_name,' ',u.last_name), u.username, aw.accesskey, aw.secretkey, aw.date from home_awscredential as aw join users_customuser as u on u.id=aw.user_id")
        queries.append( a)
    if sys.argv[2] == "d":
        a = str("select * from users_customuser where role=3")
        queries.append( a)
    if sys.argv[2] == "e":
        a = str("select * from home_unsubscriber")
        queries.append( a)
    if sys.argv[2] == "f":
        if len(sys.argv) == 3:
            a = str("select id,firstname,lastname,email from home_job")
        queries.append( a)
    if sys.argv[2] == "g":
        if len(sys.argv) == 4:
            a = str("call getUserDossier(%s)" % (sys.argv[3],))
        else:
            a = str("select sc.user_id,sc.day,sc.time,sc.day_2,sc.time_2,sc.mode,sc.mode_2,sc.phone,u.full_name from schedules as sc left join users as u on sc.user_id=u.id")
        queries.append( a)

    if sys.argv[2] == "h":
        if len(sys.argv)  == 3:
            a = str("select CONCAT(u.first_name,' ',u.last_name) as full_name, u.email, t.topic, ts.status, ts.video, DATE(ts.last_watched) from Courses_topicstat as ts left join Courses_coursetopic as t on t.id=ts.topic_id left join users_customuser as u on u.id=ts.user_id")
        elif sys.argv[3] == "info":
            a = str("select CONCAT(u.first_name,' ',u.last_name) as full_name, u.email, t.topic, ts.status, ts.video, DATE(ts.last_watched) from Courses_topicstat as ts left join Courses_coursetopic as t on t.id=ts.topic_id left join users_customuser as u on u.id=ts.user_id where u.email='%s'" % (sys.argv[4]))
        queries.append( a)

    if sys.argv[2] == "i":
        if len(sys.argv) == 4:
            # to find video likely subscribers for a specific day, enter the date as argument. e.g ~/daily 1 i 2017-08-22
            #a = str("call getLikelyToSubscribe('%s'  - INTERVAL 1 DAY)" % (sys.argv[3],))
            a = str("call getLikelyToSubscribe('%s')" % (sys.argv[3],))
        else:
            a = str("call getLikelyToSubscribe(NULL)")
        queries.append( a)

    if sys.argv[2] == "j":
        a = str("select u.email, CONCAT(u.first_name,' ',u.last_name) as full_name,ci.course_title from users_customuser as u right join Courses_userinterest as ui on u.id=ui.user_id join Courses_course as ci on ui.course_id=ci.id")
        queries.append( a)

    if sys.argv[2] == "k":
        if len(sys.argv)  == 3:
            a = str("select u.username,lr.user_id,lr.lab_id,lr.course_topic_id, c.lab_name,lr.grade,lr.date from Courses_gradesreport as  lr left join users_customuser as u on u.id=lr.user_id left join Courses_coursetopic as c on c.id=lr.course_topic_id WHERE DATE(lr.date) = (CURDATE() - INTERVAL 1 DAY);")
        elif sys.argv[3] == "all":
            a = str("select u.username,lr.user_id,lr.lab_id,lr.course_topic_id, c.lab_name,lr.grade,lr.date from Courses_gradesreport as lr left join users_customuser as u on u.id=lr.user_id left join Courses_coursetopic as c on c.id=lr.course_topic_id;")
        elif sys.argv[3] == "info":
            a = str("select u.username,lr.user_id,lr.lab_id,lr.course_topic_id, c.lab_name,lr.grade,lr.date,u.email from Courses_gradesreport as  lr left join users_customuser as u on u.id=lr.user_id left join Courses_coursetopic as c on c.id=lr.course_topic_id;")
        elif sys.argv[3] == "today":
            a = str("select u.username,lr.user_id,lr.lab_id,lr.course_topic_id, c.lab_name,lr.grade,lr.date from Courses_gradesreport as  lr left join users_customuser as u on u.id=lr.user_id left join Courses_coursetopic as c on c.id=lr.course_topic_id WHERE DATE(lr.date) = CURDATE();")
        queries.append( a)

    if sys.argv[2] == "l":
        a = str("select distinct(u.email), CONCAT(u.first_name,' ',u.last_name) as full_name, h.amount, u.id, h.date from home_groupclassregister as h join users_customuser as u on u.id=h.user_id")
        queries.append( a)
 
    if sys.argv[2] == "m":
        a = str("select CONCAT(firstname,' ',lastname) as full_name,email,phone,Address,course from home_internship")
        queries.append( a)

    if sys.argv[2] == "s":
        a = str("select  COUNT( id) from users_customuser where date_joined > TIMESTAMP( DATE_SUB( NOW(), INTERVAL 6 day))")
        queries.append( a)
        a = str("select date_joined, COUNT( id) from users_customuser where date_joined > TIMESTAMP( DATE_SUB( NOW(), INTERVAL 7 day)) AND DAYNAME(date_joined)='Sunday'")
        queries.append( a)
        a = str("select DAYNAME(date_joined), COUNT( id) from users_customuser where date_joined > TIMESTAMP( DATE_SUB( NOW(), INTERVAL 6 day)) AND DAYNAME(date_joined)='Monday'")
        queries.append( a)
        a = str("select DAYNAME(date_joined), COUNT( id) from users_customuser where date_joined > TIMESTAMP( DATE_SUB( NOW(), INTERVAL 6 day)) AND DAYNAME(date_joined)='Tuesday'")
        queries.append( a)
        a = str("select DAYNAME(date_joined), COUNT( id) from users_customuser where date_joined > TIMESTAMP( DATE_SUB( NOW(), INTERVAL 6 day)) AND DAYNAME(date_joined)='Wednesday'")
        queries.append( a)
        a = str("select DAYNAME(date_joined), COUNT( id) from users_customuser where date_joined > TIMESTAMP( DATE_SUB( NOW(), INTERVAL 6 day)) AND DAYNAME(date_joined)='Thursday'")
        queries.append( a)
        a = str("select DAYNAME(date_joined), COUNT( id) from users_customuser where date_joined > TIMESTAMP( DATE_SUB( NOW(), INTERVAL 6 day)) AND DAYNAME(date_joined)='Friday'")
        queries.append( a)
        a = str("select DAYNAME(date_joined), COUNT( id) from users_customuser where date_joined > TIMESTAMP( DATE_SUB( NOW(), INTERVAL 6 day)) AND DAYNAME(date_joined)='Saturday'")
        queries.append( a)

    if sys.argv[2] == "t":
        a = str("select u.full_name, u.username, aw.access_Key_id, aw.secret_access_key from aws_settings as aw left join users as u on u.id=aw.user_id")
        queries.append( a)

    if sys.argv[2] == "u":
        a = str("select email, fullname as full_name, old_career, new_career_id, application_date from home_careerswitchapplication where email NOT IN (SELECT email FROM home_unsubscriber) ")
        queries.append( a)

    if sys.argv[2] == "uy":
        a = str("SELECT email, fullname as full_name, old_career, new_career_id, application_date from home_careerswitchapplication WHERE email NOT IN (SELECT email FROM home_unsubscriber) AND application_date >= DATE_SUB(NOW(), INTERVAL 25 HOUR) ")
        queries.append( a)

    if sys.argv[2] == "v":
        a = str("select email, fullname as full_name, phone, position_id, interest, application_date from home_job where email NOT IN (SELECT email FROM home_unsubscriber) ")
        queries.append( a)

    if sys.argv[2] == "vy":
        a = str("SELECT email, fullname as full_name, phone, position_id, interest, application_date FROM home_job WHERE email NOT IN (SELECT email FROM home_unsubscriber) AND application_date >= DATE_SUB(NOW(), INTERVAL 25 HOUR) ")
        queries.append( a)


if sys.argv[1] == "2":
    if sys.argv[2] == "b":
        a = str("select id,fname,lname,username,created from users")
    elif sys.argv[2] == "c":
        a = str("select * from expertsearch")

parser = configparser.SafeConfigParser()
parser.read( CONFIG_FILE)

if sys.argv[1] == "1":
    connection = MySQLdb.connect (host=parser.get('linuxjobber','HOST'),user=parser.get('linuxjobber','USER'),passwd=parser.get('linuxjobber','PASSWD'),db=parser.get('linuxjobber','DB'));
elif sys.argv[1] == "2":
    connection = MySQLdb.connect (host=parser.get('noobaid','host'),user=parser.get('noobaid','user'),passwd=parser.get('noobaid','passwd'),db=parser.get('noobaid','db'));

def runAndPrint( connection, a):

    cursor = connection.cursor ()

    # execute the SQL query using execute() method.
    cursor.execute (a)


    if sys.argv[2] == "t":
        # fetch all of the rows from the query
        results = cursor.fetchall ()
        #empty running machines list in this directory
        open('aws_instance_list', 'w').close()
        for aws_user in results:
            try:
                aws_output = subprocess.check_output('python /var/www/html/cake2/app/webroot/python/s3_sample.py %s %s instance_running' % (aws_user[2],aws_user[3]), shell=True).split('\n')
                for line in aws_output:
                    if 'instance_ip' in line:
                        print( str(aws_user[0])+" --------------> "+ line)
                        # update running machines list
                        addToList( line)
            except subprocess.CalledProcessError as cpe:
                print ( str(aws_user[0])+'----- AWS account error')

    elif sys.argv[2] != "insert":
        # fetch all of the rows from the query
        results = cursor.fetchall ()
        widths = []
        columns = []
        tavnit = '|'
        separator = '+' 

        for cd in cursor.description:
            widths.append(max(cd[2], len(cd[0])))
            columns.append(cd[0])

        for w in widths:
            tavnit += " %-"+"%ss |" % (w,)
            separator += '-'*w + '--+'

        print(separator)
        print(tavnit % tuple(columns))
        print(separator)
        for row in results:
            print(tavnit % row)
        print(separator)

    cursor.close ()

#if sys.argv[2] == "t":
#    aws_output = subprocess.check_output('python /var/www/html/cake2/app/webroot/python/s3_sample.py %s %s instance_running' % ('AKIAJO3IPFW577P64VPQ', '8r2IKxICYhwasIrzWdS2siMao11VnnjJg7mS7ghO'), shell=True).split('\n')
#    for line in aws_output:
#        if 'instance_ip' in line:
#            print( results[0]+line)
#else:
for qry in queries:
    runAndPrint( connection, qry)

# close the connection
connection.close ()

# exit the program
sys.exit()
