from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('add/', TaskCreateView.as_view(), name='add-task'),
    path('edit/<int:task_id>/', TaskEditView.as_view(), name='edit-task'),
    path('delete-confirmation/<int:task_id>/', DeleteConfirmationView.as_view(), name='delete-confirmation'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
