from django.urls import path, include
from profile_app import views

app_name = 'profile_app'

urlpatterns = [
    path('', include(views.CreateView.as_view()), name='create'),
    path('update/', include(views.UpdateView.as_view()), name='update'),
    path('login/', include(views.LoginView.as_view()), name='login'),
    path('logout/', include(views.LogoutView.as_view()), name='logout'),
]