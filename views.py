from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.forms.models import inlineformset_factory

from hackathon.models import Person, Project, ProjectNeed, ProjectStaff
from hackathon.forms import ProjectForm, PersonForm

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

def person(request, slugPerson):
    varsContext = {}
    varsContext.update(check_login(request))

    varsContext["me"] = get_object_or_404(Person, slug=slugPerson)
    
    return render_to_response("hackathon/person.html", varsContext, context_instance=RequestContext(request))

def project(request, slugProject):
    varsContext = {}
    varsContext.update(check_login(request))

    varsContext["me"] = get_object_or_404(Project, slug=slugProject)

    return render_to_response("hackathon/project.html", varsContext, context_instance=RequestContext(request))

def project_sign_up(request):
    varsContext = {}
    varsContext.update(check_login(request))

    return render_to_response("hackathon/project_sign_up.html", varsContext, context_instance=RequestContext(request))

def signup(request):
    varsContext = {}
    varsContext.update(check_login(request))

    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = PersonForm()
    
    varsContext['form'] = form

    return render_to_response("hackathon/signup.html", varsContext,
                                    context_instance=RequestContext(request))

def project_submit(request):
    StaffFormset = inlineformset_factory(Project, ProjectStaff)
    NeedsFormset = inlineformset_factory(Project, ProjectNeed)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        project_staff = StaffFormset(request.POST, prefix="staff")
        project_needs = NeedsFormset(request.POST, prefix="needs")
        if form.is_valid() and project_staff.is_valid() and project_needs.is_valid():
            project_staff.save()
            project_needs.save()
            form.save()
    else:
        form = ProjectForm()
        project_staff = StaffFormset(prefix="staff")
        project_needs = NeedsFormset(prefix="needs")
    
    varsContext = {
        "form": form,
        "project_needs": project_needs,
        "project_staff": project_staff
    }

    return render_to_response("hackathon/project_submit.html", varsContext,
                                context_instance=RequestContext(request))