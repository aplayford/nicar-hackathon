from django.core.management.base import NoArgsCommand

from hackathon.models import JoinProjectRequest

class Command(NoArgsCommand):
    def handle_noargs(self, *args, **kwargs):
        for p in JoinProjectRequest.objects.filter(do_send=True):
            p.send_request()
        for p in JoinProjectRequest.objects.filter(do_answer=True):
            p.send_response()