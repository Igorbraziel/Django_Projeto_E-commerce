from django.contrib import admin
from profile_app.models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = 'id', 'user', 'age', 'birth_date', 'cpf',
    list_display_links = 'id',
    search_fields = 'id',
    list_per_page = 10
    ordering = '-id',
