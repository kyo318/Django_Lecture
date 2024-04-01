from django.urls import path 
from . import views 

app_name = 'chem'

urlpatterns = [
  path("test/", views.index, name="index"),
]