from django.shortcuts import render_to_response
from django.template import RequestContext

from hackathon.models import Project, Person

def index(request):
    varsContext = {}

    varsContext["projects"] = Project.objects.all()
    varsContext["people"] = Person.objects.all()

    return render_to_response("hackathon/index.html", varsContext, context_instance=RequestContext(request))

def login(request):
    varsContext = {}
    return render(request, "hackathon/login.html", varsContext, context_instance=RequestContext(request))

def person(request, slugPerson):
    varsContext = {}

    varsContext["me"] = Person.objects.get(slug=slugPerson)
    
    return render(request, "hackathon/person.html", varsContext, context_instance=RequestContext(request))

def project(request, slugProject):
    varsContext = {}

    varsContext["me"] = Project.objects.get(slug=slugProject)

    return render(request, "hackathon/project.html", varsContext, context_instance=RequestContext(request))

def project_sign_up(request):
    varsContext = {}
    return render(request, "hackathon/project_sign_up.html", varsContext, context_instance=RequestContext(request))

def signup(request):
    varsContext = {}
    return render(request, "hackathon/signup.html", varsContext, context_instance=RequestContext(request))