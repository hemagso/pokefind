from django.db import models
from django.contrib.auth.models import User
from hashid_field import HashidAutoField

class FAQGroup(models.Model):
    name = models.CharField(max_length=64, default="")
    priority = models.IntegerField(default=999)

    def __str__(self):
        return "FAQGroup: {name}".format(name=self.name)


class FAQItem(models.Model):
    group = models.ForeignKey(FAQGroup, on_delete=models.CASCADE)
    question = models.CharField(max_length=128, default="")
    answer = models.TextField(default="")
    priority = models.IntegerField(default=999)

    def __str__(self):
        words = self.question.split()
        if len(words) > 4:
            question = " ".join(words[0:4]) + "..."
        else:
            question = self.question
        return "[{group}] {question}".format(group=self.group.name, question=question)


class Image(models.Model):
    """ Image

    This model represent a frame from a Pokemon Episode.
    """
    season = models.IntegerField()
    episode = models.IntegerField()
    frame = models.IntegerField()
    id = HashidAutoField(primary_key = True, allow_int_lookup=True)


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
    comment = models.CharField(max_length=64, default="")
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, null=True)
