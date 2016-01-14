from django.shortcuts import render
from django.http import HttpResponse
import json
from .forms import coordsForm




# Create your views here.
def home(request):
    return  render(request, 'deformation/home.html', {})

def input(request):
    if request.method == 'POST':
        form = coordsForm(request.POST)
        if form.is_valid():
            coord = form.cleaned_data['coordsList']
            data = json.loads(coord);
            print (data[0])
            return HttpResponse(coord)
        else:
            return HttpResponse('not valid')
    else:
        form = coordsForm()
    return  render(request, 'deformation/grid.html', {'form': form})

def all(request):
    return  render(request, 'deformation/all.html', {})

def test(request):
    return  render(request, 'deformation/grid.html', {})
