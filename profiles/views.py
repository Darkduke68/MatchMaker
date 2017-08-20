from django.shortcuts import render, redirect
from profiles.forms import ProfileUpdateForm


# Create your views here.
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            redirect('profile')
        else:
            return render(request, 'profiles/update.html', {'form': form})
    else:
        form = ProfileUpdateForm(instance=request.user)
        context = {
            'form': form,
            'user': request.user,
        }
        return render(request, 'profiles/update.html', context)
