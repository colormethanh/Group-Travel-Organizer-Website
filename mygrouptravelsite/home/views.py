from asyncio import events
from dataclasses import fields
from django import views
from django.db import IntegrityError
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Going, Trip, Event

from mygrouptravelsite.owner import OwnerListView, OwnerDetailView, OwnerDeleteView
from home.forms import TripForm, EventForm, TripJoinForm


# Create your views here.

""" Landing page view """
def HomePage(request):
    template_name = "home/home_page.html"
    return render (request, template_name)


""" Views for TRIPs """
class TripListView(OwnerListView):
    model = Trip
    template_name = "home/trip_list.html"


class TripCreateView(LoginRequiredMixin, View):
    template_name = 'home/trip_form.html'
    fields = ['name', 'start_date', 'end_date']
    success_url = reverse_lazy('home:trip_list')

    def get(self, request, pk=None):
        form = TripForm
        ctx = {
            'form': form,
            'title': 'Trip Creation'
            }
        return render(request, self.template_name, ctx)
    
    def post(self, request, pk=None):
        form = TripForm(request.POST)
        if not form.is_valid():
            ctx = {'form':form}
            return render(request, self.template_name, ctx)
        trip = form.save(commit=False)
        trip.owner = self.request.user
        trip.save()
        return redirect(self.success_url)

class TripDetailView(OwnerDetailView):
    template_name = "home/trip_detail.html"

    def get(self, request, pk):
        t = Trip.objects.get(id=pk)
        events = Event.objects.filter(trip=t)
        event_dict = dict()
        members = Going.objects.filter(trip=t)
        user = self.request.user

        for ct, event in enumerate(events):
            key = 'event'+str(ct)
            event_dict[key] = event
        
        ismember = t.ismember(user.id)
        ctx = {'trip': t, 'events':event_dict, 'members': members, 'ismember': ismember}
        return render(request, self.template_name, ctx)

class TripDeleteView(OwnerDeleteView):
    model = Trip
    success_url = reverse_lazy('home:trip_list')

class TripUpdateView(LoginRequiredMixin, View):
    template_name = 'home/trip_form.html'
    fields = ['name', 'start_date', 'end_date']

    def get(self, request, pk):
        trip = get_object_or_404(Trip, id=pk, owner=self.request.user)
        events = Event.objects.filter(trip=pk)

        form = TripForm(instance=trip)
        ctx = {'form':form,
            'trip': trip, 
            'events':events,
            'title': 'Trip Update'
            }
        return render(request, self.template_name, ctx)
    
    def post(self, request, pk=None):
        trip = get_object_or_404(Trip, id=pk, owner=self.request.user)
        form = TripForm(request.POST, instance=trip)

        success_url = reverse_lazy('home:trip_detail', kwargs={'pk':trip.id})

        if not form.is_valid():
            ctx = {'form':form}
            return render(request, self.template_name, ctx)
        
        form = form.save()
        return redirect(success_url)

class TripJoin(LoginRequiredMixin, View):
    template_name = 'home/trip_form.html'

    def get(self, request, pk):
        trip = get_object_or_404(Trip, id=pk)
        ctx = {'trip': trip, 'form':TripJoinForm()}
        return render (request, self.template_name, ctx)
    
    def post(self, request, pk):
        trip = get_object_or_404(Trip, id=pk)
        form = TripJoinForm(request.POST)
        success_url = reverse_lazy('home:trip_detail', kwargs={'pk':trip.id})

        if not form.is_valid():
            ctx = {'trip': trip, 'form': form}
            return render(request, self.template_name, ctx)
        
        entered = form.cleaned_data['trip_key']
        key = trip.key
        user = self.request.user
        

        if entered == key:
            print(" Adding user to trip ")
            going = Going(trip=trip, user=user)
            try:
                going.save()
            except IntegrityError as e:
                pass
            return redirect(success_url)
        else:
            ctx = {'trip': trip, 'form': form, 'error_message': 'Key error, make sure you typed the key correctly'}
            return render(request, self.template_name, ctx )


        
    



""" Views for EVENTs """
class EventCreateView(LoginRequiredMixin, View):
    model = Event
    template_name = 'home/trip_form.html'


    def get(self, request, pk=None):
        form = EventForm
        trip = get_object_or_404(Trip, id=pk)
        
        ctx = {'form': form, 
            'trip':trip,
            'title': 'Event Creation'
            }
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = EventForm(request.POST)
        trip = get_object_or_404(Trip, id=pk)

        success_url = reverse_lazy('home:trip_detail', kwargs={'pk':trip.id})


        if not form.is_valid():
            ctx = {'form':form, 'trip':trip}
            return render(request, self.template_name, ctx)

        event = form.save(commit=False)
        event.trip = trip
        event.save()
        return redirect(success_url)

class EventUpdateView(LoginRequiredMixin, View):
    model = Event
    template_name = 'home/trip_form.html'
    fields = ['name', 'location', 'cost', 'start_date' ,'end_date']

    def get(self, request, pk, pk_event):
        trip = get_object_or_404(Trip, id=pk, owner=self.request.user)
        event = get_object_or_404(Event, id=pk_event)
        form = EventForm(instance=event)
        ctx = {'form':form,
            'title': 'Event Update'
            }
        return render(request, self.template_name, ctx)
    
    def post(self, request, pk, pk_event):
        trip = get_object_or_404(Trip, id=pk, owner=self.request.user)
        event = get_object_or_404(Event, id=pk_event)
        form = EventForm(request.POST, instance=event)

        success_url = reverse_lazy('home:trip_detail', kwargs={'pk':trip.id})

        if not form.is_valid():
            ctx = {'form':form}
            return render(request, self.template_name, ctx)
        
        form = form.save()
        return redirect(success_url)

    


    



    

