from dataclasses import fields
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Trip

from mygrouptravelsite.owner import OwnerListView, OwnerDetailView, OwnerDeleteView
from home.forms import TripForm


# Create your views here.

def HomePage(request):
    template_name = "home/home_page.html"
    return render (request, template_name)


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
        ctx = {'form': form}
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

class TripDetailView(OwnerDetailView, View):
    model = Trip
    template_name = "home/trip_detail.html"

    def get(self, request, pk):
        trip = Trip.objects.get(id=pk)
        ctx = {'trip': trip}
        return render(request, self.template_name, ctx)

class TripDeleteView(OwnerDeleteView):
    model = Trip
    success_url = reverse_lazy('home:trip_list')





    



    

