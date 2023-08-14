from django.urls import path
from . import views


urlpatterns=[
    path('v1/search/', views.search_view)
]
