# from django.contrib import admin
# from django.utils.safestring import mark_safe
# from .models import User

# class UserAdmin(admin.ModelAdmin):
#     list_display = ['username', 'email', 'first_name', 'last_name', 'get_profile_picture']
#     fields = ['username', 'email', 'first_name', 'last_name', 'profile_picture']  # Ajoutez le champ profile_picture ici

#     def get_profile_picture(self, obj):
#         if obj.profile_picture:
#             return mark_safe(f'<img src="{obj.profile_picture.url}" width="50" height="50"/>')
#         else:
#             return 'No image'

#     get_profile_picture.short_description = 'Profile Picture'

# admin.site.register(User, UserAdmin)
