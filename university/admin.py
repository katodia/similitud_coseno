from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from university.models import *


class AreaAdmin(admin.ModelAdmin):
    list_display = ['id', 'view_name']
    ordering = ['id']
    search_fields = ['name']

    def view_name(self, x):
        base_url = reverse('admin:university_area_change', args=(x.id,))
        return mark_safe('<a href="%s">%s</a>' % (base_url, x.name))


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'view_name', 'area_name']
    ordering = ['id', 'name']
    search_fields = ['name', 'area__name']

    def area_name(self, x):
        base_url = reverse('admin:university_area_change', args=(x.area_id,))
        return mark_safe('<a href="%s">%s</a>' % (base_url, x.area.name))

    def view_name(self, x):
        base_url = reverse('admin:university_course_change', args=(x.id,))
        return mark_safe('<a href="%s">%s</a>' % (base_url, x.name))


class LectureAdmin(admin.ModelAdmin):
    list_display = ['id', 'view_name', 'credits']
    ordering = ['id']
    search_fields = ['name']

    def view_name(self, x):
        base_url = reverse('admin:university_lecture_change', args=(x.id,))
        return mark_safe('<a href="%s">%s</a>' % (base_url, x.name))


class UniversityAdmin(admin.ModelAdmin):
    list_display = ['id', 'view_name', 'description']
    ordering = ['id']

    def view_name(self, x):
        base_url = reverse('admin:university_university_change', args=(x.id,))
        return mark_safe('<a href="%s">%s</a>' % (base_url, x.name))


admin.site.register(University, UniversityAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lecture, LectureAdmin)
