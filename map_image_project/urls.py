from django.contrib import admin
from django.urls import path
from map_image_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/process_coordinates/', views.process_coordinates, name='process_coordinates'),
    # Add other URL patterns as needed
]
