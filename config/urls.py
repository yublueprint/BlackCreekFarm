from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('app.urls')), 
]

if settings.ENABLE_SILK:
    urlpatterns += [
        path("silk/", include("silk.urls", namespace="silk")),
    ]

if settings.DEBUG:
    # urlpatterns += [
    #         path('__debug__/', include('debug_toolbar.urls')),
    #     ]
    pass