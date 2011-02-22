from django.conf.urls.defaults import *

urlpatterns = patterns('hackathon.views',
    url(r'^$', 'index', name="index"),
    url(r'^person/(?P<id>[\d]+)/(?P<slugPerson>[\w-]+)/$', 'person', name="person"),
    url(r'^person/(?P<id>[\d]+)/(?P<slugPerson>[\w-]+)/edit/$',
                        'person', {'edit': True}, name="edit-person"),
    
    url(r'^project/(?P<id>[\d]+)/(?P<slugProject>[\w-]+)/$', 'project', name="project"),
    url(r'^project/(?P<id>[\d]+)/(?P<slugProject>[\w-]+)/edit/$',
    	'project', {'edit': True}, name="edit-project"),
    url(r'^project/(?P<id>[\d]+)/(?P<slugProject>[\w-]+)/volunteer/$',
        'project_volunteer', {'go': False}, name="project-volunteer"),
    url(r'^project/(?P<id>[\d]+)/(?P<slugProject>[\w-]+)/volunteer/go/$',
        'project_volunteer', {'go': True}, name="project-volunteer-success"),

    url(r'^join_request/(?P<id>[\d]+)/$', 'project_request', name="project-request"),
    url(r'^join_request/(?P<id>[\d]+)/(?P<ans>[\w-]+)/$', 'project_request',
                        name="project-request-respond"),
    url(r'^join_request/(?P<id>[\d]+)/(?P<ans>[\w-]+)/go/$', 'project_request',
                        {'go': True}, name="project-request-respond-go"),
    
    url(r'^submit_project/$', 'submit_project', name="submit-project"),

    url(r'^signup/$', 'signup', name="signup"),
) + patterns('',
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'hackathon/login.html'}, name="login"),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name="logout"),
)