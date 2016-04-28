from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView


class IndexView(ListView):
    def get(self, request):
        return render(request, 'index.html', {'foo': 'bar'})
