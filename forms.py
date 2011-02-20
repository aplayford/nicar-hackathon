from django import forms

from hackathon.models import Person, Project

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		exclude = ('slug',)
		widgets = {
			'characteristics': forms.CheckboxSelectMultiple()
		}

class PersonForm(forms.ModelForm):
	password = forms.CharField(max_length=50)

	def save(*args, **kwargs):
		m = super(PersonForm, *args, **kwargs)


	class Meta:
		model = Person
		exclude = ('slug', 'user',)
		fields = ('email', 'password', 'name', 'bio', 'skills_summary', 'website', 'roles_willing')
		widgets = {
			'roles_willing': forms.CheckboxSelectMultiple(),
			'password': forms.PasswordInput()
		}