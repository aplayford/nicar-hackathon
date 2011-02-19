from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from hackathon.models import Project, Person

def index(request):
    varsContext = {}

    varsContext["projects"] = Project.objects.all()
    varsContext["people"] = Person.objects.all()

    return render_to_response("hackathon/index.html", varsContext, context_instance=RequestContext(request))

def login(request):
    varsContext = {}
    return render_to_response("hackathon/login.html", varsContext, context_instance=RequestContext(request))

def person(request, slugPerson):
    varsContext = {}

    varsContext["me"] = get_object_or_404(Person, slug=slugPerson)
    
    return render_to_response("hackathon/person.html", varsContext, context_instance=RequestContext(request))

def project(request, slugProject):
    varsContext = {}

    varsContext["me"] = get_object_or_404(Project, slug=slugProject)

    return render_to_response("hackathon/project.html", varsContext, context_instance=RequestContext(request))

def project_sign_up(request):
    varsContext = {}
    return render_to_response("hackathon/project_sign_up.html", varsContext, context_instance=RequestContext(request))

def signup(request):
    varsContext = {}
    return render_to_response("hackathon/signup.html", varsContext, context_instance=RequestContext(request))