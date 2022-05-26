from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.loginUser),
    path('admin_register/', views.registerAdmin),
    path('tutorial/', views.tutorial),
    path('faq/', views.faq),
    path('admin_register/admin',admin.site.urls),
    path('user_register/', views.registerUser),
    path('logout/', views.logoutView, name='logout'),
    path('dashboard/',views.dashboard,  name='dashboard'),
    path('position/', views.positionView, name='position'),
    path('result/', views.resultView, name='result'),
    path('editprofile/', views.editProfileView, name='editprofile'),
    path('changepass/', views.changePasswordView, name='changepass'),
    path('candidate/<int:pos>/', views.candidateView, name='candidate'),
    path('candidate/detail/<int:id>/', views.candidateDetailView, name='detail'),
    path('verifyUser/', views.userVerify, name='verify'),
    path('verifyUser/verify',views.verify),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT)