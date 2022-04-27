from asyncio import events
from dataclasses import fields
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Trip, Event

from mygrouptravelsite.owner import OwnerListView, OwnerDetailView, OwnerDeleteView
from home.forms import TripForm, EventForm


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
    model = Trip
    template_name = 'home/trip_form.html'
    fields = ['name', 'start_date', 'end_date']
    success_url = reverse_lazy('home:trip_list')

    def get(self, request, pk=None):
        form = TripForm
        ctx = {'form': form,}
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
    model = Trip
    template_name = "home/trip_detail.html"

    def get(self, request, pk):
        t = Trip.objects.get(id=pk)
        events = Event.objects.filter(trip = t)
        ctx = {'trip': t, 'events':events}
        return render(request, self.template_name, ctx)

class TripDeleteView(OwnerDeleteView):
    model = Trip
    success_url = reverse_lazy('home:trip_list')


""" Views for EVENTs """
class EventCreateView(LoginRequiredMixin, View):
    model = Event
    template_name = 'home/event_form.html'


    def get(self, request, pk=None):
        form = EventForm
        trip = get_object_or_404(Trip, id=pk)
        
        ctx = {'form': form, 'trip':trip}
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

    


    



    

