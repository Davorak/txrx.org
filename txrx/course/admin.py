from django.contrib import admin
from django import forms
from widgets import CKEditor
from course.models import Subject, Course, Section, Session, Enrollment, Term

class SubjectAdmin(admin.ModelAdmin):
    pass

class SectionInline(admin.TabularInline):
    extra = 0
    model = Section
    exclude = ("description","images",'location',"tools")

class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("subjects",)
    inlines = (SectionInline,)

class SectionAdmin(admin.ModelAdmin):
    list_display = ("course","user","starttime","hours","sessions","full","cancelled")
    list_editable = ("user","starttime","hours","sessions","full","cancelled")
    

class SessionAdmin(admin.ModelAdmin):
    pass

class EnrollmentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Subject,SubjectAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Section,SectionAdmin)
#admin.site.register(Enrollment,EnrollmentAdmin)
#admin.site.register(Session,SessionAdmin)
admin.site.register(Term)
