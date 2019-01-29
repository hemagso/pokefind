# Django boilerplate
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Max

# Data models
from .models import Pokemon, Annotation, AreaAnnotation, Image

# Standard library
from datetime import datetime
import json
import random


def index(request):
    """" index view

    Renders the main webpage of the application

    :param request: The HTTP request sent by the client
    :return Rendered template of the application

    """
    context = {
        "pokemon_list": Pokemon.objects.all()
    }
    return render(request, 'annotations/index.html', context)


def make(request):
    """" make view

    Submit a new annotation to the database.

    :param request: The HTTP request sent by the client
    :return String containing "OK"

    todo: Add error handling and feedback to the client
    """
    areas = json.loads(request.POST["annotations"])
    frame_id = int(request.POST["frame_id"])

    img = Image.objects.get(pk=frame_id)

    annotation = Annotation()
    annotation.image = img
    annotation.timestamp = datetime.now()
    annotation.save()

    for area in areas:
        new_area = AreaAnnotation()
        new_area.annotation = annotation
        new_area.width = area["bbox"]["width"]
        new_area.height = area["bbox"]["height"]
        new_area.x = area["bbox"]["x"]
        new_area.y = area["bbox"]["y"]
        if area["id"]:
            new_area.pokemon = Pokemon.objects.get(id=area["id"])
        new_area.save()

    return HttpResponse("OK")


def frame_image(request, id):
    """" frame_image view

    Serve one frame of an specific Pokemon Episode

    :param request: The HTTP Request sent by the client
    :param id: ID of the frame requested
    :return HttpResponse object containing the image

    todo: Add error handling and feedback to the client
    """
    img = Image.objects.get(id=id)
    img_path = "annotations/data/frames/season_{season:02d}/episode_{episode:03d}/frame_{frame:09d}.jpg".format(
        season=img.season,
        episode=img.episode,
        frame=img.frame
    )
    with open(img_path, "rb") as f:
        img_data = f.read()
        return HttpResponse(img_data, content_type="image/jpg")


def get_frame(request):
    """" get_frame view

    Select one random frame ID to be sent over to the client

    :param request: The HTTP Request sent by the client
    :return HttpResponse object containing the JSON representation of a frame and its metadata

    todo: Do a better random frame selection
    todo: Integrate with login so as not to serve repeated images to the same user (Low-priority)
    """
    max_id = Image.objects.all().aggregate(max_id=Max("id"))["max_id"]
    frame = None
    while not frame:
        pk = random.randint(1, max_id)
        frame = Image.objects.filter(pk=pk).first()
    ret_data = {
        "id": frame.pk,
        "season": frame.season,
        "episode": frame.episode,
        "frame": frame.frame
    }
    return HttpResponse(json.dumps(ret_data))