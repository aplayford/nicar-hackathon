from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import copy

from hackathon.models import Person, Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('slug',)

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
        print("save save save start.")
        if user is not None:
            pass_args = uncommit_copy(kwargs)

            me = super(PersonForm, self).save(*args, **pass_args)
            me.user = user

            if kwargs.get('commit', True):
                me.save()
            return me
        else:
            print("do save mr. save sir.")
            return super(PersonForm, self).save(*args, **kwargs)

    class Meta:
        model = Person
        fields = ('name', 'bio', 'skills_summary', 'website', 'roles_willing', 'user')
        widgets = {
            'roles_willing': forms.CheckboxSelectMultiple(),
            'user': forms.HiddenInput(),
        }

def uncommit_copy(kwargs):
    args = copy.deepcopy(kwargs)
    args["commit"] = False
    return args