from django.contrib import admin
from .models import UpdateInfo, UpdateVersion

class UpdateInfoAdmin(admin.ModelAdmin):
  list_display = ('update_version','update_info','created','modified')
  list_filter = ['update_version']
  ordering = ['created']


class UpdateVersionAdmin(admin.ModelAdmin):
  list_display = ('version','created','modified')
  list_filter = ['version']
  ordering = ['created']
  
  
admin.site.register(UpdateInfo,UpdateInfoAdmin)
admin.site.register(UpdateVersion,UpdateVersionAdmin)
