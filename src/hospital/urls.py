from django.contrib import admin
from django.urls import path, include

from .views import home_view, login_view, logout_view, instruction_db_fill_test

urlpatterns = [
    path('test_fill/', instruction_db_fill_test, name='test_fill')
]