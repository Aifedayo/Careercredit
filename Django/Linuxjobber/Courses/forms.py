from django import forms
from Courses.models import Document
from django.forms.widgets import HiddenInput
from django.contrib.auth.models import User

class DocumentGradingForm(forms.ModelForm):
	
	class Meta:
		model = Document
		fields = ['document',]


class MachineGradingForm(forms.Form):
	machine = forms.CharField(label='Instance IP',max_length=150)
	user_id = forms.IntegerField(widget=HiddenInput)

class GradeReportsReceivers(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email',]
