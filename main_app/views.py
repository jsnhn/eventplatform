from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, ListView, DetailView
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

class EventList(ListView):
    model = Event
    template_name = 'events/index.html' #file location
    context_object_name = 'events' # specify the name of the context variable that will be used in the template

# def events_detail(request, event_id): #'events/<int:event_id>/' this determined the parameter name for event_id
#     event = Event.objects.get(id=event_id) #DetailView automatically retrieves the object based on the primary key provided in the URL pattern. It uses the pk field by default, which should match the primary key of the model. you would need the code on the left if the path was 'events/<int:event_id>/'
#     return render(request, 'events/detail.html', {
#         'event': event
#     })

class EventDetail(DetailView):
    model = Event
    template_name = 'events/detail.html'
    context_object_name = 'event' #single instance of an object

class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['name', 'short_summary','category', 'date', 'time', 'location', 'about', 'age_restriction']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)