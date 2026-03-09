from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include("app.urls")),
]

if getattr(settings, "ENABLE_SILK", False):
    urlpatterns += [
        path("silk/", include("silk.urls", namespace="silk")),
    ]

if settings.DEBUG:
    # Serve static files in development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
