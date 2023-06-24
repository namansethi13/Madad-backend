from django.urls import path
from django.conf import settings
from donations import views
from django.conf.urls.static import static
urlpatterns = [
    path('create/', views.createdonation, name='createdonation') ,
    path('',views.showdonations,name='showdonations'),
    path('userdonations',views.showdonations,name='showdonations'),
    path('updatedonation/<int:id>',views.updatedonation,name='updatedonation'),
    path('deletedonation/<int:id>',views.deletedonation,name='deletedonation')

]
#urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
