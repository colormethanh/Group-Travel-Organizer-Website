from dataclasses import fields
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Trip

from mygrouptravelsite.owner import OwnerListView
from home.forms import TripForm


# Create your views here.

def HomePage(request):
    html = "<html><body>Welcome to my front page!</body></html>"
    return HttpResponse(html)


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


    



    

