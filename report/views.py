from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student
from django.core.paginator import Paginator
from report.models import SubjectMarks
from django.db.models import Q , Sum

# Create your views here.

def get_students(request):
        queryset = Student.objects.all()

        ranks = Student.objects.annotate(marks = Sum('studentmarks__marks')).order_by('-marks','-student_age')
        for rank in ranks:
            print(rank.marks)
        if request.GET.get('search'):
            search = request.GET.get('search')
            queryset =  queryset.filter(
                Q(student_name__icontains = search) |
                Q(department__department__icontains = search)|
                Q(student_id__student_id__icontains = search)|
                Q(student_email__icontains = search)|
                Q(student_age__icontains = search)
            )
        paginator = Paginator(queryset, 15) 

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        return render (request, 'report/student.html',{'queryset':page_obj})

def see_marks(request, student_id):
   
    queryset = SubjectMarks.objects.filter(student__student_id__student_id=student_id)
    total_marks = queryset.aggregate(total_marks = Sum('marks'))     
    current_rank = 1
    ranks = Student.objects.annotate(marks = Sum('studentmarks__marks')).order_by('-marks','-student_age')
    i = 1
    for rank in ranks:
        if student_id == rank.student_id.student_id:
            current_rank = i
            break
        i=i+1


    return render (request,'report/see_marks.html',{'queryset':queryset ,'total_marks':total_marks, 'current_rank':current_rank}) 
