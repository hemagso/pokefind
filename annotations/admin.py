from django.contrib import admin
from .models import Image, Annotation, Pokemon, AreaAnnotation

admin.site.register(Image)
admin.site.register(Annotation)
admin.site.register(Pokemon)
admin.site.register(AreaAnnotation)
