from django.urls import path
from django.conf import settings
from donations import views
from django.conf.urls.static import static
urlpatterns = [
    path('create/', views.createdonation, name='createdonation') ,
    path('',views.showdonations,name='showdonations'),
    path('userdonations/<int:user_id>',views.showdonationsforuser,name='showdonations'),
    path('updatedonation/<int:id>',views.updatedonation,name='updatedonation'),
    path('deletedonation/<int:id>',views.deletedonation,name='deletedonation'),
    path('claim/<int:donation_id>', views.claimdonation, name='claimdonation'),
    path('approve/<int:noti_id>', views.approvenoti, name='approvenoti'),
    path('rate/<int:noti_id>', views.submitrating, name='submitrating'),
]
#urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
