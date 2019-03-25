import shutil
import subprocess
import sys
import zipfile
import logging
import time

from os import fdopen, remove
from shutil import move
from tempfile import mkstemp

import selenium
import selenium.webdriver
from selenium.webdriver.firefox.options import Options



from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select





import django
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from Courses.models import *

os.environ.setdefault("_SETTINGS_MODULE","server.settings")



############################################################################################################################################################
# Construction of projects directories/paths.
############################################################################################################################################################
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APPLICATION_DIR = os.path.join(BASE_DIR, 'Courses')
PROJECT_DIR = os.path.join(BASE_DIR, 'Linuxjobber')
PROJECT_MEDIA_DIR = os.path.join(BASE_DIR, 'media/uploads') # Directory that contains projects media
DJANGO_LAB_SUB_DIR = os.path.join(APPLICATION_DIR, 'utils/DjangoLabSubmissions/') #Directory that contains media exclucive to DjangoLabs Application
VERYFD_BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),'veryfd') #Project to install students application 
VERYFD_PROJECT_DIR = os.path.join(VERYFD_BASE_DIR, 'veryfd') #Verifyd project directory containing the settings.py and urls.py

############################################################################################################################################################

#REQUIREMENT_TEXT = 'Django==2.0\ngunicorn==19.9.0\nmysqlclient==1.3.12\n'
REQUIREMENT_TEXT = 'Django==2.0\n'



#--------------------------------------------------------------------------------------------------------
#FUNCTIONS
#--------------------------------------------------------------------------------------------------------

def check_if_upload_is_django_project(EXTRACT_LOCATION, user):
	flag=0
	for root, dirs, files in os.walk(EXTRACT_LOCATION):
		for dirname in dirs:
			if dirname == 'myscrumy':
				flag+=1
		for dirname in dirs:
			if dirname == user + 'scrumy':
				flag+=1
		for file in files:
			if file.endswith('dmin.py') or file.endswith('odels.py') or file.endswith('iews.py') or file.endswith('ests.py') or file.endswith('pps.py') or file.endswith('settings.py') or file.endswith('manage.py'):
				flag+=1
		for file in files:
			if file.endswith('urls.py'):
				flag+= 1
	if flag > 9:
		return(True)
	else:
		return(False)



def save_grade(lab_number, current_user, result):
	try:
		course_topic = CourseTopic.objects.get(topic_number = lab_number, course__course_title = 'Django')

		i=0
		GradesReport.objects.filter(user=current_user,course_topic=course_topic).delete()
		for key,value in result.items():
			i+=1
			task=LabTask.objects.get(task_number=i, lab__topic_number=lab_number)
			if value=='done':
				report = GradesReport(score = 1, course_topic=course_topic, user=current_user, grade='passed', lab=task)
				report.save()
			else:
				report = GradesReport(score = 0, course_topic=course_topic, user=current_user, grade='failed', lab=task)
				report.save()
	except Exception as e:
		print(e)



	#report = GradesReport(score = str(mark), course_topic=course_topic, user=current_user, grade=str(grade), lab=lab)
	#report.save()
	#print('saved grade')


def create_docker_file(EXTRACT_LOCATION,PORT,USERNAME):

	DOCKER_CONFIG = {
		'LINE_1':'FROM python:3.6\n',
		'LINE_2':'MAINTAINER '+USERNAME+'\n',
		'LINE_3':'ADD . '+EXTRACT_LOCATION+'/myscrumy'+'\n',
		'LINE_4':'WORKDIR '+EXTRACT_LOCATION+'/myscrumy'+'\n',
		'LINE_5':'COPY requirements.txt ./'+'\n',
		'LINE_6':'RUN pip install --no-cache-dir -r requirements.txt'+'\n',
		'LINE_7':'EXPOSE '+str(PORT)+'\n',
		'LINE_8':'CMD [ "python", "./manage.py", "runserver", "0.0.0.0:'+str(PORT)+'" ]',
	}

	try:
		with open(os.path.join(EXTRACT_LOCATION,'myscrumy/Dockerfile'),'w') as dock:
			for key,value in DOCKER_CONFIG.items():
				dock.write(value)
	except Exception as e:
		print(e)

def stop_and_remove_docker_container(USERNAME,LAB_NUMBER):
	try:
		subprocess.run(["sudo","docker","stop",USERNAME+"scrumy_"+LAB_NUMBER]) #stop container
		subprocess.run(["sudo","docker","rm",USERNAME+"scrumy_"+LAB_NUMBER]) #remove container
	except Exception as e:
		print(e)


def build_and_run_docker(USERNAME,LAB_NUMBER,PORT):
	try:
		subprocess.run(["sudo","docker","build","-t",USERNAME+"scrumy_img","."]) #Build docker image
		subprocess.run(["sudo","docker","run","--name="+USERNAME+"scrumy_"+LAB_NUMBER,"-d","-p",PORT+":"+PORT,USERNAME+"scrumy_img"]) #run docker image
	except Exception as e:
		print(e)
#-------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------
# Logging Instances
#----------------------------------------------------------------------------------------------------------

standard_logger = logging.getLogger(__name__)
dbalogger = logging.getLogger('dba')


#-----------------------------------------------------------------------------------------------------------




def grade_django_lab20(file, lab_number, current_user, topic, course):
	error = {
		'error_msg':'',
	}
	if file.name.endswith('myscrumy.zip') and file.name.startswith('myscrumy'):

		EXTRACT_LOCATION = DJANGO_LAB_SUB_DIR+current_user.username+'_'+str(lab_number)


		result = {
			'task_one_status' : 'undone',
			'task_two_status' : 'undone',
			'task_three_status' : 'undone',
		}

		try:
			zfile = zipfile.ZipFile(file) 
		except zipfile.BadZipfile as ex:
			error['error_msg']='The file you uploaded is a bad zipfile or not a zipfile'
			return(error)
		else:

			'''
				Checks through the entire achive of the opened zifile to pick out any bad member of the achive
			'''
			ret = zfile.testzip()
			if ret is not None:
				error['error_msg']='A file in the zip achive is corrupt'
				return(error)
			else:
				zfile.extractall(EXTRACT_LOCATION)

				PORT = current_user.id+2910

				if check_if_upload_is_django_project(EXTRACT_LOCATION,current_user.username):
					profile = selenium.webdriver.FirefoxProfile()
					profile.accept_untrusted_certs = True
					options = selenium.webdriver.FirefoxOptions()
					options.add_argument('--headless')
					driver = selenium.webdriver.Firefox(firefox_profile=profile, firefox_options=options)
					
					try:

						create_docker_file(EXTRACT_LOCATION,PORT,current_user.username)

						with open(os.path.join(EXTRACT_LOCATION,'myscrumy/requirements.txt'),'w') as req:
							req.write(REQUIREMENT_TEXT)

						working_dir=os.getcwd()
						
						os.chdir(os.path.join(EXTRACT_LOCATION,'myscrumy'))

						build_and_run_docker(current_user.username,str(lab_number),str(PORT))

						with open(os.path.join(EXTRACT_LOCATION,'myscrumy/myscrumy/settings.py'),'r') as settings_file:
							for eachline in settings_file:
								if eachline.startswith('LOGIN_REDIRECT_URL'):
									result['task_three_status']='done'
					except Exception as e:
						print(e)

					shutil.rmtree(EXTRACT_LOCATION)
					time.sleep(10)

					
					try:
						csrf_t = ''
						form_method = ''

						try:
							driver.get('http:localhost:'+str(PORT)+'/'+current_user.username+'scrumy/accounts/login')
							form_method = driver.find_element_by_xpath('//form').get_attribute('method')
							csrf_t = driver.find_element_by_name('csrfmiddlewaretoken').get_attribute('type')
						except Exception as e:
							print (e)

						if csrf_t == 'hidden':
							result['task_two_status']='done'

						inputs=driver.find_elements_by_tag_name('input')
						if form_method=='post' or form_method=='POST' and len(inputs) > 1:
							result['task_one_status']='done'
					except Exception as e:
						print(e)
					finally:
						driver.quit()

					stop_and_remove_docker_container(current_user.username,str(lab_number))
					save_grade(lab_number, current_user, result)
					return(result)
				else:
					shutil.rmtree(EXTRACT_LOCATION)
					error['error_msg']='The file you uploaded does not contain your scrumy project or one of the project files are missing.'
					return(error)
	else:
		error['error_msg']='Please verify that the file you are uploading corresponds to the format specified in the lab instructions and try again'
		return(error)



def grade_django_lab19(file, lab_number, current_user, topic, course):
	error = {
		'error_msg':'',
	}
	if file.name.endswith('myscrumy.zip') and file.name.startswith('myscrumy'):

		EXTRACT_LOCATION = DJANGO_LAB_SUB_DIR+current_user.username+'_'+str(lab_number)


		result = {
			'task_one_status' : 'undone',
			'task_two_status' : 'undone',
			'task_three_status' : 'undone',
		}

		try:
			zfile = zipfile.ZipFile(file) 
		except zipfile.BadZipfile as ex:
			error['error_msg']='The file you uploaded is a bad zipfile or not a zipfile'
			return(error)
		else:

			'''
				Checks through the entire achive of the opened zifile to pick out any bad member of the achive
			'''
			ret = zfile.testzip()
			if ret is not None:
				error['error_msg']='A file in the zip achive is corrupt'
				return(error)
			else:
				zfile.extractall(EXTRACT_LOCATION)

				PORT = current_user.id+2910

				if check_if_upload_is_django_project(EXTRACT_LOCATION,current_user.username):
					profile = selenium.webdriver.FirefoxProfile()
					profile.accept_untrusted_certs = True
					options = selenium.webdriver.FirefoxOptions()
					options.add_argument('--headless')
					driver = selenium.webdriver.Firefox(firefox_profile=profile, firefox_options=options)
					
					try:

						create_docker_file(EXTRACT_LOCATION,PORT,current_user.username)

						with open(os.path.join(EXTRACT_LOCATION,'myscrumy/requirements.txt'),'w') as req:
							req.write(REQUIREMENT_TEXT)

						working_dir=os.getcwd()
						
						os.chdir(os.path.join(EXTRACT_LOCATION,'myscrumy'))

						build_and_run_docker(current_user.username,str(lab_number),str(PORT))

						with open(os.path.join(EXTRACT_LOCATION,'myscrumy/myscrumy/settings.py'),'r') as settings_file:
							for eachline in settings_file:
								if eachline.startswith('LOGIN_REDIRECT_URL'):
									result['task_three_status']='done'
					except Exception as e:
						print(e)

					shutil.rmtree(EXTRACT_LOCATION)
					time.sleep(10)

					
					try:
						csrf_t = ''
						form_method = ''

						try:
							driver.get('http:localhost:'+str(PORT)+'/'+current_user.username+'scrumy/accounts/login')
							form_method = driver.find_element_by_xpath('//form').get_attribute('method')
							csrf_t = driver.find_element_by_name('csrfmiddlewaretoken').get_attribute('type')
						except Exception as e:
							print (e)

						if csrf_t == 'hidden':
							result['task_two_status']='done'

						inputs=driver.find_elements_by_tag_name('input')
						if form_method=='post' or form_method=='POST' and len(inputs) > 1:
							result['task_one_status']='done'
					except Exception as e:
						print(e)
					finally:
						driver.quit()

					stop_and_remove_docker_container(current_user.username,str(lab_number))
					save_grade(lab_number, current_user, result) 
					return(result)
				else:
					shutil.rmtree(EXTRACT_LOCATION)
					error['error_msg']='The file you uploaded does not contain your scrumy project or one of the project files are missing.'
					return(error)
	else:
		error['error_msg']='Please verify that the file you are uploading corresponds to the format specified in the lab instructions and try again'
		return(error)







#Creating Forms in Templates
def grade_django_lab18(file, lab_number, current_user, topic, course):
	error = {
		'error_msg':'',
	}
	if file.name.endswith('myscrumy.zip') and file.name.startswith('myscrumy'):

		EXTRACT_LOCATION = DJANGO_LAB_SUB_DIR+current_user.username+'_'+str(lab_number)


		result = {
			'task_one_status' : 'undone',
			'task_two_status' : 'undone',
			'task_three_status' : 'undone',
		}

		try:
			zfile = zipfile.ZipFile(file) 
		except zipfile.BadZipfile as ex:
			error['error_msg']='The file you uploaded is a bad zipfile or not a zipfile'
			return(error)
		else:

			'''
				Checks through the entire achive of the opened zifile to pick out any bad member of the achive
			'''
			ret = zfile.testzip()
			if ret is not None:
				error['error_msg']='A file in the zip achive is corrupt'
				return(error)
			else:
				zfile.extractall(EXTRACT_LOCATION)

				PORT = current_user.id+2910

				if check_if_upload_is_django_project(EXTRACT_LOCATION,current_user.username):
					profile = selenium.webdriver.FirefoxProfile()
					profile.accept_untrusted_certs = True
					options = selenium.webdriver.FirefoxOptions()
					options.add_argument('--headless')
					driver = selenium.webdriver.Firefox(firefox_profile=profile, firefox_options=options)
					
					try:

						create_docker_file(EXTRACT_LOCATION,PORT,current_user.username)

						with open(os.path.join(EXTRACT_LOCATION,'myscrumy/requirements.txt'),'w') as req:
							req.write(REQUIREMENT_TEXT)

						working_dir=os.getcwd()
						
						os.chdir(os.path.join(EXTRACT_LOCATION,'myscrumy'))

						build_and_run_docker(current_user.username,str(lab_number),str(PORT))

						with open(os.path.join(EXTRACT_LOCATION,'myscrumy/myscrumy/settings.py'),'r') as settings_file:
							for eachline in settings_file:
								if eachline.startswith('LOGIN_REDIRECT_URL'):
									result['task_three_status']='done'
					except Exception as e:
						print(e)

					shutil.rmtree(EXTRACT_LOCATION)
					time.sleep(10)

					
					try:
						csrf_t = ''
						form_method = ''

						try:
							driver.get('http:localhost:'+str(PORT)+'/'+current_user.username+'scrumy/accounts/login')
							form_method = driver.find_element_by_xpath('//form').get_attribute('method')
							csrf_t = driver.find_element_by_name('csrfmiddlewaretoken').get_attribute('type')
						except Exception as e:
							print (e)

						if csrf_t == 'hidden':
							result['task_two_status']='done'

						inputs=driver.find_elements_by_tag_name('input')
						if form_method=='post' or form_method=='POST' and len(inputs) > 1:
							result['task_one_status']='done'
					except Exception as e:
						print(e)
					finally:
						driver.quit()

					stop_and_remove_docker_container(current_user.username,str(lab_number))
					save_grade(lab_number, current_user, result)
					return(result)
				else:
					shutil.rmtree(EXTRACT_LOCATION)
					error['error_msg']='The file you uploaded does not contain your scrumy project or one of the project files are missing.'
					return(error)
	else:
		error['error_msg']='Please verify that the file you are uploading corresponds to the format specified in the lab instructions and try again'
		return(error)




#Removing hardcoded urls
def grade_django_lab17(file, lab_number, current_user, topic, course):
	error = {
		'error_msg':'',
	}
	if file.name.endswith('myscrumy.zip') and file.name.startswith('myscrumy'):

		EXTRACT_LOCATION = DJANGO_LAB_SUB_DIR+current_user.username+'_'+str(lab_number)

		result = {
			'task_one_status' : 'undone',
			'task_two_status' : 'undone',
			'task_three_status' : 'undone',
		}

		try:
			zfile = zipfile.ZipFile(file) 
		except zipfile.BadZipfile as ex:
			error['error_msg']='The file you uploaded is a bad zipfile or not a zipfile'
			return(error)
		else:

			'''
				Checks through the entire achive of the opened zifile to pick out any bad member of the achive
			'''
			ret = zfile.testzip()
			if ret is not None:
				error['error_msg']='A file in the zip achive is corrupt'
				return(error)
			else:
				zfile.extractall(EXTRACT_LOCATION)

				PORT = current_user.id+2910

				if check_if_upload_is_django_project(EXTRACT_LOCATION,current_user.username):
					profile = selenium.webdriver.FirefoxProfile()
					profile.accept_untrusted_certs = True
					options = selenium.webdriver.FirefoxOptions()
					options.add_argument('--headless')
					driver = selenium.webdriver.Firefox(firefox_profile=profile, firefox_options=options)

					try:
						create_docker_file(EXTRACT_LOCATION,PORT,current_user.username)

						with open(os.path.join(EXTRACT_LOCATION,'myscrumy/requirements.txt'),'w') as req:
							req.write(REQUIREMENT_TEXT)
						
						os.chdir(os.path.join(EXTRACT_LOCATION,'myscrumy'))

						build_and_run_docker(current_user.username,str(lab_number),str(PORT))
					except Exception as e:
						print(e)

					shutil.rmtree(EXTRACT_LOCATION)
					time.sleep(10)

					
					try:
						inner_html=''
						try:
							driver.get('http:localhost:'+str(PORT)+'/'+current_user.username+'scrumy/accounts/login')
							inner_html=driver.find_element_by_id('summary').get_attribute('innerHTML').rstrip('\n')
						except Exception as e:
							print(e)

						if inner_html == '':
							result['task_one_status']='done'

						if result['task_one_status']=='done':
							result['task_two_status']='done'

							driver.find_element_by_tag_name('a').click()
							html=driver.find_element_by_xpath('//body').get_attribute('innerHTML').rstrip('\n')
							if html.lower()=='hello world':
								result['task_three_status']='done'
					except Exception as e:
						print(e)
					finally:
						driver.quit()
					stop_and_remove_docker_container(current_user.username,str(lab_number))
					save_grade(lab_number, current_user, result)
					return(result)
				else:
					shutil.rmtree(EXTRACT_LOCATION)
					error['error_msg']='The file you uploaded does not contain your scrumy project or one of the project files are missing.'
					return(error)
	else:
		error['error_msg']='Please verify that the file you are uploading corresponds to the format specified in the lab instructions and try again'
		return(error)





#Using Django API to Access Foreign Keys in database within a Template
def grade_django_lab16(file, lab_number, current_user, topic, course):
	error = {
		'error_msg':'',
	}
	if file.name.endswith('myscrumy.zip') and file.name.startswith('myscrumy'):

		EXTRACT_LOCATION = DJANGO_LAB_SUB_DIR+current_user.username+'_'+str(lab_number)


		result = {
			'task_one_status' : 'undone',
			'task_two_status' : 'undone',
		}

		try:
			zfile = zipfile.ZipFile(file) 
		except zipfile.BadZipfile as ex:
			error['error_msg']='The file you uploaded is a bad zipfile or not a zipfile'
			return(error)
		else:

			'''
				Checks through the entire achive of the opened zifile to pick out any bad member of the achive
			'''
			ret = zfile.testzip()
			if ret is not None:
				error['error_msg']='A file in the zip achive is corrupt'
				return(error)
			else:
				zfile.extractall(EXTRACT_LOCATION)

				PORT = current_user.id+2910

				if check_if_upload_is_django_project(EXTRACT_LOCATION,current_user.username):
					profile = selenium.webdriver.FirefoxProfile()
					profile.accept_untrusted_certs = True
					options = selenium.webdriver.FirefoxOptions()
					options.add_argument('--headless')
					driver = selenium.webdriver.Firefox(firefox_profile=profile, firefox_options=options)

					try:

						create_docker_file(EXTRACT_LOCATION,PORT,current_user.username)

						with open(os.path.join(EXTRACT_LOCATION,'myscrumy/requirements.txt'),'w') as req:
							req.write(REQUIREMENT_TEXT)

						working_dir=os.getcwd()
						
						os.chdir(os.path.join(EXTRACT_LOCATION,'myscrumy'))

						build_and_run_docker(current_user.username,str(lab_number),str(PORT))
					except Exception as e:
						print(e)

					shutil.rmtree(EXTRACT_LOCATION)
					time.sleep(10)

					
					try:
						driver.get('http:localhost:'+str(PORT)+'/'+current_user.username+'scrumy/home')

						ths=driver.find_elements_by_tag_name('th')
						daily_goal_position=0
						z=0
						for th in ths:
							z+=1
							if th.get_attribute('innerHTML').rstrip('\n').lower()=='daily goals':
								daily_goal_position=z

						learn_django_position=0
						y=0
						tds=driver.find_elements_by_tag_name('td')
						for td in tds:
							y+=1
							if td.get_attribute('innerHTML').rstrip('\n').lower()=='learn django':
								learn_django_position=y

						if daily_goal_position==learn_django_position and daily_goal_position!=0:
							result['task_one_status']='done'
							result['task_two_status']='done'
					except Exception as e:
						print(e)
					finally:
						driver.quit()

					stop_and_remove_docker_container(current_user.username,str(lab_number))
					save_grade(lab_number, current_user, result)
					return(result)
				else:
					shutil.rmtree(EXTRACT_LOCATION)
					error['error_msg']='The file you uploaded does not contain your scrumy project or one of the project files are missing.'
					return(error)
	else:
		error['error_msg']='Please verify that the file you are uploading corresponds to the format specified in the lab instructions and try again'
		return(error)









def grade_django_lab15(file, lab_number, current_user, topic, course):
	error = {
		'error_msg':'',
	}
	if file.name.endswith('myscrumy.zip') and file.name.startswith('myscrumy'):

		EXTRACT_LOCATION = DJANGO_LAB_SUB_DIR+current_user.username+'_'+str(lab_number)


		result = {
			'task_one_status' : 'undone',
		}

		try:
			zfile = zipfile.ZipFile(file) 
		except zipfile.BadZipfile as ex:
			error['error_msg']='The file you uploaded is a bad zipfile or not a zipfile'
			return(error)
		else:

			'''
				Checks through the entire achive of the opened zifile to pick out any bad member of the achive
			'''
			ret = zfile.testzip()
			if ret is not None:
				error['error_msg']='A file in the zip achive is corrupt'
				return(error)
			else:
				zfile.extractall(EXTRACT_LOCATION)

				PORT = current_user.id+2910

				if check_if_upload_is_django_project(EXTRACT_LOCATION,current_user.username):
					profile = selenium.webdriver.FirefoxProfile()
					profile.accept_untrusted_certs = True
					options = selenium.webdriver.FirefoxOptions()
					options.add_argument('--headless')
					driver = selenium.webdriver.Firefox(firefox_profile=profile, firefox_options=options)
					try:

						create_docker_file(EXTRACT_LOCATION,PORT,current_user.username)

						with open(os.path.join(EXTRACT_LOCATION,'myscrumy/requirements.txt'),'w') as req:
							req.write(REQUIREMENT_TEXT)
						
						os.chdir(os.path.join(EXTRACT_LOCATION,'myscrumy'))

						build_and_run_docker(current_user.username,str(lab_number),str(PORT))
					except Exception as e:
						print(e)

					shutil.rmtree(EXTRACT_LOCATION)
					time.sleep(10)

					
					try:
						driver.get('http:localhost:'+str(PORT)+'/'+current_user.username+'scrumy/movegoal/386')
						inner_html=''
						try:
							inner_html=driver.find_element_by_id('summary').get_attribute('innerHTML').rstrip('\n')
						except Exception as e:
							print(e)
						if inner_html == '':
							result['task_one_status']='done'
					except Exception as e:
						print(e)
					finally:
						driver.quit()

					stop_and_remove_docker_container(current_user.username,str(lab_number))
					save_grade(lab_number, current_user, result)
					return(result)
				else:
					shutil.rmtree(EXTRACT_LOCATION)
					error['error_msg']='The file you uploaded does not contain your scrumy project or one of the project files are missing.'
					return(error)
	else:
		error['error_msg']='Please verify that the file you are uploading corresponds to the format specified in the lab instructions and try again'
		return(error)




def grade_django_lab14(file, lab_number, current_user, topic, course):
	error = {
		'error_msg':'',
	}

	if file.name.endswith('myscrumy.zip') and file.name.startswith('myscrumy'):

		EXTRACT_LOCATION = DJANGO_LAB_SUB_DIR+current_user.username+'_'+str(lab_number)


		result = {
			'task_one_status' : 'undone',
			'task_two_status' : 'undone',
			'task_three_status' : 'undone',
		}


		try:
			zfile = zipfile.ZipFile(file) 
		except zipfile.BadZipfile as ex:
			error['error_msg']='The file you uploaded is a bad zipfile or not a zipfile'
			return(error)
		else:

			'''
				Checks through the entire achive of the opened zifile to pick out any bad member of the achive
			'''
			ret = zfile.testzip()
			if ret is not None:
				error['error_msg']='A file in the zip achive is corrupt'
				return(error)
			else:
				zfile.extractall(EXTRACT_LOCATION)

				PORT = current_user.id+2910
				if check_if_upload_is_django_project(EXTRACT_LOCATION,current_user.username):
					profile = selenium.webdriver.FirefoxProfile()
					profile.accept_untrusted_certs = True
					options = selenium.webdriver.FirefoxOptions()
					options.add_argument('--headless')
					driver = selenium.webdriver.Firefox(firefox_profile=profile, firefox_options=options)
					try:

						create_docker_file(EXTRACT_LOCATION,PORT,current_user.username)

						with open(os.path.join(EXTRACT_LOCATION,'myscrumy/requirements.txt'),'w') as req:
							req.write(REQUIREMENT_TEXT)

						working_dir=os.getcwd()
						
						os.chdir(os.path.join(EXTRACT_LOCATION,'myscrumy'))

						build_and_run_docker(current_user.username,str(lab_number),str(PORT))
					except Exception as e:
						print(e)

					shutil.rmtree(EXTRACT_LOCATION)
					time.sleep(10)

					
					try:
						driver.get('http:localhost:'+str(PORT)+'/'+current_user.username+'scrumy/home')

						user_inner_html = driver.find_element_by_xpath('//td[contains(text(),"louis")]').get_attribute('innerHTML').rstrip('\n')
						if user_inner_html.lower() == 'louis':
							result['task_one_status']='done'
							result['task_two_status']='done'
							result['task_three_status']='done'
					except Exception as e:
						print(e)
					finally:
						driver.quit()

					stop_and_remove_docker_container(current_user.username,str(lab_number))
					save_grade(lab_number, current_user, result) 
					return(result)
				else:
					shutil.rmtree(EXTRACT_LOCATION)
					error['error_msg']='The file you uploaded does not contain your scrumy project or one of the project files are missing.'
					return(error)
	else:
		error['error_msg']='Please verify that the file you are uploading corresponds to the format specified in the lab instructions and try again'
		return(error)


#CREATING VIEWS THAT ACCESS THE DATABASE
def grade_django_lab13(file, lab_number, current_user, topic, course):
	error = {
		'error_msg':'',
	}

	if file.name.endswith('myscrumy.zip') and file.name.startswith('myscrumy'):

		EXTRACT_LOCATION = DJANGO_LAB_SUB_DIR+current_user.username+'_'+str(lab_number)


		result = {
			'task_one_status' : 'undone',
			'task_two_status' : 'undone',
			'task_three_status' : 'undone',
			'task_four_status' : 'undone',
		}

		try:
			zfile = zipfile.ZipFile(file) 
		except zipfile.BadZipfile as ex:
			error['error_msg']='The file you uploaded is a bad zipfile or not a zipfile'
			return(error)
		else:

			'''
				Checks through the entire achive of the opened zifile to pick out any bad member of the achive
			'''
			ret = zfile.testzip()
			if ret is not None:
				error['error_msg']='A file in the zip achive is corrupt'
				return(error)
			else:
				zfile.extractall(EXTRACT_LOCATION)

				PORT = current_user.id+2910
				if check_if_upload_is_django_project(EXTRACT_LOCATION,current_user.username):
					profile = selenium.webdriver.FirefoxProfile()
					profile.accept_untrusted_certs = True
					options = selenium.webdriver.FirefoxOptions()
					options.add_argument('--headless')
					driver = selenium.webdriver.Firefox(firefox_profile=profile, firefox_options=options)
					driver2 = selenium.webdriver.Firefox(firefox_profile=profile, firefox_options=options)
					try:

						create_docker_file(EXTRACT_LOCATION,PORT,current_user.username)

						with open(os.path.join(EXTRACT_LOCATION,'myscrumy/requirements.txt'),'w') as req:
							req.write(REQUIREMENT_TEXT)

						working_dir=os.getcwd()
						
						os.chdir(os.path.join(EXTRACT_LOCATION,'myscrumy'))

						build_and_run_docker(current_user.username,str(lab_number),str(PORT))
					except Exception as e:
						print(e)

					shutil.rmtree(EXTRACT_LOCATION)
					time.sleep(10)
					try:
						driver.get('http:localhost:'+str(PORT)+'/'+current_user.username+'scrumy/addgoal')
						inner_html=''
						try:
							inner_html=driver.find_element_by_id('summary').get_attribute('innerHTML').rstrip('\n')
						except Exception as e:
							print(e)
						print(inner_html)
						if inner_html == '':
							result['task_one_status']='done'
					except Exception as e:
						print(e)
					
					try:
						driver2.get('http:localhost:'+str(PORT)+'/'+current_user.username+'scrumy/home')

						inner_html=driver2.find_element_by_xpath('//body').get_attribute('innerHTML').rstrip('\n')
						if inner_html.lower() == 'learn django':
							result['task_two_status']='done'
							result['task_three_status']='done'
					except Exception as e:
						print(e)
					finally:
						driver.quit()
						driver2.quit()

					if result['task_one_status']=='done' and result['task_two_status']=='done':
						result['task_four_status']='done'

					stop_and_remove_docker_container(current_user.username,str(lab_number))
					save_grade(lab_number, current_user, result)
					return(result)
				else:
					shutil.rmtree(EXTRACT_LOCATION)
					error['error_msg']='The file you uploaded does not contain your scrumy project or one of the project files are missing.'
					return(error)				
	else:
		error['error_msg']='Please verify that the file you are uploading corresponds to the format specified in the lab instructions and try again'
		return(error)



#CREATING VIEWS THAT ACCEPT ARGUMENTS
def grade_django_lab12(file, lab_number, current_user, topic, course):
	error = {
		'error_msg':'',
	}

	if file.name.endswith('myscrumy.zip') and file.name.startswith('myscrumy'):

		EXTRACT_LOCATION = DJANGO_LAB_SUB_DIR+current_user.username+'_'+str(lab_number)


		result = {
			'task_one_status' : 'undone',
			'task_two_status' : 'undone',
		}

		try:
			zfile = zipfile.ZipFile(file) 
		except zipfile.BadZipfile as ex:
			error['error_msg']='The file you uploaded is a bad zipfile or not a zipfile'
			return(error)
		else:


			'''
				Checks through the entire achive of the opened zifile to pick out any bad member of the achive
			'''
			ret = zfile.testzip()
			if ret is not None:
				error['error_msg']='A file in the zip achive is corrupt'
				return(error)
			else:
				zfile.extractall(EXTRACT_LOCATION)

				PORT = current_user.id+2910
				if check_if_upload_is_django_project(EXTRACT_LOCATION,current_user.username):
					profile = selenium.webdriver.FirefoxProfile()
					profile.accept_untrusted_certs = True
					options = selenium.webdriver.FirefoxOptions()
					options.add_argument('--headless')
					driver = selenium.webdriver.Firefox(firefox_profile=profile, firefox_options=options)
					try:

						create_docker_file(EXTRACT_LOCATION,PORT,current_user.username)

						with open(os.path.join(EXTRACT_LOCATION,'myscrumy/requirements.txt'),'w') as req:
							req.write(REQUIREMENT_TEXT)

						working_dir=os.getcwd()
						
						os.chdir(os.path.join(EXTRACT_LOCATION,'myscrumy'))

						build_and_run_docker(current_user.username,str(lab_number),str(PORT))
					except Exception as e:
						print(e)

					shutil.rmtree(EXTRACT_LOCATION)
					time.sleep(10)
					try:
						driver.get('http:localhost:'+str(PORT)+'/admin')

						driver.find_element_by_name('username').send_keys('louis')
						driver.find_element_by_name('password').send_keys('DJANGO_123')
						driver.find_element_by_xpath('//input[@type="submit"]').click()

						driver.find_element_by_partial_link_text('Scrumy goals').click()
						scrumy_goal_records = driver.find_elements_by_partial_link_text('ScrumyGoals object')

						record_length = len(scrumy_goal_records)
						goal_id=''
						for rec in range(record_length):
							driver.get('http:localhost:'+str(PORT)+'/admin')
							driver.find_element_by_partial_link_text('Scrumy goals').click()
							scrumy_goal_records = driver.find_elements_by_partial_link_text('ScrumyGoals object')
							scrumy_goal_records[rec].click()
							goal_id=driver.find_element_by_name('goal_id').get_attribute('value').rstrip('\n')
		
						elem=''
		
						try:
							driver.get('http://localhost:'+str(PORT)+'/'+current_user.username+'scrumy/movegoal/'+goal_id)
							elem=driver.find_element_by_xpath('//div[@id="summary"]').get_attribute('id').rstrip('\n')
							print(elem)
						except Exception as e:
							print(e)
						if elem != 'summary':
							result['task_one_status']='done'
							result['task_two_status']='done'
					except Exception as e:
						print(e)
					finally:
						driver.quit()
					stop_and_remove_docker_container(current_user.username,str(lab_number))
					save_grade(lab_number, current_user, result)
					return(result)
				else:
					shutil.rmtree(EXTRACT_LOCATION)
					error['error_msg']='The file you uploaded does not contain your scrumy project or one of the project files are missing.'
					return(error)					
	else:
		error['error_msg']='Please verify that the file you are uploading corresponds to the format specified in the lab instructions and try again'
		return(error)





def grade_django_lab11(file, lab_number, current_user, topic, course):
	error = {
		'error_msg':'',
	}
	if file.name.endswith('myscrumy.zip') and file.name.startswith('myscrumy'):

		EXTRACT_LOCATION = DJANGO_LAB_SUB_DIR+current_user.username+'_'+str(lab_number)


		result = {
			'task_one_status' : 'undone',
			'task_two_status' : 'undone',
			'task_three_status' : 'undone',
		}

		try:
			zfile = zipfile.ZipFile(file) 
		except zipfile.BadZipfile as ex:
			error['error_msg']='The file you uploaded is a bad zipfile or not a zipfile'
			return(error)
		else:


			'''
				Checks through the entire achive of the opened zifile to pick out any bad member of the achive
			'''
			ret = zfile.testzip()
			if ret is not None:
				error['error_msg']='A file in the zip achive is corrupt'
				return(error)
			else:
				zfile.extractall(EXTRACT_LOCATION)

				PORT = current_user.id+2910
				if check_if_upload_is_django_project(EXTRACT_LOCATION,current_user.username):
					profile = selenium.webdriver.FirefoxProfile()
					profile.accept_untrusted_certs = True
					options = selenium.webdriver.FirefoxOptions()
					options.add_argument('--headless')
					driver = selenium.webdriver.Firefox(firefox_profile=profile, firefox_options=options)
					try:

						create_docker_file(EXTRACT_LOCATION,PORT,current_user.username)

						with open(os.path.join(EXTRACT_LOCATION,'myscrumy/requirements.txt'),'w') as req:
							req.write(REQUIREMENT_TEXT)

						working_dir=os.getcwd()
						
						os.chdir(os.path.join(EXTRACT_LOCATION,'myscrumy'))

						build_and_run_docker(current_user.username,str(lab_number),str(PORT))
					except Exception as e:
						print(e)

					shutil.rmtree(EXTRACT_LOCATION)

					time.sleep(10)

					try:
						driver.get('http:localhost:'+str(PORT)+'/admin')

						driver.find_element_by_name('username').send_keys('louis')
						driver.find_element_by_name('password').send_keys('DJANGO_123')
						driver.find_element_by_xpath('//input[@type="submit"]').click()

						driver.find_element_by_partial_link_text('Scrumy goals').click()
						scrumy_goal_records = driver.find_elements_by_partial_link_text('ScrumyGoals object')

						record_length = len(scrumy_goal_records)
						m_list=[]
						for rec in range(record_length):
							driver.get('http:localhost:'+str(PORT)+'/admin')
							driver.find_element_by_partial_link_text('Scrumy goals').click()
							scrumy_goal_records = driver.find_elements_by_partial_link_text('ScrumyGoals object')
							scrumy_goal_records[rec].click()
							goal_name=driver.find_element_by_name('goal_name').get_attribute('value').rstrip('\n')
							goal_id=driver.find_element_by_name('goal_id').get_attribute('value').rstrip('\n')
							created_by=driver.find_element_by_name('created_by').get_attribute('value').rstrip('\n')
							moved_by=driver.find_element_by_name('moved_by').get_attribute('value').rstrip('\n')
							owner=driver.find_element_by_name('owner').get_attribute('value').rstrip('\n')
							select_element = Select(driver.find_element_by_name("goal_status"))
							goal_status = select_element.first_selected_option.text


							m_list.append({'goal_status':goal_status,'goal_name':goal_name,'goal_id':goal_id,'created_by':created_by,'moved_by':moved_by,'owner':owner})
						for each_entry in m_list:
							if each_entry['goal_name'].lower()=='learn django' and each_entry['goal_id'].lower()=='1' and each_entry['created_by'].lower()=='oma' and each_entry['moved_by'].lower()=='louis' and each_entry['owner'].lower()=='louis':
								result['task_one_status']='done'

						driver.get('http:localhost:'+str(PORT)+'/admin')
						driver.find_element_by_partial_link_text('Goal status').click()
						goal_status_records = driver.find_elements_by_partial_link_text('GoalStatus object')
						
						goal_status_record_length = len(goal_status_records)
						
						
						for rec in range(goal_status_record_length):
							driver.get('http:localhost:'+str(PORT)+'/admin')
							driver.find_element_by_partial_link_text('Goal status').click()
							goal_status_records = driver.find_elements_by_partial_link_text('GoalStatus object')
							goal_status_records[rec].click()
							p=driver.find_element_by_name('status_name').get_attribute('value').rstrip('\n').lower()
							print('here is p')
							print(p)
							if p =='daily goal':
								driver.get('http:localhost:'+str(PORT)+'/admin')
								driver.find_element_by_partial_link_text('Goal status').click()
								goal_status_records_2 = driver.find_elements_by_partial_link_text('GoalStatus object')
								for each_entry in m_list:

									if each_entry['goal_status']==goal_status_records_2[rec].get_attribute('innerHTML').rstrip('\n'):
										result['task_two_status']='done'

						driver.get('http:localhost:'+str(PORT)+'/'+current_user.username+'scrumy')
						elem = driver.find_element_by_xpath('//body').get_attribute('innerHTML')
						if elem != '':
							result['task_three_status']='done'
					except Exception as e:
						print(e)
					finally:
						driver.quit()

					stop_and_remove_docker_container(current_user.username,str(lab_number))
					save_grade(lab_number, current_user, result)
					return(result)
				else:
					shutil.rmtree(EXTRACT_LOCATION)
					error['error_msg']='The file you uploaded does not contain your scrumy project or one of the project files are missing.'
					return(error)						
	else:
		error['error_msg']='Please verify that the file you are uploading corresponds to the format specified in the lab instructions and try again'
		return(error)


def grade_django_lab10(file, lab_number, current_user, topic, course):
	error = {
		'error_msg':'',
	}

	if file.name.endswith('myscrumy.zip') and file.name.startswith('myscrumy'):


		EXTRACT_LOCATION = DJANGO_LAB_SUB_DIR+current_user.username+'_'+str(lab_number)


		result = {
			'task_one_status' : 'undone',
			'task_two_status' : 'undone',
			'task_three_status' : 'undone',
		}

		try:
			zfile = zipfile.ZipFile(file) 
		except zipfile.BadZipfile as ex:
			error['error_msg']='The file you uploaded is a bad zipfile or not a zipfile'
			return(error)
		else:

			'''
				Checks through the entire achive of the opened zifile to pick out any bad member of the achive
			'''
			ret = zfile.testzip()
			if ret is not None:
				error['error_msg']='A file in the zip achive is corrupt'
				return(error)
			else:
				zfile.extractall(EXTRACT_LOCATION)

				PORT = current_user.id+2910
				if check_if_upload_is_django_project(EXTRACT_LOCATION,current_user.username):
					profile = selenium.webdriver.FirefoxProfile()
					profile.accept_untrusted_certs = True
					options = selenium.webdriver.FirefoxOptions()
					options.add_argument('--headless')
					driver = selenium.webdriver.Firefox(firefox_profile=profile, firefox_options=options)
					try:

						create_docker_file(EXTRACT_LOCATION,PORT,current_user.username)

						with open(os.path.join(EXTRACT_LOCATION,'myscrumy/requirements.txt'),'w') as req:
							req.write(REQUIREMENT_TEXT)

						working_dir=os.getcwd()
						
						os.chdir(os.path.join(EXTRACT_LOCATION,'myscrumy'))

						build_and_run_docker(current_user.username,str(lab_number),str(PORT))
					except Exception as e:
						print(e)

					shutil.rmtree(EXTRACT_LOCATION)

					time.sleep(10)

					try:
						driver.get('http:localhost:'+str(PORT)+'/admin')

						driver.find_element_by_name('username').send_keys('louis')
						driver.find_element_by_name('password').send_keys('DJANGO_123')
						driver.find_element_by_xpath('//input[@type="submit"]').click()

						driver.find_element_by_partial_link_text('Goal status').click()
						goal_status_records = driver.find_elements_by_partial_link_text('GoalStatus object')

						record_length = len(goal_status_records)


						count=0
						for rec in range(record_length):
							driver.get('http:localhost:'+str(PORT)+'/admin')
							driver.find_element_by_partial_link_text('Goal status').click()
							goal_status_records = driver.find_elements_by_partial_link_text('GoalStatus object')
							goal_status_records[rec].click()
							x = driver.find_element_by_name('status_name').get_attribute('value').rstrip('\n')
							if x.lower() == 'weekly goal' or x.lower() == 'daily goal' or x.lower() == 'verify goal' or x.lower() == 'done goal':
								count+=1

						if count>3:
							result['task_one_status']='done'
							result['task_two_status']='done'


						driver.get('http:localhost:'+str(PORT)+'/admin')
						driver.find_element_by_partial_link_text('Scrumy goals').click()
						scrumy_goal_records = driver.find_elements_by_partial_link_text('ScrumyGoals object')

						record_length = len(scrumy_goal_records)
						m_list=[]
						count2=0
						for rec in range(record_length):
							driver.get('http:localhost:'+str(PORT)+'/admin')
							driver.find_element_by_partial_link_text('Scrumy goals').click()
							scrumy_goal_records = driver.find_elements_by_partial_link_text('ScrumyGoals object')
							scrumy_goal_records[rec].click()
							goal_name=driver.find_element_by_name('goal_name').get_attribute('value').rstrip('\n')
							goal_id=driver.find_element_by_name('goal_id').get_attribute('value').rstrip('\n')
							created_by=driver.find_element_by_name('created_by').get_attribute('value').rstrip('\n')
							moved_by=driver.find_element_by_name('moved_by').get_attribute('value').rstrip('\n')
							owner=driver.find_element_by_name('owner').get_attribute('value').rstrip('\n')

							m_list.append({'goal_name':goal_name,'goal_id':goal_id,'created_by':created_by,'moved_by':moved_by,'owner':owner})
						for each_entry in m_list:
							if each_entry['goal_name'].lower()=='learn django' and each_entry['goal_id'].lower()=='1' and each_entry['created_by'].lower()=='louis' and each_entry['moved_by'].lower()=='louis' and each_entry['owner'].lower()=='louis':
								result['task_three_status']='done'
					except Exception as e:
						print(e)
					finally:
						driver.quit()

					stop_and_remove_docker_container(current_user.username,str(lab_number))
					save_grade(lab_number, current_user, result)
					return(result)
				else:
					shutil.rmtree(EXTRACT_LOCATION)
					error['error_msg']='The file you uploaded does not contain your scrumy project or one of the project files are missing.'
					return(error)	
	else:
		error['error_msg']='Please verify that the file you are uploading corresponds to the format specified in the lab instructions and try again'
		return(error)



#WORKING WITH DJANGO MODELS
def grade_django_lab9(file, lab_number, current_user, topic, course):
	error = {
		'error_msg':'',
	}
	if file.name.endswith('myscrumy.zip') and file.name.startswith('myscrumy'):

		EXTRACT_LOCATION = DJANGO_LAB_SUB_DIR+current_user.username+'_'+str(lab_number)

		result = {
			'task_one_status' : 'undone',
			'task_two_status' : 'undone',
			'task_three_status' : 'undone',
			'task_four_status': 'undone',
			'task_five_status' : 'undone',
		}


		try:
			zfile = zipfile.ZipFile(file) 
		except zipfile.BadZipfile as ex:
			error['error_msg']='The file you uploaded is a bad zipfile or not a zipfile'
			return(error)
		else:

			'''
				Checks through the entire achive of the opened zifile to pick out any bad member of the achive
			'''
			ret = zfile.testzip()
			if ret is not None:
				error['error_msg']='A file in the zip achive is corrupt'
				return(error)
			else:
				zfile.extractall(EXTRACT_LOCATION)

				PORT = current_user.id+2910
				if check_if_upload_is_django_project(EXTRACT_LOCATION,current_user.username):
					profile = selenium.webdriver.FirefoxProfile()
					profile.accept_untrusted_certs = True
					options = selenium.webdriver.FirefoxOptions()
					options.add_argument('--headless')
					driver = selenium.webdriver.Firefox(firefox_profile=profile, firefox_options=options)
					try:

						create_docker_file(EXTRACT_LOCATION,PORT,current_user.username)

						with open(os.path.join(EXTRACT_LOCATION,'myscrumy/requirements.txt'),'w') as req:
							req.write(REQUIREMENT_TEXT)

						working_dir=os.getcwd()
						
						os.chdir(os.path.join(EXTRACT_LOCATION,'myscrumy'))

						build_and_run_docker(current_user.username,str(lab_number),str(PORT))
					except Exception as e:
						print(e)

					shutil.rmtree(EXTRACT_LOCATION)

					time.sleep(10)

					#log into users project admin page (localhost:PORT/admin)
					
					
					try:
						driver.get('http:localhost:'+str(PORT)+'/admin')

						driver.find_element_by_name('username').send_keys('louis')
						driver.find_element_by_name('password').send_keys('DJANGO_123')
						driver.find_element_by_xpath('//input[@type="submit"]').click()

						goal_status = driver.find_element_by_partial_link_text('Goal status').get_attribute('innerHTML').rstrip('\n')
						scrumy_goals = driver.find_element_by_partial_link_text('Scrumy goals').get_attribute('innerHTML').rstrip('\n')
						scrumy_history = driver.find_element_by_partial_link_text('Scrumy historys').get_attribute('innerHTML').rstrip('\n')
						if goal_status=='Goal statuss' and scrumy_goals=='Scrumy goalss' and scrumy_history=='Scrumy historys':
							result['task_one_status']='done'
							result['task_five_status']='done'


						driver.find_element_by_partial_link_text('Scrumy goals').click()
						driver.find_element_by_class_name('addlink').click()
						goal_name = driver.find_element_by_name('goal_name').get_attribute('name')
						goal_id = driver.find_element_by_name('goal_id').get_attribute('name')
						created_by = driver.find_element_by_name('created_by').get_attribute('name')
						moved_by = driver.find_element_by_name('moved_by').get_attribute('name')
						owner = driver.find_element_by_name('owner').get_attribute('name')

						driver.get('http://localhost:'+str(PORT)+'/admin')
						driver.find_element_by_partial_link_text('Goal status').click()
						driver.find_element_by_class_name('addlink').click()
						status_name = driver.find_element_by_name('status_name').get_attribute('name')

						driver.get('http://localhost:'+str(PORT)+'/admin')
						driver.find_element_by_partial_link_text('Scrumy history').click()
						driver.find_element_by_class_name('addlink').click()
						h_created_by = driver.find_element_by_name('created_by').get_attribute('name')
						h_moved_by = driver.find_element_by_name('moved_by').get_attribute('name')
						h_moved_from = driver.find_element_by_name('moved_from').get_attribute('name')
						h_moved_to = driver.find_element_by_name('moved_to').get_attribute('name')
						#time_0 = driver.find_element_by_name('time_of_action_0').get_attribute('name')
						#time_1 = driver.find_element_by_name('time_of_action_1').get_attribute('name')	
						if goal_name=='goal_name' and goal_id=='goal_id' and created_by=='created_by' and moved_by=='moved_by' and owner=='owner' and status_name == 'status_name' and h_moved_to=='moved_to' and h_moved_from=='moved_from' and h_moved_by=='moved_by'and h_created_by=='created_by':
							result['task_two_status']='done'

						driver.get('http:localhost:'+str(PORT)+'/admin')
						driver.find_element_by_partial_link_text('Scrumy goals').click()
						driver.find_element_by_class_name('addlink').click()
						goal_status_2 = driver.find_element_by_name('goal_status').get_attribute('name')
						usr = driver.find_element_by_name('user').get_attribute('name')

						driver.get('http://localhost:'+str(PORT)+'/admin')
						driver.find_element_by_partial_link_text('Scrumy history').click()
						driver.find_element_by_class_name('addlink').click()
						goal = driver.find_element_by_name('goal').get_attribute('name')

						if usr == 'user':
							result['task_three_status']='done'

						if usr=='user' and goal_status_2=='goal_status' and goal=='goal':
							result['task_four_status']='done'

						driver.close()
					except Exception as e:
						print(e)
					finally:
						driver.quit()
					stop_and_remove_docker_container(current_user.username,str(lab_number))
					save_grade(lab_number, current_user, result)
					return(result)
				else:
					shutil.rmtree(EXTRACT_LOCATION)
					error['error_msg']='The file you uploaded does not contain your scrumy project or one of the project files are missing.'
					return(error)	
	else:
		error['error_msg']='Please verify that the file you are uploading corresponds to the format specified in the lab instructions and try again'
		return(error)



#CREATING DJANGO VIEWS
def grade_django_lab8(file, lab_number, current_user, topic, course):
	error = {
		'error_msg':'',
	}
	if file.name.endswith('myscrumy.zip') and file.name.startswith('myscrumy'):

		EXTRACT_LOCATION = DJANGO_LAB_SUB_DIR+current_user.username+'_'+str(lab_number)

		result = {
			'task_one_status' : 'undone',
		}


		try:
			zfile = zipfile.ZipFile(file) 
		except zipfile.BadZipfile as ex:
			error['error_msg']='The file you uploaded is a bad zipfile or not a zipfile'
			return(error)
		else:


			'''
				Checks through the entire achive of the opened zifile to pick out any bad member of the achive
			'''
			ret = zfile.testzip()
			if ret is not None:
				error['error_msg']='A file in the zip achive is corrupt'
				return(error)
			else:
				zfile.extractall(EXTRACT_LOCATION)

				PORT = current_user.id+2910
				if check_if_upload_is_django_project(EXTRACT_LOCATION,current_user.username):
					profile = selenium.webdriver.FirefoxProfile()
					profile.accept_untrusted_certs = True
					options = selenium.webdriver.FirefoxOptions()
					options.add_argument('--headless')
					driver = selenium.webdriver.Firefox(firefox_profile=profile, firefox_options=options)
					try:
						create_docker_file(EXTRACT_LOCATION,PORT,current_user.username)

						with open(os.path.join(EXTRACT_LOCATION,'myscrumy/requirements.txt'),'w') as req:
							req.write(REQUIREMENT_TEXT)

						working_dir=os.getcwd()
						
						os.chdir(os.path.join(EXTRACT_LOCATION,'myscrumy'))

						build_and_run_docker(current_user.username,str(lab_number),str(PORT))
					except Exception as e:
						print(e)

					shutil.rmtree(EXTRACT_LOCATION)

					time.sleep(10)

					try:
						driver.get('http://localhost:'+str(PORT)+'/'+current_user.username+'scrumy')
						elem = driver.find_element_by_xpath('//body')
						if elem:
							result['task_one_status']='done'
					except Exception as e:
						print(e)
					finally:
						driver.quit()
					stop_and_remove_docker_container(current_user.username,str(lab_number))
					save_grade(lab_number, current_user, result)
					return(result)
				else:
					shutil.rmtree(EXTRACT_LOCATION)
					error['error_msg']='The file you uploaded does not contain your scrumy project or one of the project files are missing.'
					return(error)					
	else:
		error['error_msg']='Please verify that the file you are uploading corresponds to the format specified in the lab instructions and try again'
		return(error)


'''
 Making your Django application reusable for other projects.
'''
def grade_django_lab7(file, lab_number, current_user, topic, course):

	error = {
		'error_msg':'',
	}

	result = {
		'task_one_status' : 'undone',
		'task_two_status' : 'undone',
		'task_three_status' : 'undone',
		'task_four_status' : 'undone',
		'task_five_status' : 'undone',
		'task_six_status' : 'undone',
		'task_seven_status' : 'undone',
	}

	EXTRACT_LOCATION = DJANGO_LAB_SUB_DIR+current_user.username+'_'+str(lab_number)

	if file.name.endswith('.zip'):
		try:
			zfile = zipfile.ZipFile(file) 
		except zipfile.BadZipfile as ex:
			error['error_msg']='The file you uploaded is a bad zipfile or not a zipfile'
			return(error)

		'''
			Checks through the entire achive of the opened zifile to pick out any bad member of the achive
		'''
		ret = zfile.testzip()
		if ret is not None:
			error['error_msg']='A file in the zip achive is corrupt'
			return(error)
		else:
			zfile.extractall(EXTRACT_LOCATION)
			for root, dirs, files in os.walk(EXTRACT_LOCATION):
				for afile in files:
					if afile.endswith('top_level.txt') or afile.endswith('sources.txt') or afile.endswith('dependency_links.txt'):
						result['task_one_status']='done'
					if afile.endswith('README.rst'):
						result['task_three_status']='done'
					if afile.endswith('setup.py'):
						result['task_four_status']='done'
					if afile.endswith('PKG-INFO'): #come back here louis.
						result['task_five_status']='done'
					if afile.endswith('MANIFEST.in'):
						result['task_six_status']='done'

				for dirname in dirs:
					if dirname.startswith('django_'+current_user.username+'scrumy'):
						result['task_two_status']='done'
			print(file)
			if file.name.endswith('.zip'):
				result['task_seven_status']='done'
			save_grade(lab_number, current_user, result)
			shutil.rmtree(EXTRACT_LOCATION)
			return(result)
	else:
		error['error_msg']='Please verify that the file you are uploading corresponds to the format specified in the lab instructions and try again'
		return(error)





def grade_django_lab6(file, lab_number, current_user, topic, course):

	match_count = 0
	mark = 0

	result = {
		'task_one_status' : 'undone',
	}

	error = {
		'error_msg':'',
	}

	if file.name.endswith('.sql'):
		with open(os.path.join(DJANGO_LAB_SUB_DIR, current_user.username+'_'+str(lab_number)),'w') as db_file:
			db_file.write('')

		with open(os.path.join(DJANGO_LAB_SUB_DIR, current_user.username+'_'+str(lab_number)), 'wb+') as destination:
			for chunk in file.chunks():
				destination.write(chunk)

		with open(os.path.join(DJANGO_LAB_SUB_DIR, current_user.username+'_'+str(lab_number)),'r') as db_file:
			for eachline in db_file:
				if eachline.rstrip('\n') == "INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES":
					match_count +=1
				if match_count > 0:
					result['task_one_status']='done'
		save_grade(lab_number, current_user, result)
		os.remove(os.path.join(DJANGO_LAB_SUB_DIR, current_user.username+'_'+str(lab_number)))
		return(result)
	else:
		error['error_msg']='The file you uploaded is not an sql document'
		return(error)




def grade_django_lab5(file, lab_number, current_user, topic, course):
	match_count = 0
	grade = ''
	mark = 0

	result = {
		'task_one_status' : 'undone',
		'task_two_status' : 'undone',
		'task_three_status' : 'undone',
		'task_four_status' : 'undone',
	}

	error = {
		'error_msg':'',
	}
	if file.name.endswith('.sql'):
		with open(os.path.join(DJANGO_LAB_SUB_DIR, current_user.username+'_'+str(lab_number)),'w') as db_file:
			db_file.write('')

		with open(os.path.join(DJANGO_LAB_SUB_DIR, current_user.username+'_'+str(lab_number)), 'wb+') as destination:
			for chunk in file.chunks():
				destination.write(chunk)

		with open(os.path.join(DJANGO_LAB_SUB_DIR, current_user.username+'_'+str(lab_number)),'r') as db_file:
			for eachline in db_file:
				if eachline.rstrip('\n') == "CREATE TABLE IF NOT EXISTS `django_migrations` (" or eachline.rstrip('\n') == "CREATE TABLE `django_migrations` (" or eachline.rstrip('\n') == "CREATE TABLE IF NOT EXISTS `django_session` (" or eachline.rstrip('\n') == "CREATE TABLE `django_session` (":
					match_count +=1
				if match_count > 0:
					result['task_one_status']='done'
					result['task_two_status']='done'
					result['task_three_status']='done'
					result['task_four_status']='done'
					
		save_grade(lab_number, current_user, result)
		os.remove(os.path.join(DJANGO_LAB_SUB_DIR, current_user.username+'_'+str(lab_number)))
		return(result)
	else:
		error['error_msg']='The file you uploaded is not an sql document'
		return(error)





def grade_django_lab4(file, lab_number, current_user, topic, course):
	zfile = ''
	zfile_name = file.name
	exfile_name = zfile_name.rstrip('.zip')
	count = 0
	grade = ''
	mark = 0

	error = {
		'error_msg':'',
	}

	result = {
		'task_one':'undone',
		'task_two':'undone',
	}

	EXTRACT_LOCATION = DJANGO_LAB_SUB_DIR+current_user.username+'_'+str(lab_number)

	if zfile_name.endswith('.zip') and zfile_name.startswith('myscrumy'):	#Checks if uploaded file is of the format myscrumy.zip
		'''Opens the uploaded zipfile but if file cant be opened then its a bad zipfile'''
		try:
			zfile = zipfile.ZipFile(file) 
		except zipfile.BadZipfile as ex:
			error['error_msg']='The file you uploaded is a bad zipfile or not a zipfile'
			return(error)

		'''
			Checks through the entire achive of the opened zifile to pick out any bad member of the achive
		'''
		ret = zfile.testzip()
		if ret is not None:
			error['error_msg']='A file in the zip achive is corrupt'
			return(error)
		else:
			zfile.extractall(EXTRACT_LOCATION)

		try:
			with open(EXTRACT_LOCATION+'/myscrumy/myscrumy/settings.py', 'r') as settings_file:
				for eachline in settings_file:
					if eachline.rstrip('\n') == "        'ENGINE': 'django.db.backends.sqlite3'," or eachline.rstrip('\n') == "        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),":
						count += 1

			if count > 0:
				result['task_one'] = 'done'
				result['task_two'] = 'done'
				save_grade(lab_number, current_user, result)
		except FileNotFoundError:
			print('error here')
			error['error_msg']='settings.py file is missing'
			return(error)
		shutil.rmtree(EXTRACT_LOCATION)
		return(result)
	else:
		error['error_msg']='Please verify that the file you are uploading corresponds to the format specified in the lab instructions and try again'
		return(error)





def grade_django_lab3(file, lab_number, current_user, topic, course):
	zfile = ''
	zfile_name = file.name
	exfile_name = zfile_name.rstrip('.zip')
	task_1= 0
	task_2 = 0
	task_3 = 0
	task_4 = 0
	task_5 = 0
	task_6 = 0
	grade = ''
	mark = 0
	result = {
		'task_one_status' : 'undone',
		'task_two_status' : 'undone',
		'task_three_status' : 'undone',
		'task_four_status' : 'undone',
		'task_five_status' : 'undone',
		'task_six_status' : 'undone',
	}
	error = {
		'error_msg':'',
	}


	EXTRACT_LOCATION = DJANGO_LAB_SUB_DIR+current_user.username+'_'+str(lab_number)


	if zfile_name.endswith('.zip') and zfile_name.startswith('myscrumy'):	#Checks if uploaded file is of the format myscrumy.zip
		'''Opens the uploaded zipfile but if file cant be opened then its a bad zipfile'''
		try:
			zfile = zipfile.ZipFile(file) 
		except zipfile.BadZipfile as ex:
			error['error_msg']='The file you uploaded is a bad zipfile or not a zipfile'
			return(error)

		'''
			Checks through the entire achive of the opened zifile to pick out any bad member of the achive
		'''
		ret = zfile.testzip()
		if ret is not None:
			error['error_msg']='A file in the zip achive is corrupt'
			return(error)
		else:
			zfile.extractall(EXTRACT_LOCATION)

			for root, dirs, files in os.walk(EXTRACT_LOCATION):
				for dirnames in dirs:
					if dirnames == 'myscrumy':
						result['task_one_status'] = 'done'
				for dirnames in dirs:
					if dirnames == current_user.username + 'scrumy':
						task_3 += 1
				for file in files:
					if file.endswith('dmin.py') or file.endswith('odels.py') or file.endswith('iews.py') or file.endswith('ests.py') or file.endswith('pps.py'):
						task_3 += 1
				for file in files:
					if file.endswith('rls.py'):
						task_4 += 1
			try:
				with open(os.path.join(EXTRACT_LOCATION, 'myscrumy/myscrumy/urls.py'), 'r') as project_url:
					for eachline in project_url:
						
						if eachline.rstrip('\n') == "	path('"+current_user.username+"scrumy/', include("+'"'+current_user.username+'scrumy.urls")),' or eachline.rstrip('\n') == "	path('"+current_user.username+"scrumy/', include('"+current_user.username+"scrumy.urls'))," or eachline.rstrip('\n') == '	path("'+current_user.username+'scrumy/", include('+"'"+current_user.username+"scrumy.urls'))," or eachline.rstrip('\n') == '	path("'+current_user.username+'scrumy/", include("'+current_user.username+'scrumy.urls")),':
							result['task_five_status'] = 'done'
			except FileNotFoundError:
				print('file not found')
			try:
				with open(os.path.join(EXTRACT_LOCATION, 'myscrumy/'+current_user.username+'scrumy/urls.py'), 'r') as app_url:
					print(eachline)
					for eachline in app_url:
						if eachline.rstrip('\n') == "	path('', views.index)," or eachline.rstrip('\n') == '	path("", views.index),':
							result['task_six_status'] = 'done'
			except FileNotFoundError:
				print('error')
			shutil.rmtree(EXTRACT_LOCATION)


			if task_3 > 5 or task_3 == 6:
				result['task_three_status'] = 'done'

			if result['task_three_status'] == 'done':
				result['task_two_status'] = 'done'

			if task_4 > 1:
				result['task_four_status'] = 'done'

			save_grade(lab_number, current_user, result)
			return (result)
	else:
		error['error_msg']='The file you uploaded is a bad zipfile or not a zipfile'
		return(error)

	

	






def grade_django_lab2(file, lab_number, current_user):

	'''count = 0
	grade = 0
	mark = 0

	if file.name.rstrip('\n').endswith('.txt'):
		
		try:
			with open(os.path.join(PROJECT_MEDIA_DIR, file.name), 'r') as fil:
				for eachline in fil:
					if eachline.rstrip('\n') == 'Django==2.0.1':
						count += 1
			
			if count > 1:
				grade = 'Passed'
				mark = 100
			else:
				grade = 'Failed'
				mark = 0
		except Exception as e:
			grade = 'Failed'
			mark = 0
			print(e)
	else:
		grade = 'Failed'
		mark = 0

	save_grade(lab_number, mark, current_user, grade)'''
	return ('You dont need to submit this, Procede with lab 3')









def display_django_result(course, lab_number, current_user):

	score=0
	percent=0
	stat=0
	leng=0
	topic=CourseTopic.objects.get(course__course_title = course, topic_number = lab_number)
	try:
		next_topic=CourseTopic.objects.get(course__course_title = course, topic_number = int(lab_number)+1)
	except CourseTopic.DoesNotExist:
		next_topic=None

	grades=GradesReport.objects.filter(user=current_user, course_topic=topic)
	for grade in grades:
		leng=leng+1
		if grade.grade=="passed":
			score=score+1
	if leng==0:
		stat="Not attempted"
	else:
		percent=(score/leng)*100

		if percent > 70:
			stat="passed"
		else:
			stat="Failed"

    #check if still grading
	'''for grade in grades:
		for gra in grade:
			if gra.grade == "Grading":
			    stat = "Grading" '''

	context = {
	    'topic' : topic,
	    'result' : GradesReport.objects.filter(user=current_user,course_topic=topic),
	    'related_topic': CourseTopic.objects.filter(course=topic.course),
	    'course_name' : course,
	    'lab_no': lab_number,
	    'next_topic': next_topic,
	    'percent': int(percent),
	    'stat': stat,
	}
	return (context)


def grade_django_lab(file, lab_number, current_user, topic, course):


	if lab_number == 3:
		grade = grade_django_lab3(file, lab_number, current_user, topic, course)
		context=display_django_result(course, lab_number, current_user)
		return (context)
	elif lab_number == 4:
		grade = grade_django_lab4(file, lab_number, current_user, topic, course)
		context=display_django_result(course, lab_number, current_user)
		return (context)
	elif lab_number == 5:
		grade = grade_django_lab5(file, lab_number, current_user, topic, course)
		context=display_django_result(course, lab_number, current_user)
		return (context)
	elif lab_number == 6:
		grade = grade_django_lab6(file, lab_number, current_user, topic, course)
		context=display_django_result(course, lab_number, current_user)
		return (context)
	elif lab_number == 7:
		grade = grade_django_lab7(file, lab_number, current_user, topic, course)
		context=display_django_result(course, lab_number, current_user)
		return (context)
	elif lab_number == 8:
		grade = grade_django_lab8(file, lab_number, current_user, topic, course)
		context=display_django_result(course, lab_number, current_user)
		return (context)
	elif lab_number == 9:
		grade = grade_django_lab9(file, lab_number, current_user, topic, course)
		context=display_django_result(course, lab_number, current_user)
		return (context)
	elif lab_number == 10:
		grade = grade_django_lab10(file, lab_number, current_user, topic, course)
		context=display_django_result(course, lab_number, current_user)
		return (context)
	elif lab_number == 11:
		grade = grade_django_lab11(file, lab_number, current_user, topic, course)
		context=display_django_result(course, lab_number, current_user)
		return (context)
	elif lab_number == 12:
		grade = grade_django_lab12(file, lab_number, current_user, topic, course)
		context=display_django_result(course, lab_number, current_user)
		return (context)
	elif lab_number == 13:
		grade = grade_django_lab13(file, lab_number, current_user, topic, course)
		context=display_django_result(course, lab_number, current_user)
		return (context)
	elif lab_number == 14:
		grade = grade_django_lab14(file, lab_number, current_user, topic, course)
		context=display_django_result(course, lab_number, current_user)
		return (context)
	elif lab_number == 15:
		grade = grade_django_lab15(file, lab_number, current_user, topic, course)
		context=display_django_result(course, lab_number, current_user)
		return (context)
	elif lab_number == 16:
		grade = grade_django_lab16(file, lab_number, current_user, topic, course)
		context=display_django_result(course, lab_number, current_user)
		return (context)
	elif lab_number == 17:
		grade = grade_django_lab17(file, lab_number, current_user, topic, course)
		context=display_django_result(course, lab_number, current_user)
		return (context)
	elif lab_number == 18:
		grade = grade_django_lab18(file, lab_number, current_user, topic, course)
		context=display_django_result(course, lab_number, current_user)
		return (context)
	elif lab_number == 19:
		grade = grade_django_lab19(file, lab_number, current_user, topic, course)
		context=display_django_result(course, lab_number, current_user)
		return (context)
	elif lab_number == 20:
		grade = grade_django_lab20(file, lab_number, current_user, topic, course)
		context=display_django_result(course, lab_number, current_user)
		return (context)
	elif lab_number == 21:
		grade = grade_django_lab21(file, lab_number, current_user, topic, course)
		context=display_django_result(course, lab_number, current_user)
		return (context)
	else:
		return ('Invalid request')
