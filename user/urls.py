
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name = 'logout'),
    path('profile/<int:pk>/', views.profile_view, name='profile_view'),
    path('people/', views.people, name='people'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)