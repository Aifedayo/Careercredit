from django import forms

from .models import *

class WeForm(forms.Form):
	types = forms.ModelChoiceField(queryset=wetype.objects.all(), empty_label="Select",widget = forms.Select(attrs = {'class':'form-control isaput'}) )
	date = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker form-control isaput','placeholder': 'Your graduation date'}))

class JobApplicationForm(forms.ModelForm):
	fullname = forms.CharField(label='First Name', widget = forms.TextInput(attrs = {'placeholder': 'Your full name', 'id' :'JobFname', 'class':'form-control jobfinput'}) )
	email = forms.CharField(label='Email', widget = forms.TextInput(attrs = {'placeholder': 'Your email address', 'id' :'JobFname', 'class':'form-control jobfinput'}) )
	phone = forms.CharField(label='Phone', widget = forms.TextInput(attrs = {'placeholder': 'Your phone number', 'id' :'JobFname', 'class':'form-control jobfinput'}) )
	cv_link = forms.CharField(label='Phone',required = False, widget = forms.TextInput(attrs = {'placeholder': 'Link to CV or LinkedIn', 'id' :'cv_link', 'class':'form-control jobfinput', }) )
	resume = forms.FileField(label='cv',required = False, widget = forms.FileInput(attrs = {'id':'file-upload','accept':".pdf,.doc,.docx"}))

	class Meta:
		model = Job
		fields = ['resume','email','fullname','cv_link','phone']

class PartimeApplicationForm(forms.ModelForm):

	High = [
    	(1,'Yes'),
    	(0,'No'),
    ]

	fullname = forms.CharField(label='First Name', widget = forms.TextInput(attrs = {'placeholder': 'Your full name', 'id' :'JobFname', 'class':'form-control jobfinput'}) )
	email = forms.EmailField(label='Email', widget = forms.TextInput(attrs = {'placeholder': 'Your email address', 'id' :'JobFname', 'class':'form-control jobfinput'}) )
	phone = forms.CharField(label='Phone', widget = forms.TextInput(attrs = {'placeholder': 'Your phone number', 'id' :'JobFname', 'class':'form-control jobfinput'}) )
	position = forms.ModelChoiceField(queryset=PartTimePostion.objects.all(), empty_label="Select",widget = forms.Select(attrs = {'placeholder': 'Position', 'id' :'JobFname', 'class':'form-control jobfinput jobselect'}) )
	cv_link = forms.CharField(label='Phone',required = False, widget = forms.TextInput(attrs = {'placeholder': 'Link to CV or LinkedIn', 'id' :'cv_link', 'class':'form-control jobfinput', }) )
	cv = forms.FileField(label='cv',required = False, widget = forms.FileInput(attrs = {'id':'file-upload','accept':".pdf,.doc,.docx"}))
	high_salary = forms.ChoiceField(choices=High,widget = forms.RadioSelect(attrs = {'class':'jobcheckbox'}))

	class Meta:
		model = PartTimeJob
		exclude = ['application_date']



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
	resume = forms.FileField(required = True, widget = forms.FileInput(attrs = {'accept':".pdf,.doc,.docx"}))

	class Meta:
		model = Internship
		fields = '__all__'
		exclude = ('date',)

class ResumeForm(forms.ModelForm):
	class Meta:
		model = Resume
		fields = ['resume',]


	

class ContactUsForm(forms.ModelForm):
	
	class Meta:
		model = ContactMessages
		fields = ['full_name','email','phone_no','message_subject','message',]
		


class AWSCredUpload(forms.ModelForm):
	document = forms.FileField(label='', widget = forms.FileInput(attrs = {'placeholder': 'Aws credentials', 'id' :'upload-file', 'accept':".csv"}) )
	class Meta:
		model = Document
		fields = ['document',]

class UnsubscribeForm(forms.ModelForm):
		email = forms.CharField(label='Email Address', max_length=50)
		class Meta:
			model = Unsubscriber
			fields = ['email']


class CareerSwitchApplicationForm(forms.ModelForm):
	fullname = forms.CharField(label='First Name', widget = forms.TextInput(attrs = {'placeholder': 'Your full name', 'id' :'JobFname', 'class':'form-control jobfinput'}) )
	email = forms.CharField(label='Email', widget = forms.TextInput(attrs = {'placeholder': 'Your email address', 'id' :'JobFname', 'class':'form-control jobfinput'}) )
	new_career = forms.ModelChoiceField(queryset=FullTimePostion.objects.all(), empty_label="Select",widget = forms.Select(attrs = { 'class':'form-control jobfinput'}) )
	old_career = forms.CharField(label='Old Career', widget = forms.TextInput(attrs = {'placeholder': 'Old Career', 'class':'form-control jobfinput'}) )
	phone = forms.CharField(label='Phone', widget = forms.TextInput(attrs = {'placeholder': 'Your phone number', 'id' :'JobFname', 'class':'form-control jobfinput'}) )
	cv_link = forms.CharField(label='cv link',required = False, widget = forms.TextInput(attrs = {'placeholder': 'Link to CV or LinkedIn', 'id' :'cv_link', 'class':'form-control jobfinput', }) )
	resume = forms.FileField(label='cv',required = False, widget = forms.FileInput(attrs = {'id':'file-upload','accept':".pdf,.doc,.docx"}))

	class Meta:
		model = CareerSwitchApplication
		exclude = ['application_date']
