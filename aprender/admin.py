from django.contrib import admin
from .models import User, Word, Set, Folder
# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, AuthorAdmin)
admin.site.register(Word, AuthorAdmin)
admin.site.register(Set, AuthorAdmin)
admin.site.register(Folder, AuthorAdmin)