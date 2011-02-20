from django.conf.urls.defaults import *

urlpatterns = patterns('hackathon.views',
    url(r'^$', 'index', name="index"),
    url(r'^person/(?P<slugPerson>[\w-]+)/$', 'person', name="person"),
    url(r'^project/(?P<slugProject>[\w-]+)/$', 'project', name="project"),

    # Haven't looked at yet, but these are placeholders...
    url(r'^project_sign_up/$', 'project_sign_up', name="project_sign_up"),
    url(r'^signup/$', 'signup', name="signup"),
) + patterns('',
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'hackathon/login.html'}, name="login"),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {}, name="logout"),
)