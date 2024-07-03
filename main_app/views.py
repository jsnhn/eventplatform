from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event

# Create your views here.


class HomeView(TemplateView):
    template_name = 'home.html'

class AboutView(TemplateView):
    template_name = 'about.html'

# def events_index(request):
#     events = Event.objects.all()
#     return render(request, 'events/index.html', {
#         'events': events
#     })

class EventList(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/index.html' #file location
    context_object_name = 'events' # specify the name of the context variable that will be used in the template
    #TODO how to to display just the logged in user's events?

# def events_detail(request, event_id): #'events/<int:event_id>/' this determined the parameter name for event_id
#     event = Event.objects.get(id=event_id) #DetailView automatically retrieves the object based on the primary key provided in the URL pattern. It uses the pk field by default, which should match the primary key of the model. you would need the code on the left if the path was 'events/<int:event_id>/'
#     return render(request, 'events/detail.html', {
#         'event': event
#     })


class EventDetail(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'events/detail.html'
    context_object_name = 'event' #single instance of an object


class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['name', 'short_summary','category', 'date', 'time', 'location', 'about', 'age_restriction']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['name', 'short_summary','category', 'date', 'time', 'location', 'about', 'age_restriction']
    

class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = '/events'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)