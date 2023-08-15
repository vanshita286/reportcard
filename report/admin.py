from django.contrib import admin
from .models import *
from django.db.models import Sum


admin.site.register(StudentID)
admin.site.register(Student)
admin.site.register(Department)
admin.site.register(Subject)

class SubjectMarksAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'marks']

admin.site.register(SubjectMarks, SubjectMarksAdmin)
class ReportCardAdmin(admin.ModelAdmin):
    list_display = ['student', 'student_rank', 'total_marks']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(total_marks=Sum('student__subjectmarks__marks'))

    def total_marks(self, obj):
        return obj.total_marks
