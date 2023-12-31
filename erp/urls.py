from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/im/', include('im.urls')),
    path('api/user/', include('user.urls')),
    path('api/auth/', include('auth.urls')),
    path('api/crm/', include('crm.urls')),
    path('api/comments/', include('comments.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)