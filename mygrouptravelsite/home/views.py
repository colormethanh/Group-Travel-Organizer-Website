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
from django.views.generic.edit import DeleteView
from django.templatetags.static import static

from .models import Going, Group, Event, Voted, Comment, Like, Photos
from home.forms import GroupForm, EventForm, GroupJoinForm, CommentForm, PhotoForm

from mygrouptravelsite.owner import OwnerListView, OwnerDetailView, OwnerDeleteView



# Create your views here.

""" Landing page view """
def HomePage(request):
    template_name = "home/home_page.html"
    return render (request, template_name)


""" Views for Groups """
class GroupListView(OwnerListView):
    model = Group
    template_name = "home/group_list.html"


class UserGroupListView( LoginRequiredMixin ,View):
    model = Group
    template_name = "home/group_list.html"

    def get(self, request):
        user = self.request.user
        group_list = [ t.group for t in Going.objects.filter(user=user)]

        ctx = {'group_list':group_list, 'usergroups':True }
        return render(request, self.template_name, ctx)


class GroupCreateView(LoginRequiredMixin, View):
    template_name = 'home/group_form.html'
    fields = ['name', 'key', 'start_date', 'end_date']
    title='Group Creation'
    form_action = reverse_lazy('home:group_create')
        
    def get(self, request, pk=None):
        form = GroupForm
        
        ctx = {
            'form': form,
            'title': self.title,
            'form_action':self.form_action
            }
        return render(request, self.template_name, ctx)
    
    def post(self, request, pk=None):
        form = GroupForm(request.POST)
        if not form.is_valid():
            errors = form.errors
            print(errors)
            ctx = {'form':form, 
                    'title':self.title,
                    'form_action':self.form_action,
                    'errors':errors,
                }
            return render(request, self.template_name, ctx)
        group = form.save(commit=False)
        group.owner = self.request.user
        group.icon = static('icons/'+str(group.icon))
        group.save()

        going = Going(group=group, user=self.request.user)
        going.save()

        pk = group.id
        success_url = reverse_lazy('home:group_detail', kwargs={'pk':pk})
        return redirect(success_url)

class GroupDetailView(OwnerDetailView):
    template_name = "home/group_detail.html"

    def get(self, request, pk):
        t = Group.objects.get(id=pk)
        events = Event.objects.filter(group=t)
        user = self.request.user
        comments = Comment.objects.filter(group=t).order_by('-created_at')
        carousel_pics = Photos.objects.filter(group=t).order_by('-created_at')

        comment_form = CommentForm()
        photo_form = PhotoForm()

        members = Going.objects.filter(group=t)
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


        
        ctx = {'group': t, 
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

class GroupDeleteView(OwnerDeleteView):
    model = Group
    success_url = reverse_lazy('home:group_list')

class GroupUpdateView(LoginRequiredMixin, View):
    template_name = 'home/group_form.html'
    fields = ['name', 'start_date', 'end_date']

    def get(self, request, pk):
        group = get_object_or_404(Group, id=pk, owner=self.request.user)
        events = Event.objects.filter(group=pk)

        form = GroupForm(instance=group)
        ctx = {'form':form,
            'group': group, 
            'events':events,
            'title': 'Group Update'
            }
        return render(request, self.template_name, ctx)
    
    def post(self, request, pk=None):
        group = get_object_or_404(Group, id=pk, owner=self.request.user)
        form = GroupForm(request.POST, instance=group)

        success_url = reverse_lazy('home:group_detail', kwargs={'pk':group.id})

        if not form.is_valid():
            ctx = {'form':form}
            return render(request, self.template_name, ctx)
        
        group = form.save(commit=False)
        group.icon = static('icons/'+str(group.icon))
        group.save()
        return redirect(success_url)

class GroupJoin(LoginRequiredMixin, View):
    template_name = 'home/group_form.html'

    def get(self, request, pk):
        group = get_object_or_404(Group, id=pk)
        ctx = {'group': group, 'form':GroupJoinForm()}
        return render (request, self.template_name, ctx)
    
    def post(self, request, pk):
        group = get_object_or_404(Group, id=pk)
        form = GroupJoinForm(request.POST)
        success_url = reverse_lazy('home:group_detail', kwargs={'pk':group.id})

        if not form.is_valid():
            ctx = {'group': group, 'form': form}
            return render(request, self.template_name, ctx)
        
        entered = form.cleaned_data['group_key']
        key = group.key
        user = self.request.user
        

        if entered == key:
            print(" Adding user to group ")
            going = Going(group=group, user=user)
            try:
                going.save()
            except IntegrityError as e:
                pass
            return redirect(success_url)
        else:
            ctx = {'group': group, 'form': form, 'error_message': 'Key error, make sure you typed the key correctly'}
            return render(request, self.template_name, ctx )

class GroupMemberView(LoginRequiredMixin, View):
    template_name = 'home/member_list.html'
    def get(self, request, pk):
        group = get_object_or_404(Group, id=pk)
        member_list = Going.objects.filter(group=group)
        ctx = {'member_list':member_list, 'group':group }
        return render(request, self.template_name, ctx)


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        group = get_object_or_404(Group, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, group=group)
        comment.save()
        return redirect(reverse('home:group_detail', args=[pk]))

class PhotoView(LoginRequiredMixin, View):

    def post(self, request, pk):
        group = get_object_or_404(Group, id=pk)
        photo_form = PhotoForm(request.POST, request.FILES)
        if photo_form.is_valid():
            print('form was valid')
            photo = photo_form.save(commit=False)
            photo.owner = self.request.user
            photo.group = group
            photo.save()
        else:
            print (photo_form.errors)
        return redirect(reverse('home:group_detail', kwargs={'pk':group.id}))

    



""" Views for EVENTs """
class EventCreateView(LoginRequiredMixin, View):
    model = Event
    template_name = 'home/group_form.html'
    
    def get(self, request, pk=None):
        form = EventForm
        group = get_object_or_404(Group, id=pk)
        form_action = reverse_lazy('home:event_create', kwargs={'pk':group.id})
        

        
        
        ctx = {'form': form, 
            'group':group,
            'title': 'Event Creation',
            'form_action': form_action,
            }
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = EventForm(request.POST)
        group = get_object_or_404(Group, id=pk)
        form_action = reverse_lazy('home:event_create', kwargs={'pk':group.id})

        success_url = reverse_lazy('home:group_detail', kwargs={'pk':group.id})


        if not form.is_valid():
            errors = form.non_field_errors
            print(errors)
            ctx = {'form':form, 
                    'group':group,
                    'title': 'Event Creation',
                    'form_action': form_action,
                    'errors': errors,
                    }
            return render(request, self.template_name, ctx)

        event = form.save(commit=False)
        event.group = group
        event.save()
        return redirect(success_url)


class EventListView( LoginRequiredMixin ,View):
    model = Event
    template_name = "home/event_list.html"

    def get(self, request, pk):
        user = self.request.user
        group = get_object_or_404(Group, id=pk)
        event_list = Event.objects.filter(group=group, confirmed=False)
        ctx = {'event_list':event_list, 'group':group}
        return render(request, self.template_name, ctx)


class EventDetailView(LoginRequiredMixin, View):
    template_name = "home/event_detail.html"

    def get(self, request, pk, pk_event):
        e = Event.objects.get(id=pk_event)
        members = e.group.members.all()
        user = self.request.user
        voted = e.has_voted(user.id)
        e.get_dates_range(e.start_date, e.end_date)
        ctx = {'event': e, 'members': members, 'voted':voted}
        return render(request, self.template_name, ctx)

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'home/group_confirm_delete.html'
    success_url = reverse_lazy('home:home_page')

class EventUpdateView(LoginRequiredMixin, View):
    model = Event
    template_name = 'home/group_form.html'
    fields = ['name', 'location', 'cost', 'start_date' ,'end_date']

    def get(self, request, pk, pk_event):
        group = get_object_or_404(Group, id=pk, owner=self.request.user)
        event = get_object_or_404(Event, id=pk_event)
        form = EventForm(instance=event)
        ctx = {'form':form,
            'title': 'Event Update'
            }
        return render(request, self.template_name, ctx)
    
    def post(self, request, pk, pk_event):
        group = get_object_or_404(Group, id=pk, owner=self.request.user)
        event = get_object_or_404(Event, id=pk_event)
        form = EventForm(request.POST, instance=event)

        success_url = reverse_lazy('home:group_detail', kwargs={'pk':group.id})

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

    confirmed = event.chk_confirmed()

    return redirect(reverse('home:group_detail', args=[pk]))

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


    


    



    

