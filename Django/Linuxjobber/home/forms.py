from django import forms
from . import models
from .models import Document, Internship, Resume


class JobApplicationForm(forms.ModelForm):
	firstname = forms.CharField(label='First Name', widget = forms.TextInput(attrs = {'placeholder': 'First name', 'id' :'JobFname', 'class':'form-control inputarea'}) )
	lastname = forms.CharField(label='Last Name', widget = forms.TextInput(attrs = {'placeholder': 'Last name', 'id' :'JobFname', 'class':'form-control inputarea'}) )
	email = forms.CharField(label='Email', widget = forms.TextInput(attrs = {'placeholder': 'Email', 'id' :'JobFname', 'class':'form-control inputarea'}) )
	phone = forms.CharField(label='Phone', widget = forms.TextInput(attrs = {'placeholder': 'Phone', 'id' :'JobFname', 'class':'form-control inputarea'}) )

	class Meta:
		model = models.Job
		fields = '__all__'



class JobPlacementForm(forms.Form):
	education = forms.CharField(max_length = 70)
	career =  forms.CharField(max_length = 100)
	experience = forms.IntegerField()
	is_certified = forms.CharField(max_length = 50)
	training = forms.CharField(max_length = 50)
	can_relocate = forms.CharField(max_length = 50)
	awareness1 = forms.CharField(max_length= 200)

class InternshipForm(forms.ModelForm):
	firstname = forms.CharField(label='First Name', widget = forms.TextInput(attrs = {'placeholder': 'First name', 'id' :'JobFname', 'class':'form-control'}) )
	lastname = forms.CharField(label='Last Name', widget = forms.TextInput(attrs = {'placeholder': 'Last name', 'id' :'JobFname', 'class':'form-control'}) )
	email = forms.CharField(label='Email', widget = forms.TextInput(attrs = {'placeholder': 'Email', 'id' :'JobFname', 'class':'form-control'}) )
	phone = forms.CharField(label='Phone Number', widget = forms.TextInput(attrs = {'placeholder': 'Phone', 'id' :'JobFname', 'class':'form-control'}) )
	Address = forms.CharField(label='Address', widget = forms.TextInput(attrs = {'placeholder': 'Address', 'id' :'JobFname', 'class':'form-control'}) )
	college = forms.CharField(label='college', widget = forms.TextInput(attrs = {'placeholder': 'college/university', 'id' :'JobFname', 'class':'form-control'}) )
	country = forms.CharField(label='country', widget = forms.TextInput(attrs = {'placeholder': 'Country/State', 'id' :'JobFname', 'class':'form-control'}) )
	experience = forms.CharField(label='experience', widget = forms.TextInput(attrs = {'placeholder': 'Experience', 'id' :'JobFname', 'class':'form-control'}) )
	course = forms.CharField(label='course', widget = forms.TextInput(attrs = {'placeholder': 'Course of study/Deparment ', 'id' :'JobFname', 'class':'form-control'}) )
	resume = forms.FileField(label='', widget = '')
	
	class Meta:
		model = Internship
		fields = '__all__'

class ResumeForm(forms.ModelForm):
	class Meta:
		model = Resume
		fields = ['resume',]


	

class ContactUsForm(forms.ModelForm):
	
	class Meta:
		model = models.ContactMessages
		fields = ['full_name','email','phone_no','message_subject','message',]
		


class AWSCredUpload(forms.ModelForm):
	document = forms.FileField(label='', widget = forms.FileInput(attrs = {'placeholder': 'Aws credentials', 'id' :'upload-file'}) )
	class Meta:
		model = Document
		fields = ['document',]