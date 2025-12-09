from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",RedirectView.as_view(url="conferences/liste/")),
    path('conferences/', include('ConferenceApp.urls')),
    path('user/', include('UserApp.urls'))
]
