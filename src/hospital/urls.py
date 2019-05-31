from django.urls import path

from .views import home_view, login_view, logout_view, show_case_view, MedicamentListView, show_med_instruction_view
from .utils import instruction_db_fill_test_view


urlpatterns = [
    path('', home_view, name='home'),
path('test_fill/<int:mn>/<int:mx>/', instruction_db_fill_test_view, name='test_fill'),
    # auth
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('medicament/', MedicamentListView.as_view(), name='medicament'),
    path('medicament/<int:pk>/', show_med_instruction_view, name='show_med_instruction'),
    # patient
    # path('case/create/', create_case_view, name="create_case"),
    path('case/<int:pk>/', show_case_view, name="show_case"),
    # path('case/<int:pk>/edit/', edit_case_view, name="edit_person"),
    # path('case/<int:pk>/delete/', delete_case_view, name="delete_case"),
]
