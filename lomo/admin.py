from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *
# Register your models here.

# edit inline choice on VOTE
class ChoiceInline(admin.TabularInline):
	model = Choice

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):

	list_display = ('id','image_tag','header','channel_name','created_date')
	list_display_links = ('id','header','image_tag')
	inlines = [ChoiceInline,]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
	list_display = ('id','thumb_image','title','created_date')
	list_display_links = ('id', 'title','thumb_image')

class WxUserAdmin(admin.ModelAdmin):
	list_display = ('id','openid','created_date')
	list_display_links = ('id','openid')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
	list_display = ('id','belong_to_user','belong_to_choice','created_date')
	list_display_links = ('id','created_date')


admin.site.register(WxUser, WxUserAdmin)

class ArticleAdmin(SummernoteModelAdmin):
	list_display = ('id', 'image_tag','title', 'created_date')
	list_display_links = ('id', 'title','created_date','image_tag')

admin.site.register(Article, ArticleAdmin)