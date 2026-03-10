from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('web.urls', namespace='web')),
    path('ckeditor/', include('ckeditor_uploader.urls')),  # Add this line for CKEditor integration
    path('cart/', include('web.urls', namespace='web')),
    path('seller/', include('web.urls', namespace='web')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
