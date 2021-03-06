from django.conf.urls.defaults import *

urlpatterns = patterns('hackathon.views',
    url(r'^$', 'index', name="index"),
    url(r'^person/(?P<id>[\d]+)/(?P<slugPerson>[\w-]+)/$', 'person', name="person"),
    url(r'^person/(?P<id>[\d]+)/(?P<slugPerson>[\w-]+)/edit/$',
        'person', {'edit': True}, name="edit-person"),
    
    url(r'^project/(?P<id>[\d]+)/(?P<slugProject>[\w-]+)/$', 'project', name="project"),
    url(r'^project/(?P<id>[\d]+)/(?P<slugProject>[\w-]+)/edit/$',
    	'project', {'edit': True}, name="edit-project"),
    
    url(r'^submit_project/$', 'submit_project', name="submit-project"),
    #url(r'^submit_project/success/$', 'submit_project_success', name="submit-project-success"),

    url(r'^signup/$', 'signup', name="signup"),
    #url(r'^signup/success/$', 'signup_success', name="signup-success"),
) + patterns('',
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'hackathon/login.html'}, name="login"),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name="logout"),
)