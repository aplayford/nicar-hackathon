from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string

class SluggedModel(models.Model):
    slug = models.SlugField(max_length=50, blank=True,
                            help_text="If you leave this blank, it will be filled in with magic!")

    def save(self, *args, **kwargs):
        if not self.slug:
            if hasattr(self, "slug_text"):
                slug_text = self.slug_text()
            else:
                slug_text = unicode(self)
        
            self.slug = slugify(slug_text)

        return super(SluggedModel, self).save(*args, **kwargs)
    
    class Meta:
        abstract = True

class Person(SluggedModel):
    user = models.OneToOneField('auth.User', blank=True)
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    
    skills_summary = models.TextField(blank=True)

    roles_willing = models.ManyToManyField('RoleChoice', blank=True, verbose_name="willing to help with:")

    website = models.URLField(blank=True)

    def __unicode__(self):
        return u"%s" % self.name
    
    class Meta:
        verbose_name_plural = "people"
    
    @models.permalink
    def get_absolute_url(self):
        return ('person', [], {'slugPerson': self.slug, 'id': self.id})

    @models.permalink
    def get_edit_url(self):
        return ('edit-person', [], {'slugPerson': self.slug, 'id': self.id})

class Project(SluggedModel):
    name = models.CharField(max_length=150)
    description = models.TextField()
    website = models.URLField(blank=True)
    repo = models.URLField(blank=True)

    def __unicode__(self):
        return u"%s" % self.name
    
    def leaders(self):
        return list(self.staff.filter(team_leader=True))

    def is_leader(self, pers):
        try:
            self.staff.get(team_leader=True, person=pers)
            return True
        except:
            return False
    
    @models.permalink
    def get_absolute_url(self):
        return ('project', [], {'slugProject': self.slug, 'id': self.id})
    
    @models.permalink
    def get_edit_url(self):
        return ('edit-project', [], {'slugProject': self.slug, 'id': self.id})

###########$###########
## Request models    ##
## For inline forms  ##
############$##########

class JoinProjectRequest(models.Model):
    project = models.ForeignKey('Project', related_name="volunteer_requests")
    volunteer = models.ForeignKey('Person', related_name="projects_volunteered")
    
    status = models.CharField(max_length=3, choices=(('YES', 'Yes'), ('NO', 'No'),), blank=True)

    do_send = models.BooleanField(default=False)
    do_answer = models.BooleanField(default=False)
    
    queued_for = models.ManyToManyField('Person', related_name="requests_waiting")
    respondent = models.ForeignKey('Person', blank=True, null=True)

    @models.permalink
    def get_yes_url(self):
        return ('project-request-respond', [], {'id': self.id, 'ans': "yes"})
    @models.permalink
    def get_no_url(self):
        return ('project-request-respond', [], {'id': self.id, 'ans': "no"})
    @models.permalink
    def get_absolute_url(self):
        return ('project-request', [], {'id': self.id})


    def send_request(self):
        varsContext = {
            "volunteer": self.volunteer,
            "project": self.project,
            "req": self
        }

        for staff in self.project.leaders():
            staff.person.user.email_user(
                "Someone wants to join your hackathon project",
                render_to_string("hackathon/emails/volunteer.txt", varsContext),
                from_email = "hackathon@nicar.adamplayford.com"
            )
            self.queued_for.add(staff.person)
        
        self.do_send = False
        self.save()
    
    def queue_response(self, ans, respondent):
        self.do_answer = True
        self.status = ans.upper()
        if respondent:
            self.respondent = respondent
        
        if ans.lower() == "yes":
            self.project.staff.create(
               person=self.volunteer
            )

        self.save()
    
    def send_response(self):
        code = self.status.lower()

        varsContext = {
            "req": self,
            "project": self.project
        }

        self.volunteer.user.email_user(
            "Hackathon Project: %s" % self.project.name,
            render_to_string("hackathon/emails/response_%s.txt" % code, varsContext),
            from_email = "hackathon@nicar.adamplayford.com"
        )

        self.do_answer = False
        self.save()

###########$###########
## F-keyed models    ##
## For inline forms  ##
############$##########

class ProjectNeed(models.Model):
    project = models.ForeignKey("Project", related_name="needs")
    role_needed = models.ForeignKey('RoleChoice')
    number_slots = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        if self.number_slots > 1:
            return u"%s (%s)" % (self.role_needed, self.number_slots)
        else:
            return u"%s" % self.role_needed

class ProjectStaff(models.Model):
    project = models.ForeignKey("Project", related_name="staff")
    person = models.ForeignKey("Person", related_name="projects")
    #roles = models.ManyToManyField('RoleChoice', blank=True)
    team_leader = models.BooleanField()

    def __unicode__(self):
        return u"%s" % self.person

    class Meta:
        verbose_name_plural = "project staff"
        unique_together = ('team_leader', 'project',)
    
    def get_absolute_url(self):
        return self.person.get_absolute_url()

######################
## Helper models    ##
## 'Choices' for FK ##
######################

class ChoiceModel(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        abstract = True
        ordering = ('name',)

class RoleChoice(ChoiceModel):
    pass