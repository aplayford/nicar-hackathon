from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import copy

from hackathon.models import Person, Project

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		exclude = ('slug',)
		widgets = {
			'characteristics': forms.CheckboxSelectMultiple()
		}

class UserForm(UserCreationForm):
	email = forms.EmailField(label="E-mail", max_length=75, required=True)

	def save(self, *args, **kwargs):
		pass_args = uncommit_copy(kwargs)

		me = super(UserForm, self).save(*args, **pass_args)
		me.email = self.cleaned_data['email']
		print(self.cleaned_data['email'])

		if kwargs.get('commit', True):
			me.save()
		return me

class PersonForm(forms.ModelForm):
	def save(self, user, *args, **kwargs):
		pass_args = uncommit_copy(kwargs)

		me = super(PersonForm, self).save(*args, **pass_args)
		me.user = user

		if kwargs.get('commit', True):
			me.save()
		return me

	class Meta:
		model = Person
		fields = ('name', 'bio', 'skills_summary', 'website', 'roles_willing')
		widgets = {
			'roles_willing': forms.CheckboxSelectMultiple()
		}

def uncommit_copy(kwargs):
	args = copy.deepcopy(kwargs)
	args["commit"] = False
	return args