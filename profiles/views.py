from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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
        return render(request, 'profiles/main.html', {'user': request.user})
    return redirect('home')
