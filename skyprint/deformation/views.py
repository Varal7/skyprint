from django.shortcuts import render
from django.http import HttpResponse
from .forms import coordsForm
from django.shortcuts import redirect

from .scripts.processSimple import *





# Create your views here.
def home(request):
    return  render(request, 'deformation/home.html', {})

def input(request):
    if request.method == 'POST':
        form = coordsForm(request.POST)
        if form.is_valid():
            coordsList = form.cleaned_data['coordsList']
            res = resFromCoords(coordsList)
            return render(request, 'deformation/result.html', {'coordsList' : coordsList, 'res' : res})
        else:
            return HttpResponse('not valid')
    else:
        form = coordsForm()
    return  render(request, 'deformation/grid.html', {'form': form})

def all(request):
    return  render(request, 'deformation/all.html', {})

def test(request):
    return  render(request, 'deformation/grid.html', {})
