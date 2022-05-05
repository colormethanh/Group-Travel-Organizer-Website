from asyncio import events
from dataclasses import fields
from django import views
from django.db import IntegrityError
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Going, Trip, Event, Voted, Comment
from home.forms import TripForm, EventForm, TripJoinForm, CommentForm

from mygrouptravelsite.owner import OwnerListView, OwnerDetailView, OwnerDeleteView



# Create your views here.

""" Landing page view """
def HomePage(request):
    template_name = "home/home_page.html"
    return render (request, template_name)


""" Views for TRIPs """
class TripListView(OwnerListView):
    model = Trip
    template_name = "home/trip_list.html"

class UserTripListView( LoginRequiredMixin ,View):
    model = Trip
    template_name = "home/trip_list.html"

    def get(self, request):
        user = self.request.user
        trip_list = [ t.trip for t in Going.objects.filter(user=user)]
        ctx = {'trip_list':trip_list }
        return render(request, self.template_name, ctx)


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
        user = self.request.user
        comments = Comment.objects.filter(trip=t).order_by('-created_at')
        
        comment_form = CommentForm()

        members = Going.objects.filter(trip=t)
        ismember = t.ismember(user.id)

        conf_events_dict = dict()
        unconf_events_dict = dict()
        for ct, event in enumerate(events):
            key = 'event'+str(ct)
            if event.confirmed:
                conf_events_dict[key]= event
            else:
                unconf_events_dict[key] = event
        
        ctx = {'trip': t, 
                'unconf_events':unconf_events_dict, 
                'conf_events':conf_events_dict , 
                'members': members, 
                'ismember': ismember, 
                'comments': comments,
                'form':comment_form
                }
    
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

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        trip = get_object_or_404(Trip, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, trip=trip)
        comment.save()
        return redirect(reverse('home:trip_detail', args=[pk]))

        
    



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

class EventDetailView(LoginRequiredMixin, View):
    template_name = "home/event_detail.html"

    def get(self, request, pk, pk_event):
        e = Event.objects.get(id=pk_event)
        members = e.trip.members.all()
        user = self.request.user
        voted = e.has_voted(user.id)
        print(" the user has voted: ", voted)
        
        ctx = {'event': e, 'members': members, 'voted':voted}
        return render(request, self.template_name, ctx)


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

def Vote(request, pk, pk_event):
    event = get_object_or_404(Event, pk=pk_event)
    print(event)
    event.votes += 1
    event.save()

    voter = Voted(event=event, user=request.user)
    voter.save()
    return redirect(reverse('home:trip_detail', args=[pk]))






    


    



    

