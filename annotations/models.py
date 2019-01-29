from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    """ Image

    This model represent a frame from a Pokemon Episode.
    """
    season = models.IntegerField()
    episode = models.IntegerField()
    frame = models.IntegerField()


class Annotation(models.Model):
    """ Annotation

    This model represent an annotation of a frame made by one user. One
    annotation is associated with a frame, and may be associated with various
    AreaAnnotation models through its primary key.
    """
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField()


class Pokemon(models.Model):
    """ Annotation

    This model represent a Pokemon.

    :todo Remove thumbnail field from this model
    """
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    thumbnail = models.FilePathField()


class AreaAnnotation(models.Model):
    """ Annotation

    This model represent an area annotated in a frame. It is associated with an
    Annotation object through a foreign key. Positions and Dimensions are given
    in terms of a percentage of the frame dimensions.

    :todo Add constraint on x, y, width and height fields
    """
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, null=True)
