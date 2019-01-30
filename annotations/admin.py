from django.contrib import admin
from .models import Image, Annotation, Pokemon, AreaAnnotation, FAQItem, FAQGroup

admin.site.register(Image)
admin.site.register(Annotation)
admin.site.register(Pokemon)
admin.site.register(AreaAnnotation)
admin.site.register(FAQItem)
admin.site.register(FAQGroup)
