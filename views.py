from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from hackathon.models import Project, Person

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

    return render_to_response("hackathon/signup.html", varsContext, context_instance=RequestContext(request))