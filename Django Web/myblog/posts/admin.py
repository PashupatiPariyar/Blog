from django.contrib import admin
from .models import Post

class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title','updated','timestamp']
    list_display_links = ['updated'] #puts the link
    list_filter = ['updated','timestamp']
    search_fields = ['title', 'content']
    list_editable = ['title']
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)
