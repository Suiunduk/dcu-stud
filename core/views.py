from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from university_employee.models import Employee
from student_abroad.models import StudentAbroadCommon
from student_foreign.models import StudentForeign
from university_local.models import University
from users.models import CustomUser


def homepage(request):
    if request.user.is_authenticated:
        user = request.user
        customUser = CustomUser.objects.get(id=user.id)

        if customUser.is_superuser:
            students_count = StudentAbroadCommon.objects.all().count()
            universities_count = University.objects.all().count()
            employees_count = Employee.objects.all().count()
            return render(request, 'core/admin_homepage.html', {"students_count": students_count,
                                                                "universities_count": universities_count,
                                                                "employees_count": employees_count})

        elif customUser.is_employee:
            employee = Employee.objects.get(user_id=customUser.id)
            students_count_for_emp = StudentAbroadCommon.objects.filter(university=employee.university).count()
            return render(request, 'core/employee_homepage.html', {"students_count": students_count_for_emp})

        else:
            return render(request, 'core/student_homepage.html')

    else:
        students_count = StudentAbroadCommon.objects.all().count()
        students_count_by_country = StudentAbroadCommon.objects.all().values('education_country').\
            annotate(count=Count('education_country')).order_by('-count')
        students_country_count = StudentAbroadCommon.objects.values('education_country').distinct().count()
        abr_students_count = StudentForeign.objects.all().count()
        abr_students_count_by_country = StudentForeign.objects.all().values('country').\
            annotate(count=Count('country')).order_by('-count')
        abr_students_count_by_uni = StudentForeign.objects.all().values('university__university_name').\
            annotate(count=Count('university')).order_by('-count')
        abr_students_country_count = StudentForeign.objects.values('country').distinct().count()

        return render(request, 'core/landing_page.html', {"students_count": students_count,
                                                          "students_count_by_country": students_count_by_country,
                                                          "students_country_count": students_country_count,
                                                          "abr_students_count": abr_students_count,
                                                          "abr_students_count_by_country": abr_students_count_by_country,
                                                          "abr_students_count_by_uni": abr_students_count_by_uni,
                                                          "abr_students_country_count": abr_students_country_count})
