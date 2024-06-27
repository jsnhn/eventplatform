from django.shortcuts import render

# Create your views here.

events = [
  {'name': 'Lolo'}
]

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def events_index(request):
    return render(request, 'events/index.html', {
        'events': events
    })