from asyncio import events
from dataclasses import fields
from re import template
from django import views
from django.db import IntegrityError
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Going, Trip, Event, Voted, Comment, Like, Photos
from home.forms import TripForm, EventForm, TripJoinForm, CommentForm, PhotoForm

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
        ctx = {'trip_list':trip_list, 'usertrips':True }
        return render(request, self.template_name, ctx)


class TripCreateView(LoginRequiredMixin, View):
    template_name = 'home/trip_form.html'
    fields = ['name', 'key', 'start_date', 'end_date']
    title='Trip Creation'
    form_action = reverse_lazy('home:trip_create')
        
    def get(self, request, pk=None):
        form = TripForm
        
        ctx = {
            'form': form,
            'title': self.title,
            'form_action':self.form_action
            }
        return render(request, self.template_name, ctx)
    
    def post(self, request, pk=None):
        form = TripForm(request.POST)
        if not form.is_valid():
            errors = form.errors
            print(errors)
            ctx = {'form':form, 
                    'title':self.title,
                    'form_action':self.form_action,
                    'errors':errors,
                }
            return render(request, self.template_name, ctx)
        trip = form.save(commit=False)
        trip.owner = self.request.user
        trip.save()

        pk = trip.id
        success_url = reverse_lazy('home:trip_detail', kwargs={'pk':pk})
        return redirect(success_url)

class TripDetailView(OwnerDetailView):
    template_name = "home/trip_detail.html"

    def get(self, request, pk):
        t = Trip.objects.get(id=pk)
        events = Event.objects.filter(trip=t)
        user = self.request.user
        comments = Comment.objects.filter(trip=t).order_by('-created_at')
        carousel_pics = Photos.objects.filter(trip=t).order_by('-created_at')
        
        comment_form = CommentForm()
        photo_form = PhotoForm()

        members = Going.objects.filter(trip=t)
        ismember = t.ismember(user.id)

        liked_comments=list()

        conf_events_dict = dict()
        unconf_events_dict = dict()
        for ct, event in enumerate(events):
            key = 'event'+str(ct)
            if event.confirmed:
                conf_events_dict[key]= event
            else:
                unconf_events_dict[key] = event
        
        if user.is_authenticated:
            rows = request.user.comment_liked.values('id')
            liked_comments = [row['id'] for row in rows]

        
        ctx = {'trip': t, 
                'unconf_events':unconf_events_dict, 
                'conf_events':conf_events_dict , 
                'members': members, 
                'ismember': ismember, 
                'comments': comments,
                'form':comment_form,
                'photo_form': photo_form,
                'liked_comments': liked_comments,
                'carousel_pics':carousel_pics,
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

class TripMemberView(LoginRequiredMixin, View):
    template_name = 'home/member_list.html'
    def get(self, request, pk):
        user = self.request.user
        trip = get_object_or_404(Trip, id=pk)
        member_list = Going.objects.filter(trip=trip)
        ctx = {'member_list':member_list, 'trip':trip }
        return render(request, self.template_name, ctx)


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        trip = get_object_or_404(Trip, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, trip=trip)
        comment.save()
        return redirect(reverse('home:trip_detail', args=[pk]))

class PhotoView(LoginRequiredMixin, View):

    def post(self, request, pk):
        trip = get_object_or_404(Trip, id=pk)
        photo_form = PhotoForm(request.POST, request.FILES)
        if photo_form.is_valid():
            print('form was valid')
            photo = photo_form.save(commit=False)
            photo.owner = self.request.user
            photo.trip = trip
            photo.save()
        else:
            print (photo_form.errors)
        return redirect(reverse('home:trip_detail', kwargs={'pk':trip.id}))

    



""" Views for EVENTs """
class EventCreateView(LoginRequiredMixin, View):
    model = Event
    template_name = 'home/trip_form.html'
    
    def get(self, request, pk=None):
        form = EventForm
        trip = get_object_or_404(Trip, id=pk)
        form_action = reverse_lazy('home:event_create', kwargs={'pk':trip.id})
        

        
        
        ctx = {'form': form, 
            'trip':trip,
            'title': 'Event Creation',
            'form_action': form_action,
            }
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = EventForm(request.POST)
        trip = get_object_or_404(Trip, id=pk)
        form_action = reverse_lazy('home:event_create', kwargs={'pk':trip.id})

        success_url = reverse_lazy('home:trip_detail', kwargs={'pk':trip.id})


        if not form.is_valid():
            ctx = {'form':form, 
                    'trip':trip,
                    'title': 'Event Creation',
                    'form_action': form_action,
                    }
            return render(request, self.template_name, ctx)

        event = form.save(commit=False)
        event.trip = trip
        event.save()
        return redirect(success_url)


class EventListView( LoginRequiredMixin ,View):
    model = Event
    template_name = "home/event_list.html"

    def get(self, request, pk):
        user = self.request.user
        trip = get_object_or_404(Trip, id=pk)
        event_list = Event.objects.filter(trip=trip, confirmed=False)
        ctx = {'event_list':event_list, 'trip':trip}
        return render(request, self.template_name, ctx)


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

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddLikeView(LoginRequiredMixin, View):
    def post(self, request, pk_comment) :
        c = get_object_or_404(Comment, id=pk_comment)
        like = Like(user=request.user, comment=c)
        try:
            like.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteLikeView(LoginRequiredMixin, View):
    def post(self, request, pk_comment) :
        c = get_object_or_404(Comment, id=pk_comment)
        try:
            like = Like.objects.get(user=request.user, comment=c).delete()
        except Like.DoesNotExist as e:
            pass
        return HttpResponse()


    


    



    

