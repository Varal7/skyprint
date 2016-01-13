from django.shortcuts import render

# Create your views here.
def home(request):
    return  render(request, 'deformation/home.html', {})

def input(request):
    return  render(request, 'deformation/input.html', {})

def all(request):
    return  render(request, 'deformation/all.html', {})

def test(request):
    return  render(request, 'deformation/grid.html', {})
