from django.conf.urls.defaults import *


urlpatterns = patterns('hackathon.views',
    (r'^$', 'index'),
    (r'^login/$', 'login'),
    (r'^person/(?P<slugPerson>[\w-])/$', 'person'),
    (r'^project/(?P<slugProject>[\w-])/$', 'project'),

    # Haven't looked at yet, but these are placeholders...
    (r'^project_sign_up/$', 'project_sign_up'),
    (r'^signup/$', 'signup'),
)