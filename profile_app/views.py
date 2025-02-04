from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import copy

from . import forms
from . import models

class BaseProfileView(View):
    template_name = 'profile_app/create.html'
    
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        
        self.profile = None
        self.cart = self.request.session.get('cart')
        
        if self.request.user.is_authenticated:
            self.profile = models.UserProfile.objects.filter(user=self.request.user).first() 
            
            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user,
                ),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None,
                    instance=self.profile,   
                )
            }
            
        else:
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'profileform': forms.ProfileForm(data=self.request.POST or None),
            }
                    
        self.userform = self.context['userform']
        self.profileform = self.context['profileform']
        
        if self.request.user.is_authenticated:
            self.template_name = 'profile_app/update.html'
        
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
            
            if not self.profile:
                self.profileform.cleaned_data['user'] = user
                self.profile = models.UserProfile(**self.profileform.cleaned_data)
                self.profile.save()
            else:
                self.profile = self.profileform.save(commit=False)
                self.profile.user = user
                self.profile.save()
            
        else:
            user = self.userform.save(commit=False)
            user.set_password(password)
            user.save()
            
            profile = self.profileform.save(commit=False)
            profile.user = user
            profile.save()
            
        if password:
            authenticated = authenticate(
                self.request, 
                username=user,
                password=password,
            )
            
            if authenticated:
                login(self.request, user=user)
        
        self.request.session['cart'] = self.cart
        self.request.session.save()
        
        messages.success(self.request, 'Your Register has been created successfully')
        
        return redirect('profile_app:create')
    

class UpdateView(CreateView):
    ...

class LoginView(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
                    
        if not username or not password:
            messages.error(self.request, 'Username and password needs to be filled')
            return redirect('profile_app:create')
        
        user = authenticate(self.request, username=username, password=password)
        if not user:
            messages.error(self.request, 'Username or password are invalids')
            return redirect('profile_app:create')
        
        login(self.request, user=user)
        messages.success(self.request, 'You are logged in successfully')
        return redirect('product:cart')
    
        
        
        

class LogoutView(View):
    def get(self, *args, **kwargs):
        cart = copy.deepcopy(self.request.session.get('cart'))
        
        logout(self.request)
        
        self.request.session['cart'] = cart
        self.request.session.save()
        
        return redirect('product:list')
        

