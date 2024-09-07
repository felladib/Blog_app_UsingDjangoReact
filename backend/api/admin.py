# from django.contrib import admin
# from django.utils.safestring import mark_safe
# from .models import User

from django.contrib import admin
from api import models as api_models

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":["title"]}

admin.site.register(api_models.User)
admin.site.register(api_models.Profile)

admin.site.register(api_models.Category)
admin.site.register(api_models.Post , PostAdmin)
admin.site.register(api_models.Comment)
admin.site.register(api_models.Notification)
admin.site.register(api_models.Bookmark)

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
