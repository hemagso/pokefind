from django.urls import path

from . import views

app_name = 'annotations'
urlpatterns = [
    path('', views.index, name='index'),
    path('make', views.make),
    path('frame_image/<slug:id>', views.frame_image),
    path('get_frame', views.get_frame),
    path('get_pokemon_list', views.get_pokemon_list)
]
