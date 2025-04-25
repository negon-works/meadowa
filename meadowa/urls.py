
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include('web.urls',namespace='web')),
    path('ckeditor/', include('ckeditor_uploader.urls')),  # Add this line for CKEditor integration
    path('cart/', include('web.urls',namespace='web')),
    path('seller/', include('web.urls', namespace='web')),

]
