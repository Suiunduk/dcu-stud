from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView

from announcement.models import Announcement, AnnouncementDocument
from university_employee.models import Employee
from student_abroad.models import StudentAbroad
from student_foreign.models import StudentForeign
from university_local.models import University
from users.models import CustomUser


def homepage(request):
    if request.user.is_authenticated:
        user = request.user
        customUser = CustomUser.objects.get(id=user.id)

        if customUser.is_superuser:
            students_count = StudentAbroad.objects.all().count()
            universities_count = University.objects.all().count()
            employees_count = Employee.objects.all().count()
            return render(request, 'core/admin_homepage.html', {"students_count": students_count,
                                                                "universities_count": universities_count,
                                                                "employees_count": employees_count})

        elif customUser.user_type == 'university_employee':
            employee = Employee.objects.get(user_id=customUser.id)
            students_count_for_emp = StudentAbroad.objects.filter(edu_organisation=employee.edu_organisation).count()
            return render(request, 'core/employee_homepage.html', {"students_count": students_count_for_emp})


        else:
            return render(request, 'core/student_homepage.html')

    else:
        students_count = StudentAbroad.objects.all().count()
        students_count_by_country = StudentAbroad.objects.all().values('education_country'). \
                                        annotate(count=Count('education_country')).order_by('-count')[:10]
        students_country_count = StudentAbroad.objects.values('education_country').distinct().count()
        abr_students_count = StudentForeign.objects.all().count()
        abr_students_count_by_country = StudentForeign.objects.all().values('country'). \
                                            annotate(count=Count('country')).order_by('-count')[:10]
        abr_students_count_by_uni = StudentForeign.objects.all().values('edu_organisation__org_name'). \
                                        annotate(count=Count('edu_organisation')).order_by('-count')[:10]
        abr_students_country_count = StudentForeign.objects.values('country').distinct().count()

        announcements = Announcement.objects.all()
        announcement_docs = AnnouncementDocument.objects.all()

        return render(request, 'core/landing/landing_page.html', {"students_count": students_count,
                                                                  "students_count_by_country":
                                                                      students_count_by_country,
                                                                  "students_country_count": students_country_count,
                                                                  "abr_students_count": abr_students_count,
                                                                  "abr_students_count_by_country":
                                                                      abr_students_count_by_country,
                                                                  "abr_students_count_by_uni":
                                                                      abr_students_count_by_uni,
                                                                  "abr_students_country_count":
                                                                      abr_students_country_count,
                                                                  "announcements": announcements,
                                                                  "announcement_docs": announcement_docs})


class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = "core/landing/announcement_landing.html"

    def get_context_data(self, **kwargs):
        context = super(AnnouncementDetailView, self).get_context_data(**kwargs)
        context['documents'] = AnnouncementDocument.objects.filter(announcement=self.kwargs['pk'])
        return context
