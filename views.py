from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login

from hackathon.models import Person, Project, ProjectNeed, ProjectStaff
from hackathon.forms import ProjectForm, PersonForm, UserForm

def check_login(req):
    if req.user.is_authenticated():
        try:
            profile = req.user.get_profile()
        except Person.DoesNotExist:
            profile = req.user
        return {
            'logged_in': True,
            'user': profile
        }
    else:
        return { 'logged_in': False }

def index(request):
    varsContext = {}
    varsContext.update(check_login(request))

    varsContext["projects"] = Project.objects.all()
    varsContext["people"] = Person.objects.all()

    return render_to_response("hackathon/index.html", varsContext, context_instance=RequestContext(request))

def person(request, slugPerson, id, edit=False):
    varsContext = {}
    varsContext.update(check_login(request))

    me = varsContext["me"] = get_object_or_404(Person, id=id)
    if varsContext["me"].slug != slugPerson:
        return HttpResponseRedirect(varsContext["me"].get_absolute_url())

    if varsContext['logged_in']:
        can_edit = varsContext["can_edit"] = (me == varsContext['user'])
    else:
        can_edit = False

    if edit:
        if varsContext["logged_in"] == False:
            return HttpResponseRedirect("%s?next=%s" % (reverse('login'), reverse('edit-person', kwargs={'slugPerson': me.slug, 'id': me.id})))
        elif not can_edit:
            return HttpResponseRedirect(me.get_absolute_url())
        else:
            return signup(request, edit_instance=me)

    return render_to_response("hackathon/person.html", varsContext, context_instance=RequestContext(request))

def project(request, slugProject, id, edit=False):
    varsContext = {}
    varsContext.update(check_login(request))

    me = varsContext["me"] = get_object_or_404(Project, id=id)
    if varsContext["me"].slug != slugProject:
        return HttpResponseRedirect(varsContext["me"].get_absolute_url())
    
    owner = me.leader()
    if varsContext['logged_in'] and owner is not None:
        can_edit = varsContext["can_edit"] = (owner.person == varsContext['user'])
    else:
        can_edit = False

    if edit:
        if varsContext["logged_in"] == False:
            return HttpResponseRedirect("%s?next=%s" % (reverse('login'), reverse('edit-project', kwargs={'slugProject': me.slug, 'id': me.id})))
        elif not can_edit:
            return HttpResponseRedirect(me.get_absolute_url())
        else:
            return submit_project(request, edit_instance=varsContext["me"])

    return render_to_response("hackathon/project.html", varsContext, context_instance=RequestContext(request))

def signup(request, edit_instance=None):
    varsContext = {}
    varsContext.update(check_login(request))

    if edit_instance:
        view_url = "edit-person"
        view_args, view_kwargs = ([], {'slugPerson': edit_instance.slug, 'id': edit_instance.id})
    else:
        view_url = "signup"
        view_args, view_kwargs = ([], {})

    if 'next' in request.GET and request.GET['next']:
        varsContext['next'] = request.GET['next']
        varsContext['target'] = "%s?next=%s" % (reverse(view_url, args=view_args, kwargs=view_kwargs), varsContext['next'])
    else:
        varsContext['next'] = None
        varsContext['target'] = reverse(view_url, args=view_args, kwargs=view_kwargs)

    if request.method == 'POST':
        if edit_instance is None:
            form1 = UserForm(request.POST)
            form2 = PersonForm(request.POST)
        else:
            form1 = None
            form2 = PersonForm(request.POST, instance=edit_instance)
        
        if (form1 is None or form1.is_valid()) and form2.is_valid():
            if edit_instance is None:
                usr = form1.save()
                usr = authenticate(username=usr.username, password=form1.cleaned_data['password1'])
                login(request, usr)
            else:
                usr = None
            profile = form2.save(usr)
            
            if varsContext['next'] is None:
                varsContext['next'] = profile.get_absolute_url()
            return HttpResponseRedirect(varsContext['next'])
    else:
        if edit_instance is None:
            form1 = UserForm()
            form2 = PersonForm()
        else:
            form1 = None
            form2 = PersonForm(instance=edit_instance)
    
    varsContext['form1'] = form1
    varsContext['form2'] = form2

    return render_to_response("hackathon/signup.html", varsContext,
                                    context_instance=RequestContext(request))

def submit_project(request, edit_instance=None):
    varsContext = {}
    varsContext.update(check_login(request))

    if edit_instance:
        view_url = "edit-project"
        view_args, view_kwargs = ([], {'slugProject': edit_instance.slug, 'id': edit_instance.id})
    else:
        view_url = "submit-project"
        view_args, view_kwargs = ([], {})

    if not varsContext['logged_in']:
        return HttpResponseRedirect("%s?next=%s" % (reverse('signup'), reverse('submit-project')))
    
    if 'next' in request.GET and request.GET['next']:
        varsContext['next'] = request.GET['next']
        varsContext['target'] = "%s?next=%s" % (reverse(view_url, kwargs=view_kwargs), varsContext['next'])
    else:
        if edit_instance:
            varsContext['next'] = edit_instance.get_absolute_url()
        else:
            varsContext['next'] = None
        varsContext['target'] = reverse(view_url, kwargs=view_kwargs)
    
    StaffFormset = inlineformset_factory(Project, ProjectStaff)
    NeedsFormset = inlineformset_factory(Project, ProjectNeed)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            proj = form.save()
            
            project_staff = StaffFormset(request.POST, prefix="staff", instance=proj)
            project_needs = NeedsFormset(request.POST, prefix="needs", instance=proj)
            if project_staff.is_valid() and project_needs.is_valid():
                project_staff.save()
                project_needs.save()

                if varsContext['next'] is None:
                    varsContext['next'] = proj.get_absolute_url()
                return HttpResponseRedirect(varsContext['next'])
        else:
            project_staff = StaffFormset(request.POST, prefix="staff")
            project_needs = NeedsFormset(request.POST, prefix="needs")
    else:
        if edit_instance is None:
            form = ProjectForm()
            project_staff = StaffFormset(prefix="staff")
            project_needs = NeedsFormset(prefix="needs")
        else:
            form = ProjectForm(instance=edit_instance)
            project_staff = StaffFormset(prefix="staff", instance=edit_instance)
            project_needs = NeedsFormset(prefix="needs", instance=edit_instance)

    
    varsContext.update({
        "form": form,
        "project_needs": project_needs,
        "project_staff": project_staff
    })

    return render_to_response("hackathon/project_submit.html", varsContext,
                                context_instance=RequestContext(request))

#def submit_project_success(request):
#    return render_to_response("hackathon/project_submit_success.html", varsContext,
#                                context_instance=RequestContext(request))

#def signup_success(request):
#    return render_to_response("hackathon/signup-success.html", varsContext,
#                                    context_instance=RequestContext(request))
