from django.forms import ModelForm

from hackathon.models import Person, Project

class ProjectForm(ModelForm):
	class Meta:
		model = Project
		exclude = ('slug',)

class PersonForm(ModelForm):
	class Meta:
		model = Person
		exclude = ('slug',)