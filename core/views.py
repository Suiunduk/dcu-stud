from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from employees.models import Employee
from students.models import Student
from universities.models import University
from users.models import CustomUser


def homepage(request):
    if request.user.is_authenticated:
        user = request.user
        customUser = CustomUser.objects.get(id=user.id)

        if customUser.is_superuser:
            students_count = Student.objects.all().count()
            universities_count = University.objects.all().count()
            employees_count = Employee.objects.all().count()
            return render(request, 'core/admin_homepage.html', {"students_count": students_count,
                                                                "universities_count": universities_count,
                                                                "employees_count": employees_count})

        elif customUser.is_employee:
            employee = Employee.objects.get(user_id=customUser.id)
            students_count_for_emp = Student.objects.filter(university=employee.university).count()
            return render(request, 'core/employee_homepage.html', {"students_count": students_count_for_emp})

        else:
            return render(request, 'core/student_homepage.html')

    else:
        return render(request, 'core/landing_page.html')
