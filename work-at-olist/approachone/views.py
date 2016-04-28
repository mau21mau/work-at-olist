import json
import dicttoxml
from django.http import HttpResponse
from django.shortcuts import render
from .models import Category, Channel


def approach_one_view(request):
    channels = Channel.objects.all()
    return render(request, 'approachone.html', {'channels': channels})


"""
************************************************************************************************************************
-------------------------------------------------- API VIEWS -----------------------------------------------------------
************************************************************************************************************************
"""


def api_channel(request):
    key = request.GET.get('uuid', None)
    if not key:
        return HttpResponse('(404) Not Found :(', status=404)
    channel = Channel.channel_from_key(key)
    channel_dict = {'channelName': channel.name, 'categories': [], 'uuid': channel.id_key().decode("utf-8")}
    root_categories = channel.category_set.filter(parent__isnull=True)
    for category in root_categories:
        category_tree = category.get_tree()
        channel_dict['categories'].append(category_tree)

    if request.GET.get('document', None) == 'xml':
        return HttpResponse(dicttoxml.dicttoxml(channel_dict), content_type='application/xml')
    return HttpResponse(json.dumps(channel_dict), content_type='application/json')


def api_category(request):
    key = request.GET.get('uuid', None)
    if not key:
        return HttpResponse('(404) Not Found :(', status=404)
    category = Category.category_from_key(key)
    category_dict = category.get_tree()
    if request.GET.get('document', None) == 'xml':
        return HttpResponse(dicttoxml.dicttoxml(category_dict), content_type='application/xml')
    return HttpResponse(json.dumps(category_dict), content_type='application/json')


def api_channels(request):
    channels = Channel.objects.all()
    channels_list = []
    for channel in channels:
        channel_dict = {
            'channelName': channel.name,
            'categories': [],
            'uuid': channel.id_key().decode("utf-8"),
        }
        root_categories = channel.category_set.filter(parent__isnull=True)
        for category in root_categories:
            category_tree = category.get_tree()
            channel_dict['categories'].append(category_tree)
        channels_list.append(channel_dict)

    if request.GET.get('document', None) == 'xml':
        return HttpResponse(dicttoxml.dicttoxml(channels_list), content_type='application/json')
    return HttpResponse(json.dumps(channels_list), content_type='application/json')
"""
************************************************************************************************************************
"""
