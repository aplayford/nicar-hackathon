from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField
from django.template.defaultfilters import slugify

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
    
    def leader(self):
        try:
            return self.staff.get(team_leader=True)
        except ProjectStaff.DoesNotExist:
            return None
    
    @models.permalink
    def get_absolute_url(self):
        return ('project', [], {'slugProject': self.slug, 'id': self.id})
    
    @models.permalink
    def get_edit_url(self):
        return ('edit-project', [], {'slugProject': self.slug, 'id': self.id})


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
    roles = models.ManyToManyField('RoleChoice', blank=True)
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