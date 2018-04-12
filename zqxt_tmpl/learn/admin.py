from django.contrib import admin
from learn.models import Textblog
from learn.models import User,Advise,list_info
# Register your models here.
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['message','times','username']

admin.site.register(Textblog,BlogPostAdmin)


class Useradmin(admin.ModelAdmin):
    list_display = ['username','password','email','permission']
    search_fields = ('username',)

admin.site.register(User,Useradmin)


class Adviseadmin(admin.ModelAdmin):
    list_display = ['xname','xemail','Message']
admin.site.register(Advise,Adviseadmin)

class list_infoadmin(admin.ModelAdmin):

    fieldsets = (['Main',{
        'fields':('username','name','Tel',)
    }],
    ['Advance',{'fields':('Area','age','DATEBIRTH','user_sex'),}],
    ['extra', {    'fields':('per_mess','img',),}])
    list_filter = ('user_sex','username')

admin.site.register(list_info,list_infoadmin)