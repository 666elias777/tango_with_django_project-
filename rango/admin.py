from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile

# Register your models here.
class PageInline(admin.TabularInline):
    model = Page
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class PageAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'url')
    list_filter = ('category',)
    search_fields = ('title', 'url')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)

admin.site.site_header = "Rango Admin Panel"
admin.site.site_title = "Rango Admin"
admin.site.index_title = "Welcome to the Rango Admin Panel"
