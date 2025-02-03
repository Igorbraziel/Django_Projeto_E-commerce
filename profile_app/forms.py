from django import forms
from django.contrib.auth.models import User
from profile_app.models import UserProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = 'user',
        
        
class UserForm(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
    
    password = forms.CharField(
        required=False, 
        widget=forms.PasswordInput()
    )
    
    password2 = forms.CharField(
        required=False, 
        widget=forms.PasswordInput()
    )
    
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'username', 'password', 'password2', 'email'
        
    def clean(self):
        cleaned_data = super().clean()
        
        validation_error_messages = {}
        
        username_data = cleaned_data.get('username')
        email_data = cleaned_data.get('email')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        user_db = User.objects.filter(username=username_data).first()
        email_db = User.objects.filter(email=email_data).first()
        
        if self.user:
            if user_db and self.user != user_db:
                validation_error_messages['username'] = 'This username is already in use'
                
            if email_db and self.user != email_db:
                validation_error_messages['email'] = 'This email is already in use'
                    
            if password or password2:
                if password != password2:
                    validation_error_messages['password'] = 'Passwords do not match'
                    validation_error_messages['password2'] = 'Passwords do not match'
                else:
                    if password and len(password) < 6:
                        validation_error_messages['password'] = 'Password is too short'
                    if password2 and len(password2) < 6:
                        validation_error_messages['password2'] = 'Password is too short'
        else:
            if user_db:
                validation_error_messages['username'] = 'This username is already in use'
                
            if email_db:
                validation_error_messages['email'] = 'This email is already in use'
            
            if not password:
                validation_error_messages['password'] = 'This field is required'
                
            if not password2:
                validation_error_messages['password2'] = 'This field is required'
                
            if password and password2:
                if password != password2:
                    validation_error_messages['password'] = 'Passwords do not match'
                    validation_error_messages['password2'] = 'Passwords do not match'
                else:
                    if password and len(password) < 6:
                        validation_error_messages['password'] = 'Password is too short'
                    if password2 and len(password2) < 6:
                        validation_error_messages['password2'] = 'Password is too short'
                
                
        if validation_error_messages:
            raise forms.ValidationError(message=validation_error_messages)
        
        return cleaned_data