from django.contrib import admin
from .models import Item,Post,Purchase,UserExtension


admin.site.register(Item)
admin.site.register(Post)
admin.site.register(Purchase)
admin.site.register(UserExtension)