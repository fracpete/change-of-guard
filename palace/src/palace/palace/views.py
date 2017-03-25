from django.http import HttpResponse
from django.template import loader

from os import listdir
from os.path import isfile, join

from settings import monitors

def list(request):
    template = loader.get_template('list.html')
    available = []
    for monitor in monitors:
        if monitors[monitor]['enabled']:
            available.append(monitor)
    sorted(available)
    context = {
        'monitors': available,
    }
    return HttpResponse(template.render(context, request))

def list_images(request):
    if "monitor" not in request.GET:
        return HttpResponse()
    monitor = str(request.GET.get("monitor"))
    template = loader.get_template('list_images.html')
    d = monitors[monitor]['output']
    # TODO group by day
    images = [f for f in listdir(d) if isfile(join(d, f))]
    sorted(images)
    context = {
        'monitor': monitor,
        'images': images,
    }
    return HttpResponse(template.render(context, request))

def view_image(request):
    if "monitor" not in request.GET:
        return HttpResponse()
    if "image" not in request.GET:
        return HttpResponse()
    monitor = str(request.GET.get("monitor"))
    image = str(request.GET.get("image"))
    d = monitors[monitor]['output']
    with open(d + "/" + image, "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")
