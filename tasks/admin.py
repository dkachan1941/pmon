from django.contrib import admin
from django.core.urlresolvers import reverse

from .models import Task
from .models import Competitor
# from .models import Shop
from .models import Group
from .models import Article
from .models import MobileDevice



class ArticlesInline(admin.TabularInline):
    model = Article

class TaskAdmin(admin.ModelAdmin):
    inlines = [
        ArticlesInline,
    ]
    readonly_fields=('completedate',)

class MobileDeviceInline(admin.TabularInline):
    model = Task

class MobileDeviceAdmin(admin.ModelAdmin):
    inlines = [
        MobileDeviceInline,
    ]

class ArticleAdmin(admin.ModelAdmin):
    readonly_fields=('price','photo_path',)


admin.site.register(Task,TaskAdmin)
admin.site.register(Competitor)
admin.site.register(MobileDevice, MobileDeviceAdmin)
admin.site.register(Group)
admin.site.register(Article, ArticleAdmin)