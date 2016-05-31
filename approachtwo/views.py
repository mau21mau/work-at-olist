import io
import json
import time
import dicttoxml
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from .models import Category, Channel
from .serializers import ChannelSerializer, CategorySerializer
from core.forms import ImportCsvForm
from approachtwo.management.commands.importcategories_mptt import Command


def approach_two_view(request):
    from approachtwo.serializers import CategorySerializer
    from approachtwo.models import Category
    ctry = Category.objects.all()[0]
    serializer = CategorySerializer(ctry)
    serializer.data
    """
    if request.method == 'POST':
        form = ImportCsvForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            file = io.StringIO(request.FILES['file'].read().decode('utf-8'))
            channel = request.POST['channel']
            c = Command()
            c.override_categories(channel, file)
            form = ImportCsvForm()
        return render(request, 'upload_form.html', {'form': form})
    else:
        form = ImportCsvForm()
    channels = Channel.objects.all()
    return render(request, 'approachone.html', {'channels': channels, 'form': form}, content_type='text/html')
    """


"""
************************************************************************************************************************
-------------------------------------------------- API VIEWS -----------------------------------------------------------
************************************************************************************************************************
"""


def api_channel(request):
    start = int(round(time.time() * 1000))
    key = request.GET.get('uuid', None)
    if not key:
        return HttpResponse('(404) Not Found :(', status=404)
    channel = Channel.channel_from_key(key)

    end = int(round(time.time() * 1000))
    if settings.DEBUG:
        channel_dict['meta'] = {'view_runtime': '%i ms.' % (end - start)}

    if request.GET.get('document', None) == 'xml':
        return HttpResponse(dicttoxml.dicttoxml(channel_dict), content_type='application/xml')
    return HttpResponse(json.dumps(channel_dict), content_type='application/json')


def api_category(request):
    start = int(round(time.time() * 1000))
    key = request.GET.get('uuid', None)
    if not key:
        return HttpResponse('(404) Not Found :(', status=404)
    category = Category.category_from_key(key)
    category_dict = {'data': {}, 'meta': ''}
    category_dict['data'] = category.get_tree()

    end = int(round(time.time() * 1000))
    if settings.DEBUG:
        category_dict['meta'] = {'view_runtime': '%i ms.' % (end - start)}

    if request.GET.get('document', None) == 'xml':
        return HttpResponse(dicttoxml.dicttoxml(category_dict), content_type='application/xml')
    return HttpResponse(json.dumps(category_dict), content_type='application/json')


def api_channels(request):
    start = int(round(time.time() * 1000))
    channels = Channel.objects.all()
    channels_list = {'data': [], 'meta': ''}
    for channel in channels:
        channel_dict = {
            'type':'channel',
            'uuid': channel.id_key().decode('utf-8'),
            'attributes': {
                'name': channel.name
            },
            'relationships': {
                'categories': [],
            }
        }
        root_categories = channel.category_set.filter(parent__isnull=True)
        for category in root_categories:
            category_tree = category.get_tree()
            channel_dict['relationships']['categories'].append(category_tree)
        channels_list['data'].append(channel_dict)
    end = int(round(time.time() * 1000))
    if settings.DEBUG:
        channels_list['meta'] = {'view_runtime': '%i ms.' % (end - start)}

    if request.GET.get('document', None) == 'xml':
        return HttpResponse(dicttoxml.dicttoxml(channels_list), content_type='application/json')
    return HttpResponse(json.dumps(channels_list), content_type='application/json')
"""
************************************************************************************************************************
"""
