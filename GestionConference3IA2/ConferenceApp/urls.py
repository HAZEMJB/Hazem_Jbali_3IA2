from django.urls import path
from . import views
from .views import *
urlpatterns =[
    path('conferences/', views.ConferenceList.as_view(), name='conference_list'),
    
 #path("liste/", views.list_conferences, name="liste_conferences"),
    path("liste/",ConferenceList.as_view(),name="liste_conferences"),
    path("<int:pk>/",ConferenceDetails.as_view(),name="conference_details"),
    path("add/",ConferenceCreate.as_view(),name="conference_add"),
    path("edit/<int:pk>/",ConferenceUpdate.as_view(),name="conference_update"),
     path("delete/<int:pk>/",ConferenceDelete.as_view(),name="conference_delete"),
     path('submissions/', views.ListSubmissions.as_view(), name='list_submissions'),
     path('submissions/add/', views.AddSubmission.as_view(), name='add_submission'),
    path('submissions/<str:submission_id>/', views.DetailSubmission.as_view(), name='detail_submission'),
    path('submissions/<str:submission_id>/download/', views.download_paper, name='download_paper'),
    path('submissions/<str:submission_id>/update/', views.UpdateSubmission.as_view(), name='update_submission'),


]