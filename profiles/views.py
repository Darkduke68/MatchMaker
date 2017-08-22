from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import Http404

from profiles.forms import ProfileUpdateForm


# Create your views here.
@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            return render(request, 'profiles/update.html', {'form': form})
    else:
        form = ProfileUpdateForm(instance=request.user)
        context = {
            'form': form,
            'user': request.user,
        }
        return render(request, 'profiles/update.html', context)


@login_required
def profile_get(request):
    if request.method == 'GET':
        return redirect('profile-single', pk=request.user.id)
    return Http404


@login_required
def profile_single(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except:
        user = None
    if user and request.method == 'GET':
        context = {
            'curr_user': request.user,
            'view_user': user,
        }
        return render(request, 'profiles/main.html', context)
    return Http404


