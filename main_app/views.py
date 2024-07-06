from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .models import Event, Photo
import uuid # this is used to create unique id. allow us to create unique file names and url for each photo uploaded
import boto3 # this is the SDK, all the functions that Amazon develpers wrote
import os
import requests
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

    def get_queryset(self):
        filter = self.request.GET.get('filter', None)
        print(filter)
        if filter == 'created':
            return Event.objects.filter(user=self.request.user)# This is the currently authenticated user making the request.
        elif filter == 'attending':
            return None
        else:
            return Event.objects.filter(user=self.request.user) #to display just the logged in user's events?


            
        # if filter = created events, return all the events the user created
        # if filter = attending, return all the events the user is attending
        # else if there is no filter, return all the events.
        

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
        self.object = form.save() 
        print(self.request.FILES)

        photo_file = self.request.FILES.get('photo-file', None)
        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            try:
                bucket = os.environ['S3_BUCKET']
                s3.upload_fileobj(photo_file, bucket, key)
                url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                Photo.objects.create(url=url, event_id=self.object.id)
            except Exception as e:
                print('An error occurred uploading file to S3')
                print(e)
        # this is where you will create a new photo and associated with the event. 
        return HttpResponseRedirect(self.get_success_url())
    
class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['name', 'short_summary','category', 'date', 'time', 'location', 'about', 'age_restriction']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save() 
        print(self.request.FILES)

        photo_file = self.request.FILES.get('photo-file', None)
        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            try:
                bucket = os.environ['S3_BUCKET']
                s3.upload_fileobj(photo_file, bucket, key)
                url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                Photo.objects.create(url=url, event_id=self.object.id)
            except Exception as e:
                print('An error occurred uploading file to S3')
                print(e)
        # this is where you will create a new photo and associated with the event. 
        return HttpResponseRedirect(self.get_success_url())

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