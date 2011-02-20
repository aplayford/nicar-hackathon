from django.contrib import admin

from hackathon.models import Person, Project, ProjectNeed, ProjectStaff, RoleChoice

########################
## Person admin pages ##
########################

class PersonAdmin(admin.ModelAdmin):
    pass
admin.site.register(Person, PersonAdmin)

#########################
## Project admin pages ##
#########################

class ProjectNeedInline(admin.TabularInline):
    model = ProjectNeed

class ProjectStaffInline(admin.TabularInline):
    model = ProjectStaff

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectStaffInline, ProjectNeedInline]
admin.site.register(Project, ProjectAdmin)

##############
## Defaults ##
##############

admin.site.register(RoleChoice)