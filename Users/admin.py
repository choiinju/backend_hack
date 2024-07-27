from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
UserAdmin.fieldsets+=(("Custom fields", {"fields":("first_ex","card_number","point")}),)



