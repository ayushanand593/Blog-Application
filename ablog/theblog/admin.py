from django.contrib import admin
from.models import Post,Category,Profile,Comment,Person
from import_export.admin import ImportExportModelAdmin
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Person)
class PersonAdmin(ImportExportModelAdmin):
    list_display = ('name', 'email', 'location')