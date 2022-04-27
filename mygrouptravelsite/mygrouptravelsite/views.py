from django.http import HttpResponseRedirect
from django.shortcuts import render
from mygrouptravelsite.forms import CreateUserForm

def RegistrationPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/register/confirm")

    context = {'form': form}
    return render(request, 'registration/register.html', context)

def RegistrationConfirm(request):
    return render (request, 'registration/register_confirm.html', {})