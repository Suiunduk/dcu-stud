from django.urls import path, include

from university_employee import views
from university_employee.views import EmployeeDetailView, EmployeeCreateView, EmployeeUpdateView, EmployeeDeleteView

urlpatterns = [
    path('signup/', views.EmployeeSignUpView.as_view(), name='signup'),
    path('<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('create/<int:fk>', EmployeeCreateView.as_view(), name='employee-create'),
    path('<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee-delete'),

]
