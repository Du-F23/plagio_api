from django.urls import path
import views


urlpatterns=[
    path('v1/search/', views.search_view)
]
