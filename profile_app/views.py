from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.models import User

from . import forms
from . import models

class BaseProfileView(View):
    template_name = 'profile_app/create.html'
    
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        
        self.profile = None
        
        if self.request.user.is_authenticated:
            self.profile = models.UserProfile.objects.filter(user=self.request.user).first() 
            
            userform = forms.UserForm(
                data=self.request.POST or None,
                user=self.request.user,
                instance=self.request.user,
            )
            
            profileform = forms.ProfileForm(
                data=self.request.POST or None,
                instance=self.profile,   
            )
        else:
            userform = forms.UserForm(data=self.request.POST or None),
            profileform = forms.ProfileForm(data=self.request.POST or None),
            
        self.context = {
            'userform': userform,
            'profileform': profileform,
        }
        
        self.userform = self.context['userform']
        self.profileform = self.context['profileform']
        
        self.render = render(self.request, self.template_name, self.context)
    
    def get(self, *args, **kwargs):
        return self.render
    
    
class CreateView(BaseProfileView):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.profileform.is_valid():
            messages.error(self.request, 'Errors exists in your register form, verify if all the fields were filled')
            return self.render
        
        first_name = self.userform.cleaned_data['first_name']
        last_name = self.userform.cleaned_data['last_name']
        username = self.userform.cleaned_data['username']
        password = self.userform.cleaned_data['password']
        email = self.userform.cleaned_data['email']
        
        if self.request.user.is_authenticated:
            user = get_object_or_404(User, username=self.request.user.username)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            if password:
                user.set_password(password)
            user.email = email
            user.save()
            
        else:
            user = self.userform.save(commit=False)
            user.set_password(password)
            user.save()
            
            profile = self.profileform.save(commit=False)
            profile.user = user
            profile.save()
        
        return self.render

class UpdateView(View):
    pass

class LoginView(View):
    pass

class LogoutView(View):
    pass

