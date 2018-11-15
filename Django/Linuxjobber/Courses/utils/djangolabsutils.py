import shutil
import subprocess
import sys
import zipfile
import logging

from os import fdopen, remove
from shutil import move
from tempfile import mkstemp

import selenium
import selenium.webdriver
import django
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from Courses.models import *

#from selenium import webdriver

os.environ.setdefault("_SETTINGS_MODULE","server.settings")



############################################################################################################################################################
# Construction of projects directories/paths.
############################################################################################################################################################
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APPLICATION_DIR = os.path.join(BASE_DIR, 'Courses')
PROJECT_DIR = os.path.join(BASE_DIR, 'Linuxjobber')
PROJECT_MEDIA_DIR = os.path.join(BASE_DIR, 'media/uploads') # Directory that contains projects media
MEDIA_DIR = os.path.join(APPLICATION_DIR, 'media') #Directory that contains media exclucive to DjangoLabs Application
VERYFD_BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),'veryfd') #Project to install students application 
VERYFD_PROJECT_DIR = os.path.join(VERYFD_BASE_DIR, 'veryfd') #Verifyd project directory containing the settings.py and urls.py

############################################################################################################################################################


VERYFD_ADDRESS = 'http://127.0.0.1:8005/'

os.environ['PATH'] += ':' + PROJECT_DIR + '__init__.py'

#--------------------------------------------------------------------------------------------------------
#FUNCTIONS
#--------------------------------------------------------------------------------------------------------
def replace(file_path, pattern, subst):
	fh, abs_path = mkstemp()
	with fdopen(fh,'w') as new_file:
		with open(file_path) as old_file:
			for line in old_file:
				new_file.write(line.replace(pattern,subst))
	remove(file_path)
	move(abs_path, file_path)

def save_grade(lab_number, mark, current_user, grade):
	course_topic = CourseTopic.objects.get(topic_number = lab_number, course_id = 1)
	report = GradesReport(score = str(mark), course_topic = course_topic, user_id = current_user.id, grade = str(grade))
	report.save()
	#print('saved grade')


#-------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------
# Logging Instances
#----------------------------------------------------------------------------------------------------------

standard_logger = logging.getLogger(__name__)
dbalogger = logging.getLogger('dba')


#-----------------------------------------------------------------------------------------------------------




def grade_django_lab20(file, lab_number, current_user):


	try:
		lab19 = CourseTopic.objects.get(topic_number = 19)
		check_lab19_status = ''
		check_lab19_status = GradesReport.objects.get(course_topic_id = lab19, user_id = current_user, grade = 'Passed')
	except ObjectDoesNotExist:
		check_lab19_status = ''
	except MultipleObjectsReturned:
		check_lab19_status = 'MultipleObjects'
	
	file_upload = ''
	xpected_app_name = current_user.username + 'scrumy'
	grade = ''
	mark = 0
	file_name = ''

	if file.name.endswith('.zip'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.zip')
		file_name = file.name.split('-')[1]
	elif file.name.endswith('.gz'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.gz')
		file_name = file.name.split('-')[1]
	else:
		file_name = ''


	if check_lab19_status != '' or check_lab19_status == 'MultipleObjects':
		if xpected_app_name == file_name:
			dp = 0
			try:
				subprocess.call([sys.executable, "-m", "pip", "install", file_upload])
			except Exception as e:
				dp += 1
			finally:
				os.remove(file_upload)
			
			if dp < 1:
				options = webdriver.ChromeOptions()
				options.add_argument("headless")
				driver = webdriver.Chrome(chrome_options = options)
				try:
					driver.get(VERYFD_ADDRESS+xpected_app_name)
					fname = driver.find_element_by_name('first_name').get_attribute('name')
					lname = driver.find_element_by_name('last_name').get_attribute('name')
					email = driver.find_element_by_name('email').get_attribute('name')
					uname = driver.find_element_by_name('username').get_attribute('name')
					pword = driver.find_element_by_name('password').get_attribute('name')
				except Exception as e:
					print (e)
				if fname.startswith('first') and lname.startswith('last') and email.startswith('emai') and uname.startswith('user') and pword.startswith('passw'):
					grade = "Passed"
					mark = 100
				else:
					print('Failed')
					grade = 'Failed'
					mark = 0
				save_grade(lab_number, mark, current_user, grade)
				return(grade)
			else:

				return('Something went wrong please try again')
		else:
			os.remove(file_upload)
			return("The name of the file you are submitting should be of the format 'django-your linuxjobber username+scrumy-x.x' where x is an integer value and - is an hyphen")
	else:
		os.remove(file_upload)
		return('You have not completed Lab 18 please do so to procede with this lab')


def grade_django_lab19(file, lab_number, current_user):


	try:
		lab18 = CourseTopic.objects.get(topic_number = 18)
		check_lab18_status = ''
		check_lab18_status = GradesReport.objects.get(course_topic_id = lab18, user_id = current_user, grade = 'Passed')
	except ObjectDoesNotExist:
		check_lab18_status = ''
	except MultipleObjectsReturned:
		check_lab18_status = 'MultipleObjects'
	
	file_upload = ''
	xpected_app_name = current_user.username + 'scrumy'
	grade = ''
	mark = 0
	file_name = ''

	if file.name.endswith('.zip'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.zip')
		file_name = file.name.split('-')[1]
	elif file.name.endswith('.gz'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.gz')
		file_name = file.name.split('-')[1]
	else:
		file_name = ''


	if check_lab18_status != '' or check_lab18_status == 'MultipleObjects':
		if xpected_app_name == file_name:
			dp = 0
			try:
				subprocess.call([sys.executable, "-m", "pip", "install", file_upload])
			except Exception as e:
				dp += 1
			finally:
				os.remove(file_upload)
			
			if dp < 1:
				options = webdriver.ChromeOptions()
				options.add_argument("headless")
				driver = webdriver.Chrome(chrome_options = options)
				try:
					driver.get(VERYFD_ADDRESS+xpected_app_name)
					fname = driver.find_element_by_name('first_name').get_attribute('name')
					lname = driver.find_element_by_name('last_name').get_attribute('name')
					email = driver.find_element_by_name('email').get_attribute('name')
					uname = driver.find_element_by_name('username').get_attribute('name')
					pword = driver.find_element_by_name('password').get_attribute('name')

					driver.get(VERYFD_ADDRESS+xpected_app_name+'/home')
					driver.find_element_by_xpath('//a').click()
					gname = driver.find_element_by_name('goal_name').get_attribute('name')
					user = driver.find_element_by_name('user').get_attribute('name')

				except Exception as e:
					print (e)
				if fname.startswith('first') and lname.startswith('last') and email.startswith('emai') and uname.startswith('user') and pword.startswith('passw') and gname.startswith('goal') and user.startswith('us'):
					grade = "Passed"
					mark = 100
				else:
					print('Failed')
					grade = 'Failed'
					mark = 0
				save_grade(lab_number, mark, current_user, grade)
				return(grade)
			else:

				return('Something went wrong please try again')
		else:
			os.remove(file_upload)
			return("The name of the file you are submitting should be of the format 'django-your linuxjobber username+scrumy-x.x' where x is an integer value and - is an hyphen")
	else:
		os.remove(file_upload)
		return('You have not completed Lab 18 please do so to procede with this lab')
















def grade_django_lab18(file, lab_number, current_user):


	try:
		lab17 = CourseTopic.objects.get(topic_number = 17)
		check_lab17_status = ''
		check_lab17_status = GradesReport.objects.get(course_topic_id = lab17, user_id = current_user, grade = 'Passed')
	except ObjectDoesNotExist:
		check_lab17_status = ''
	except MultipleObjectsReturned:
		check_lab17_status = 'MultipleObjects'
	
	file_upload = ''
	xpected_app_name = current_user.username + 'scrumy'
	grade = ''
	mark = 0
	file_name = ''

	if file.name.endswith('.zip'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.zip')
		file_name = file.name.split('-')[1]
	elif file.name.endswith('.gz'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.gz')
		file_name = file.name.split('-')[1]
	else:
		file_name = ''


	if check_lab17_status != '' or check_lab17_status == 'MultipleObjects':
		if xpected_app_name == file_name:
			dp = 0
			try:
				subprocess.call([sys.executable, "-m", "pip", "install", file_upload])
			except Exception as e:
				dp += 1
			finally:
				os.remove(file_upload)
			
			if dp < 1:
				options = webdriver.ChromeOptions()
				options.add_argument("headless")
				driver = webdriver.Chrome(chrome_options = options)
				csrf_t = ''
				try:
					driver.get(VERYFD_ADDRESS+xpected_app_name+'/accounts/login')
					form_method = driver.find_element_by_xpath('//form').get_attribute('method')
					csrf_t = driver.find_element_by_name('csrfmiddlewaretoken').get_attribute('type')
				except Exception as e:
					print (e)
				if form_method == 'post' or form_method == 'POST' or form_method == 'Post' and csrf_t == 'hidden':
					grade = "Passed"
					mark = 100
				else:
					print('Failed')
					grade = 'Failed'
					mark = 0
				save_grade(lab_number, mark, current_user, grade)
				return(grade)
			else:

				return('Something went wrong please try again')
		else:
			os.remove(file_upload)
			return("The name of the file you are submitting should be of the format 'django-your linuxjobber username+scrumy-x.x' where x is an integer value and - is an hyphen")
	else:
		os.remove(file_upload)
		return('You have not completed Lab 17 please do so to procede with this lab')




def grade_django_lab17(file, lab_number, current_user):
	try:
		lab16 = CourseTopic.objects.get(topic_number = 16)
		check_lab16_status = ''
		check_lab16_status = GradesReport.objects.get(course_topic_id = lab16, user_id = current_user, grade = 'Passed')
	except ObjectDoesNotExist:
		check_lab16_status = ''
	except MultipleObjectsReturned:
		check_lab16_status = 'MultipleObjects'		
	
	file_upload = ''
	xpected_app_name = current_user.username + 'scrumy'
	grade = ''
	mark = 0
	file_name = ''

	if file.name.endswith('.zip'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.zip')
		file_name = file.name.split('-')[1]
	elif file.name.endswith('.gz'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.gz')
		file_name = file.name.split('-')[1]
	else:
		file_name = ''


	if check_lab16_status != '' or check_lab16_status == 'MultipleObjects':
		if xpected_app_name == file_name:
			dp = 0
			try:
				subprocess.call([sys.executable, "-m", "pip", "install", file_upload])
			except Exception as e:
				dp += 1
			finally:
				os.remove(file_upload)
			
			if dp < 1:
				options = webdriver.ChromeOptions()
				options.add_argument("headless")
				driver = webdriver.Chrome(chrome_options = options)
				html = ''
				try:
					driver.get(VERYFD_ADDRESS+xpected_app_name+'/accounts/login')
					html = driver.find_element_by_xpath('//a')
					check = html.get_attribute('innerHTML')
					html.click()
				except Exception as e:
					print (e)
				if html != '':
					grade = "Passed"
					mark = 100
				else:
					print('Failed')
					grade = 'Failed'
					mark = 0
				save_grade(lab_number, mark, current_user, grade)
				return(grade)
			else:

				return('Something went wrong please try again')
		else:
			os.remove(file_upload)
			return("The name of the file you are submitting should be of the format 'django-your linuxjobber username+scrumy-x.x' where x is an integer value and - is an hyphen")
	else:
		os.remove(file_upload)
		return('You have not completed Lab 16 please do so to procede with this lab')





def grade_django_lab16(file, lab_number, current_user):

	try:
		lab15 = CourseTopic.objects.get(topic_number = 15)
		check_lab15_status = ''
		check_lab15_status = GradesReport.objects.get(course_topic_id = lab15, user_id = current_user, grade = 'Passed')
	except ObjectDoesNotExist:
		check_lab15_status = ''
	except MultipleObjectsReturned:
		check_lab15_status = 'MultipleObjects'		
	
	file_upload = ''
	xpected_app_name = current_user.username + 'scrumy'
	grade = ''
	mark = 0
	file_name = ''

	if file.name.endswith('.zip'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.zip')
		file_name = file.name.split('-')[1]
	elif file.name.endswith('.gz'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.gz')
		file_name = file.name.split('-')[1]
	else:
		file_name = ''


	if check_lab15_status != '' or check_lab15_status == 'MultipleObjects':
		if xpected_app_name == file_name:
			dp = 0
			try:
				subprocess.call([sys.executable, "-m", "pip", "install", file_upload])
			except Exception as e:
				dp += 1
			finally:
				os.remove(file_upload)
			
			if dp < 1:
				options = webdriver.ChromeOptions()
				options.add_argument("headless")
				driver = webdriver.Chrome(chrome_options = options)
				verify_goal_find_split = []
				done_goal_find_split = []
				verify_goal_find = ''
				done_goal_find = ''
				try:
					driver.get(VERYFD_ADDRESS+xpected_app_name+'/home')
					verify_goal_find = driver.find_element_by_xpath("//tr[2]/td[4]").get_attribute('innerHTML')
					done_goal_find = driver.find_element_by_xpath("//tr[2]/td[5]").get_attribute('innerHTML')
					verify_goal_find_split = verify_goal_find.split('T')
					done_goal_find_split = done_goal_find.split('T')
				except Exception as e:
					print (e)
				if verify_goal_find_split[1].startswith('est') and done_goal_find_split[1].startswith('est'):
					grade = "Passed"
					mark = 100
				else:
					print('Failed')
					grade = 'Failed'
					mark = 0
				save_grade(lab_number, mark, current_user, grade)
				return(grade)
			else:

				return('Something went wrong please try again')
		else:
			os.remove(file_upload)
			return("The name of the file you are submitting should be of the format 'django-your linuxjobber username+scrumy-x.x' where x is an integer value and - is an hyphen")
	else:
		os.remove(file_upload)
		return('You have not completed Lab 15 please do so to procede with this lab')






def grade_django_lab15(file, lab_number, current_user):

	try:
		lab14 = CourseTopic.objects.get(topic_number = 14)
		check_lab14_status = ''
		check_lab14_status = GradesReport.objects.get(course_topic_id = lab14, user_id = current_user, grade = 'Passed')
	except ObjectDoesNotExist:
		check_lab14_status = ''
	except MultipleObjectsReturned:
		check_lab14_status = 'MultipleObjects'		
	
	file_upload = ''
	xpected_app_name = current_user.username + 'scrumy'
	grade = ''
	mark = 0
	file_name = ''

	if file.name.endswith('.zip'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.zip')
		file_name = file.name.split('-')[1]
	elif file.name.endswith('.gz'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.gz')
		file_name = file.name.split('-')[1]
	else:
		file_name = ''


	if check_lab14_status != '' or check_lab14_status == 'MultipleObjects':
		if xpected_app_name == file_name:
			dp = 0
			try:
				subprocess.call([sys.executable, "-m", "pip", "install", file_upload])
			except Exception as e:
				dp += 1
			finally:
				os.remove(file_upload)
			
			if dp < 1:
				options = webdriver.ChromeOptions()
				options.add_argument("headless")
				driver = webdriver.Chrome(chrome_options = options)
				html = ''
				try:
					driver.get(VERYFD_ADDRESS+xpected_app_name+"/movegoal/100")
					html = driver.find_element_by_xpath('//body').get_attribute('innerHTML')
				except Exception as e:
					print (e)
				if html.rstrip('\n').lower().endswith('a record with that goal id does not exist'):
					grade = "Passed"
					mark = 100
				else:
					print('Failed')
					grade = 'Failed'
					mark = 0
				save_grade(lab_number, mark, current_user, grade)
				return(grade)
			else:

				return('Something went wrong please try again')
		else:
			os.remove(file_upload)
			return("The name of the file you are submitting should be of the format 'django-your linuxjobber username+scrumy-x.x' where x is an integer value and - is an hyphen")
	else:
		os.remove(file_upload)
		return('You have not completed Lab 14 please do so to procede with this lab')




def grade_django_lab14(file, lab_number, current_user):

	try:
		lab13 = CourseTopic.objects.get(topic_number = 13)
		check_lab13_status = ''
		check_lab13_status = GradesReport.objects.get(course_topic_id = lab13, user_id = current_user, grade = 'Passed')
	except ObjectDoesNotExist:
		check_lab13_status = ''
	except MultipleObjectsReturned:
		check_lab13_status = 'MultipleObjects'		
	
	file_upload = ''
	xpected_app_name = current_user.username + 'scrumy'
	grade = ''
	mark = 0
	file_name = ''

	if file.name.endswith('.zip'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.zip')
		file_name = file.name.split('-')[1]
	elif file.name.endswith('.gz'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.gz')
		file_name = file.name.split('-')[1]
	else:
		file_name = ''


	if check_lab13_status != '' or check_lab13_status == 'MultipleObjects':
		if xpected_app_name == file_name:
			dp = 0
			try:
				subprocess.call([sys.executable, "-m", "pip", "install", file_upload])
			except Exception as e:
				dp += 1
			finally:
				os.remove(file_upload)
			
			if dp < 1:
				options = webdriver.ChromeOptions()
				options.add_argument("headless")
				driver = webdriver.Chrome(chrome_options = options)
				html = ''
				try:
					driver.get(VERYFD_ADDRESS+xpected_app_name+"/home")
					html = driver.find_element_by_xpath('//td[contains(text(),"louis")]').get_attribute('innerHTML')
				except Exception as e:
					print (e)
				if html != '':
					grade = "Passed"
					mark = 100
					print('Passed')
				else:
					print('Failed')
					grade = 'Failed'
					mark = 0
				save_grade(lab_number, mark, current_user, grade)
				return(grade)
			else:

				return('Something went wrong please try again')
		else:
			os.remove(file_upload)
			return("The name of the file you are submitting should be of the format 'django-your linuxjobber username+scrumy-x.x' where x is an integer value and - is an hyphen")
	else:
		os.remove(file_upload)
		return('You have not completed Lab 13 please do so to procede with this lab')






def grade_django_lab13(file, lab_number, current_user):
	try:
		lab12 = CourseTopic.objects.get(topic_number = 12)
		check_lab12_status = ''
		check_lab12_status = GradesReport.objects.get(course_topic_id = lab12, user_id = current_user, grade = 'Passed')
	except ObjectDoesNotExist:
		check_lab12_status = ''
	except MultipleObjectsReturned:
		check_lab12_status = 'MultipleObjects'		
	
	file_upload = ''
	xpected_app_name = current_user.username + 'scrumy'
	grade = ''
	mark = 0
	file_name = ''

	if file.name.endswith('.zip'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.zip')
		file_name = file.name.split('-')[1]
	elif file.name.endswith('.gz'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.gz')
		file_name = file.name.split('-')[1]
	else:
		file_name = ''


	if check_lab12_status != '' or check_lab12_status == 'MultipleObjects':
		if xpected_app_name == file_name:
			dp = 0
			try:
				subprocess.call([sys.executable, "-m", "pip", "install", file_upload])
			except Exception as e:
				dp += 1
			finally:
				os.remove(file_upload)
			
			if dp < 1:
				options = webdriver.ChromeOptions()
				options.add_argument("headless")
				driver = webdriver.Chrome(chrome_options = options)
				html = 'html'
				try:
					driver.get(VERYFD_ADDRESS+xpected_app_name+"/addgoal")
					driver.get(VERYFD_ADDRESS+xpected_app_name+"/home")
					html = driver.find_element_by_xpath('//body').get_attribute('innerHTML')
				except Exception as e:
					print(e)
				if html.lower().startswith('keep learning django'):
					grade = "Passed"
					mark = 100
					print('Passed')
				else:
					print('Failed')
					grade = 'Failed'
					mark = 0
				save_grade(lab_number, mark, current_user, grade)
				return(grade)
			else:

				return('Something went wrong please try again')
		else:
			os.remove(file_upload)
			return("The name of the file you are submitting should be of the format 'django-your linuxjobber username+scrumy-x.x' where x is an integer value and - is an hyphen")
	else:
		os.remove(file_upload)
		return('You have not completed Lab 12 please do so to procede with this lab')




def grade_django_lab12(file, lab_number, current_user):
	try:
		lab11 = CourseTopic.objects.get(topic_number = 11)
		check_lab11_status = ''
		check_lab11_status = GradesReport.objects.get(course_topic_id = lab11, user_id = current_user, grade = 'Passed')
	except ObjectDoesNotExist:
		check_lab11_status = ''
	except MultipleObjectsReturned:
		check_lab11_status = 'MultipleObjects'
		
	
	file_upload = ''
	xpected_app_name = current_user.username + 'scrumy'
	grade = ''
	mark = 0
	file_name = ''

	if file.name.endswith('.zip'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.zip')
		file_name = file.name.split('-')[1]
	elif file.name.endswith('.gz'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.gz')
		file_name = file.name.split('-')[1]
	else:
		file_name = ''

	if check_lab11_status != '' or check_lab11_status == 'MultipleObjects':
		if xpected_app_name == file_name:
			dp = 0
			try:
				subprocess.call([sys.executable, "-m", "pip", "install", file_upload])
			except Exception as e:
				dp += 1
			finally:
				os.remove(file_upload)
			
			if dp < 1:
				options = webdriver.ChromeOptions()
				options.add_argument("headless")
				driver = webdriver.Chrome(chrome_options = options)
				html = ''
				try:
					driver.get(VERYFD_ADDRESS+xpected_app_name+"/movegoal/1")
					html = driver.find_element_by_xpath('//body').get_attribute('innerHTML')
				except Exception as e:
					print (e)
				if html != '':
					grade = "Passed"
					mark = 100
					print('Passed')
				else:
					print('Failed')
					grade = 'Failed'
					mark = 0
				save_grade(lab_number, mark, current_user, grade)
				return(grade)
			else:

				return('Something went wrong please try again')
		else:
			os.remove(file_upload)
			return("The name of the file you are submitting should be of the format 'django-your linuxjobber username+scrumy-x.x' where x is an integer value and - is an hyphen")
	else:
		os.remove(file_upload)
		return('You have not completed Lab 11 please do so to procede with this lab')

	standard_logger.debug('')



def grade_django_lab11(file, lab_number, current_user):
	try:
		lab10 = CourseTopic.objects.get(topic_number = 10)
		check_lab10_status = ''
		check_lab10_status = GradesReport.objects.filter(course_topic_id = lab10, user_id = current_user, grade = 'Passed').exists()
	except Exception as e:
		error = e
	
	file_upload = ''
	xpected_app_name = current_user.username + 'scrumy'
	grade = ''
	mark = 0
	file_name = ''

	if file.name.endswith('.zip') and file.name.lower().startswith('django-'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.zip')
		file_name = file.name.split('-')[1]
	else:
		file_name = ''


	if check_lab10_status:
		if xpected_app_name == file_name and file.name.endswith('.zip'):
			dp = 0
			try:
				a = subprocess.call(["pip", "install", file_upload])
			except Exception as e:
				dp += 1
			finally:
				os.remove(file_upload)
			
			if a == 0:
				options = selenium.webdriver.ChromeOptions()
				options.add_argument("headless")
				driver = selenium.webdriver.Chrome(chrome_options = options)
				html = ''
				try:
					driver.get(VERYFD_ADDRESS+xpected_app_name)
					html = driver.find_element_by_xpath('//body').get_attribute('innerHTML')
				except Exception as e:
					error = e
				if html != '':
					grade = "Passed"
					mark = 100
				else:
					grade = 'Failed'
					mark = 0
				save_grade(lab_number, mark, current_user, grade)
				return(grade)
			else:

				return('Something went wrong please try again')
		else:
			os.remove(file_upload)
			return("The name of the file you are submitting should be of the format 'django-your linuxjobber username+scrumy-x.x' where x is an integer value and - is an hyphen")
	else:
		os.remove(file_upload)
		return('You have not completed Lab 10 please do so to procede with this lab')






def grade_django_lab10(file, lab_number, current_user):

	try:
		lab9 = CourseTopic.objects.get(topic_number = 9)
		check_lab9_status = ''
		check_lab9_status = GradesReport.objects.filter(course_topic_id = lab9, user_id = current_user, grade = 'Passed').exists()
	except Exception as e:
		print(e)
		return ('Something went wrong')
	
	try:
		lab10 = CourseTopic.objects.get(topic_number = lab_number)
		check_lab10_fail_status = '' 
		check_lab10_pass_status = ''
		check_lab10_fail_status = GradesReport.objects.filter(course_topic_id = lab10, user_id = current_user, grade = 'Failed').exists()
		check_lab10_pass_status = GradesReport.objects.filter(course_topic_id = lab10, user_id = current_user, grade = 'Passed').exists()
	except Exception as e:
		return('Something went wrong')
	
	file_upload = ''
	xpected_app_name = current_user.username + 'scrumy'
	grade = ''
	mark = 0
	file_name = ''

	if file.name.endswith('.zip') and file.name.lower().startswith('django-'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.zip')
		file_name = file.name.split('-')[1]
	else:
		file_name = ''


	if check_lab9_status:
		if check_lab10_pass_status:
			os.remove(file_upload)
			return('You have already done and passed this lab')
		else:
			if check_lab10_fail_status:
				# only installation and selenium operation
				if xpected_app_name == file_name and file.name.endswith('.zip'):
					dp = 0
					try:
						a = subprocess.call(["pip", "install", file_upload])
					except Exception as e:
						dp += 1
					finally:
						os.remove(file_upload)
					if a == 0:
						options = selenium.webdriver.ChromeOptions()
						options.add_argument("headless")
						driver = selenium.webdriver.Chrome(chrome_options = options)
						driver.get(VERYFD_ADDRESS+xpected_app_name)

						html = driver.find_element_by_xpath('//body').get_attribute('innerHTML')
						if html != '':
							grade = "Passed"
							mark = 100
						else:
							grade = 'Failed'
							mark = 0
						save_grade(lab_number, mark, current_user, grade) 
						return(grade)
					else:
						# If this line ever gets to be executed,
						# a line of code that automaticaly restarts the server
						# should be added within this block
						return ('Something went wrong please try again') 
				else:
					os.remove(file_upload)
					return("The name of the file you are submitting should be of the format 'django-your linuxjobber username+scrumy-x.x' where x is an integer value and - is an hyphen")
			else:
				if xpected_app_name == file_name and file.name.endswith('.zip'):
					dp = 0
					try:
						a = subprocess.call(["pip", "install", file_upload])
					except Exception as e:
						dp +=1
					finally:
						os.remove(file_upload)
					
					if a == 0:
						try:
							options = selenium.webdriver.ChromeOptions()
							options.add_argument("headless")
							driver = selenium.webdriver.Chrome(chrome_options = options)
							driver.get(VERYFD_ADDRESS+'admin')
							driver.find_element_by_name('username').send_keys('louis')
							driver.find_element_by_name('password').send_keys('L0u15_linux')
							driver.find_element_by_xpath('//input[@type="submit"]').click()
							driver.get(VERYFD_ADDRESS+'admin/'+xpected_app_name+'/goalstatus/add/')
							driver.find_element_by_name('status_name').send_keys('Weekly Goal')
							driver.find_element_by_name('_save').click()
							driver.get(VERYFD_ADDRESS+'admin/'+xpected_app_name+'/goalstatus/add/')
							driver.find_element_by_name('status_name').send_keys('Daily Goal')
							driver.find_element_by_name('_save').click()
							driver.get(VERYFD_ADDRESS+'admin/'+xpected_app_name+'/goalstatus/add/')
							driver.find_element_by_name('status_name').send_keys('Verify Goal')
							driver.find_element_by_name('_save').click()
							driver.get(VERYFD_ADDRESS+'admin/'+xpected_app_name+'/goalstatus/add/')
							driver.find_element_by_name('status_name').send_keys('Done Goal')
							driver.find_element_by_name('_save').click()

							driver.get(VERYFD_ADDRESS+'admin/'+xpected_app_name+'/scrumygoals/add/')
							driver.find_element_by_name('goal_name').send_keys('Learn Django')
							driver.find_element_by_name('goal_id').send_keys('1')
							driver.find_element_by_name('created_by').send_keys('Louis')
							driver.find_element_by_name('moved_by').send_keys('Louis')
							driver.find_element_by_name('owner').send_keys('Louis')
							driver.find_element_by_xpath(".//*[@id='id_goal_status']/option[text()='GoalStatus object (1)']").click()
							driver.find_element_by_xpath(".//*[@id='id_user']/option[text()='louis']").click()
							driver.find_element_by_name('_save').click()

							driver.get(VERYFD_ADDRESS+'admin/'+xpected_app_name+'/scrumygoals/add/')
							driver.find_element_by_name('goal_name').send_keys('Test Verify Goal')
							driver.find_element_by_name('goal_id').send_keys('163')
							driver.find_element_by_name('created_by').send_keys('Louis')
							driver.find_element_by_name('moved_by').send_keys('Louis')
							driver.find_element_by_name('owner').send_keys('Louis')
							driver.find_element_by_xpath(".//*[@id='id_goal_status']/option[text()='GoalStatus object (3)']").click()
							driver.find_element_by_xpath(".//*[@id='id_user']/option[text()='louis']").click()
							driver.find_element_by_name('_save').click()

							driver.get(VERYFD_ADDRESS+'admin/'+xpected_app_name+'/scrumygoals/add/')
							driver.find_element_by_name('goal_name').send_keys('Test Done Goal')
							driver.find_element_by_name('goal_id').send_keys('164')
							driver.find_element_by_name('created_by').send_keys('Louis')
							driver.find_element_by_name('moved_by').send_keys('Louis')
							driver.find_element_by_name('owner').send_keys('Louis')
							driver.find_element_by_xpath(".//*[@id='id_goal_status']/option[text()='GoalStatus object (4)']").click()
							driver.find_element_by_xpath(".//*[@id='id_user']/option[text()='louis']").click()
							driver.find_element_by_name('_save').click()

							driver.get(VERYFD_ADDRESS+'admin/logout')

							driver.get(VERYFD_ADDRESS+xpected_app_name)

							html = driver.find_element_by_xpath('//body').get_attribute('innerHTML')
							
							if html != '':
								grade = "Passed"
								mark = 100
							else:
								grade = 'Failed'
								mark = 0
							save_grade(lab_number, mark, current_user, grade) 
						except Exception as e:
							# If this block of code ever gets to be executed, the next upgrade of this grader should 
							# implement the functionality that asks the user to repeat the previous and then the grader
							# logs in to the admin interface and deletes the model belonging to that user.
							grade = 'Failed'
							mark = 0
							save_grade(lab_number, mark, current_user, grade)
						return(grade)
					else:
						return('something went wrong please try again')
				else:
					os.remove(file_upload)
					return("The name of the file you are submitting should be of the format 'django-your linuxjobber username+scrumy-x.x' where x is an integer value and - is an hyphen")
	else:
		os.remove(file_upload)
		return('You have not completed Lab 9 please do so to procede with this lab')

		






def grade_django_lab9(file, lab_number, current_user):

	try:
		lab8 = CourseTopic.objects.get(topic_number = 8)
		check_lab8_status = ''
		check_lab8_status = GradesReport.objects.get(course_topic_id = lab8, user_id = current_user, grade = 'Passed')
	except ObjectDoesNotExist:
		check_lab8_status = ''
	except MultipleObjectsReturned:
		check_lab8_status = 'MultipleObjects'


	file_upload = ''
	file_name = ''

	if file.name.endswith('.zip') and file.name.lower().startswith('django-'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.zip')
		file_name = file.name.split('-')[1]
	else:
		file_name = ''

	if check_lab8_status != '' or check_lab8_status == 'MultipleObjects':

		xpected_app_name = current_user.username + 'scrumy'
		grade = ''
		mark = 0
		task_1 = 0
		task_2 = 0
		task_3 = 0
		task_4 = 0
		task_5 = 0

		if xpected_app_name == file_name and file.name.endswith('.zip'):
			dp = 0

			try:
				a = subprocess.call(["pip", "install", file_upload])
			except Exception as e:
				dp += 1 
			finally:
				os.remove(file_upload)
			if a == 0:

				cwd = os.getcwd()
				os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'veryfd'))
				print(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'veryfd'))
				os.system('python3.6 manage.py makemigrations')
				os.system('python3.6 manage.py migrate')
				os.chdir(cwd)

				try:
					options = selenium.webdriver.ChromeOptions()
					options.add_argument("headless")
					driver = selenium.webdriver.Chrome(chrome_options = options)
					driver.get(VERYFD_ADDRESS + "admin")
					driver.find_element_by_name('username').send_keys('louis')
					driver.find_element_by_name('password').send_keys('L0u15_linux')
					driver.find_element_by_xpath('//input[@type="submit"]').click()
					goal_status = driver.find_element_by_partial_link_text('Goal status').get_attribute('innerHTML').rstrip('\n')
					scrumy_goals = driver.find_element_by_partial_link_text('Scrumy goals').get_attribute('innerHTML').rstrip('\n')
					scrumy_history = driver.find_element_by_partial_link_text('Scrumy historys').get_attribute('innerHTML').rstrip('\n')
					if goal_status and scrumy_goals and scrumy_history:
						task_1 += 1
						task_5 += 1
				except Exception as e:
					task_1 = 0

				try:
					driver.find_element_by_partial_link_text('Scrumy goals').click()
					driver.find_element_by_class_name('addlink').click()
					goal_name = driver.find_element_by_name('goal_name').get_attribute('name')
					goal_id = driver.find_element_by_name('goal_id').get_attribute('name')
					created_by = driver.find_element_by_name('created_by').get_attribute('name')
					moved_by = driver.find_element_by_name('moved_by').get_attribute('name')
					owner = driver.find_element_by_name('owner').get_attribute('name')
					goal_status = driver.find_element_by_name('goal_status').get_attribute('name')
					user = driver.find_element_by_name('user').get_attribute('name')

					if goal_name and goal_id and created_by and moved_by and owner and goal_status and user:
						task_2 += 1
						task_3 += 1
						task_4 += 1
				except Exception as e:
					task_2 = 0
					task_3 = 0

				try:
					driver.find_element_by_partial_link_text('Home').click()
					driver.find_element_by_partial_link_text('Scrumy historys').click()
					driver.find_element_by_class_name('addlink').click()

					created_by = driver.find_element_by_name('created_by').get_attribute('name')
					moved_by = driver.find_element_by_name('moved_by').get_attribute('name')
					moved_from = driver.find_element_by_name('moved_from').get_attribute('name')
					moved_to = driver.find_element_by_name('moved_to').get_attribute('name')
					time_0 = driver.find_element_by_name('time_of_action_0').get_attribute('name')
					time_1 = driver.find_element_by_name('time_of_action_1').get_attribute('name')
					goal_name = driver.find_element_by_name('goal').get_attribute('name')

					if created_by and moved_by and moved_from and moved_to and time_0 and time_1 and goal_name:
						task_4 += 1
				except Exception as e:
					task_4 = 0

				x = task_1 + task_2 + task_3 + task_4 + task_5
				if x > 5:
					grade = 'Passed'
					mark = int((task_1 + task_2 + task_3 + task_4 + task_5)/6 * 100)
				else:
					grade = 'Failed'
					mark = int((task_1 + task_2 + task_3 + task_4 + task_5)/6 * 100)

				save_grade(lab_number, mark, current_user, grade)
				return (grade)
			else:
				grade = 'Failed'
				mark = 0
				save_grade(lab_number, mark, current_user, grade)
				return("Something went wrong, you may not have packaged your application correctly")
		else:
			os.remove(file_upload)
			return("The name of the file you are submitting should be of the format 'django-your linuxjobber username+scrumy-x.x' where x is an integer value and - is an hyphen")
	else:
		os.remove(file_upload)
		return('You have not completed lab 8, please do so to procede with this lab')





def grade_django_lab8(file, lab_number, current_user):

	try:
		lab7 = CourseTopic.objects.get(topic_number = 7)
		check_lab7_status = ''
		check_lab7_status = GradesReport.objects.get(course_topic_id = lab7, user_id = current_user, grade = 'Passed')
	except ObjectDoesNotExist:
		check_lab7_status = ''
	except MultipleObjectsReturned:
		check_lab7_status = 'MultipleObjects'

	file_upload = ''

	xpected_app_name = current_user.username + 'scrumy'
	grade = ''
	mark = 0
	file_name = ''

	if file.name.endswith('.zip') and file.name.lower().startswith('django-'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.zip')
		file_name = file.name.split('-')[1]
	else:
		file_name = ''

	if check_lab7_status != '' or check_lab7_status == 'MultipleObjects':
		if xpected_app_name == file_name and file.name.endswith('.zip'):
			try:
				a = subprocess.call(["pip", "install", file_upload])
				if a == 0:

					options = selenium.webdriver.ChromeOptions()
					options.add_argument("headless")
					driver = selenium.webdriver.Chrome(chrome_options = options)

					driver.get(VERYFD_ADDRESS+xpected_app_name)

					html = driver.find_element_by_xpath('//body').get_attribute('innerHTML')
				
					if html.rstrip('\n').lower() == 'hello world':
						grade = "Passed"
						mark = 100
					else:
						grade = 'Failed'
						mark = 0
					save_grade(lab_number, mark, current_user, grade)
					return(grade)
				else:
					mark = 0
					grade = 'Failed'
					save_grade(lab_number, mark, current_user, grade)
					return(grade)
			except Exception as e:
				grade = 'Failed'
				mark = 0
				save_grade(lab_number, mark, current_user, grade)
			finally:
				os.remove(file_upload)
		else:
			os.remove(file_upload)
			return("The name of the file you are submitting should be of the format 'django-your linuxjobber username+scrumy-x.x' where x is an integer value and - is an hyphen")
	else:
		os.remove(file_upload)
		return('You have not completed lab 7, please do so to procede with this lab')




def grade_django_lab7(file, lab_number, current_user):
	file_upload = ''
	file_name = ''
	xpected_app_name = current_user.username + 'scrumy'
	grade = ''
	mark = 0
	my_list = ''

	if file.name.endswith('.zip') and file.name.lower().startswith('django-'):
		file_upload = os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.zip')
		file_name = file.name.split('-')[1]
	else:
		file_name = ''

	if xpected_app_name == file_name and file.name.endswith('.zip'):
		dy = 0
		try:
			a = subprocess.call(["pip", "install", file_upload])
		except Exception as e:
			pass
		finally:
			os.remove(file_upload)

		if a == 0:
			grade = 'Passed'
			mark = 100 - dear
			save_grade(lab_number, mark, current_user, grade)
			with open(os.path.join(VERYFD_PROJECT_DIR , 'settings.py'), 'r') as settings_file:
				for eachline in settings_file:
					if eachline.rstrip('\n') == "    "+"'"+xpected_app_name+"'"+",":
						my_list = eachline
			if my_list == '':
				replace(os.path.join(VERYFD_PROJECT_DIR, 'settings.py'), 'INSTALLED_APPS = [', "INSTALLED_APPS = [\n    '"+xpected_app_name+"',")
				replace(os.path.join(VERYFD_PROJECT_DIR, 'urls.py'), 'urlpatterns = [', "urlpatterns = [\n    path('"+ xpected_app_name +"/', include('"+ xpected_app_name +".urls')),")
			return (grade)
		else:
			grade = 'Failed'
			save_grade(lab_number, mark, current_user, grade)
			return(grade)
	else:
		os.remove(file_upload)
		return ("The name of the file you are submitting should be of the format 'django-your linuxjobber username+scrumy-x.x' where x is an integer value and - is an hyphen")
	standard_logger.error("na wa")






def grade_django_lab6(file, lab_number, current_user):

	match_count = 0
	grade = ''
	mark = 0

	if file.name.endswith('.sql'):
		try:
			with open(os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.sql'), 'r') as sql_database:
				for each_line in sql_database:
					if each_line.rstrip('\n') == "INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES":
						match_count += 1

			mark = int(100 * match_count/1)
			if mark > 69:
				grade = "Passed"
			else:
				grade = "Failed"
		except Exception as e:
			print(e)
			grade = 'Failed'
		finally:
			os.remove(os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.sql'))
	else:
		grade = 'Failed'
		os.remove(os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.sql'))
	save_grade(lab_number, mark, current_user, grade)
	return (grade)



def grade_django_lab5(file, lab_number, current_user):
	match_count = 0
	grade = ''
	mark = 0

	if file.name.endswith('.sql'):
		try:
			with open(os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.sql'), 'r') as sql_database:
				for each_line in sql_database:
					if each_line.rstrip('\n') == "CREATE TABLE IF NOT EXISTS `django_migrations` (" or each_line.rstrip('\n') == "CREATE TABLE `django_migrations` (" or each_line.rstrip('\n') == "CREATE TABLE IF NOT EXISTS `django_admin_log` (" or each_line.rstrip('\n') == "CREATE TABLE `django_admin_log` (" or each_line.rstrip('\n') == "CREATE TABLE IF NOT EXISTS `django_session` (" or each_line.rstrip('\n') == "CREATE TABLE `django_session` (":
						match_count += 1
			
			mark = int(100 * match_count/3)
			if mark > 69:
				grade = "Passed"
			else:
				grade = "Failed"
		except Exception as e:
			print(e)
			grade = 'Failed'
		finally:
			os.remove(os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.sql'))
	else:
		grade = "Failed"
		os.remove(os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.sql'))
	save_grade(lab_number, mark, current_user, grade)
	return (grade)




def grade_django_lab4(file, lab_number, current_user):

	count = 0
	grade = ''
	mark = 0

	if file.name.startswith('settings'):
		try:
			with open(os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.py'), 'r') as settings_file:
				for eachline in settings_file:
					if eachline.rstrip('\n') == "        'ENGINE': 'django.db.backends.sqlite3'," or eachline.rstrip('\n') == "        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),":
						count += 1

			if count > 1:
				grade = 'Passed'
				mark = 100
			else:
				grade = 'Failed'
				mark = 0
		except Exception as e:
			print (e)
			grade = 'Failed'
		finally:
			os.remove(os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.py'))
	else:
		grade = 'Failed'
		os.remove(os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.py'))	
	save_grade(lab_number, mark, current_user, grade)
	return (grade)




def grade_django_lab3(file, lab_number, current_user):
	surname = current_user.username
	zfile = ''
	zfile_name = file.name
	exfile_name = zfile_name.rstrip('.zip')
	task_1= 0
	task_3 = 0
	task_4 = 0
	task_5 = 0
	task_6 = 0
	grade = ''
	mark = 0

	os.remove(os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.zip'))

	if zfile_name.endswith('.zip') and zfile_name.startswith('myscrumy'):	
		try:
			zfile = zipfile.ZipFile(file)
		except zipfile.BadZipfile as ex:
			print("%s no a zip file" % file)
		'''finally:
			os.remove(os.path.join(PROJECT_MEDIA_DIR, current_user.username + '_' + str(lab_number) + '.zip'))'''

		ret = zfile.testzip()
	
		if ret is not None:
			grade = 'Failed'
			print("%s is a bad zip file, error: %s" % file, ret)
		else:
			lab_docs = zfile.extractall(MEDIA_DIR)

			for root, dirs, files in os.walk(MEDIA_DIR):
				for dirnames in dirs:
					if dirnames == 'myscrumy':
						task_1 += 1
				for dirnames in dirs:
					if dirnames == surname + 'scrumy':
						task_3 += 1
				for file in files:
					if file.endswith('dmin.py') or file.endswith('odels.py') or file.endswith('iews.py') or file.endswith('ests.py') or file.endswith('pps.py'):
						task_3 += 1
				for file in files:
					if file.endswith('rls.py'):
						task_4 += 1

			with open(os.path.join(MEDIA_DIR, 'myscrumy/' + surname +'scrumy/urls.py'), 'r') as project_url:
				for eachline in project_url:
					if eachline.rstrip('\n') == "    path('"+surname+"scrumy/', include("+'"'+surname+'scrumy.urls")),' or eachline.rstrip('\n') == "    path('"+surname+"scrumy/', include('"+surname+"scrumy.urls'))," or eachline.rstrip('\n') == '    path("'+surname+'scrumy/", include('+"'"+surname+"scrumy.urls'))," or eachline.rstrip('\n') == '    path("'+surname+'scrumy/", include("'+surname+'scrumy.urls")),':
						task_5 += 1

			with open(os.path.join(MEDIA_DIR, 'myscrumy/'+surname+'scrumy/urls.py'), 'r') as app_url:
				for eachline in app_url:
					if eachline.rstrip('\n') == "    path('', views.index)," or eachline.rstrip('\n') == '    path("", views.index),':
						task_6 += 1
			shutil.rmtree(MEDIA_DIR+'/myscrumy')

			mark = int(100* (task_1 + task_3 + task_4 + task_5 + task_6)/12)

			if mark < 70:
				grade = "Failed"
			else:
				grade = "Passed"
	else:
		grade = 'Failed'
	save_grade(lab_number, mark, current_user, grade)
	return (grade)






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





def grade_django_lab(file, lab_number, current_user):

	if lab_number == 3:
		grade = grade_django_lab3(file, lab_number, current_user)
		return (grade)
	elif lab_number == 4:
		grade = grade_django_lab4(file, lab_number, current_user)
		return (grade)
	elif lab_number == 5:
		grade = grade_django_lab5(file, lab_number, current_user)
		return (grade)
	elif lab_number == 6:
		grade = grade_django_lab6(file, lab_number, current_user)
		return (grade)
	elif lab_number == 7:
		grade = grade_django_lab7(file, lab_number, current_user)
		return (grade)
	elif lab_number == 8:
		grade = grade_django_lab8(file, lab_number, current_user)
		return (grade)
	elif lab_number == 9:
		grade = grade_django_lab9(file, lab_number, current_user)
		return (grade)
	elif lab_number == 10:
		grade = grade_django_lab10(file, lab_number, current_user)
		return (grade)
	elif lab_number == 11:
		grade = grade_django_lab11(file, lab_number, current_user)
		return (grade)
	elif lab_number == 12:
		grade = grade_django_lab12(file, lab_number, current_user)
		return (grade)
	elif lab_number == 13:
		grade = grade_django_lab13(file, lab_number, current_user)
		return (grade)
	elif lab_number == 14:
		grade = grade_django_lab14(file, lab_number, current_user)
		return (grade)
	elif lab_number == 15:
		grade = grade_django_lab15(file, lab_number, current_user)
		return (grade)
	elif lab_number == 16:
		grade = grade_django_lab16(file, lab_number, current_user)
		return (grade)
	elif lab_number == 17:
		grade = grade_django_lab17(file, lab_number, current_user)
		return (grade)
	elif lab_number == 18:
		grade = grade_django_lab18(file, lab_number, current_user)
		return (grade)
	elif lab_number == 19:
		grade = grade_django_lab19(file, lab_number, current_user)
		return (grade)
	elif lab_number == 20:
		grade = grade_django_lab20(file, lab_number, current_user)
		return (grade)
	elif lab_number == 21:
		grade = grade_django_lab21(file, lab_number, current_user)
		return (grade)
	else:
		return ('Invalid request')
