from django.conf.urls import url, include
from .api import *


from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
	url(r'^summernote/', include('django_summernote.urls')),

	# 登录态接口
	url(r'^api/wxlogin/(?P<code>\w+)$', wxlogin),
	url(r'^api/wxlogin/(?P<code>\w+)/(?P<old_session>\S+)$', wxlogin),

	# top3
	url(r'^api/vote/top3',vote_top3),
	# 获取全部votes
	url(r'^api/votes/(?P<page_num>\d+)', vote),
	# 获取某个ID vote
	url(r'^api/vote$', get_vote_detail),
	# 投票
	url(r'^api/createticket',create_ticket),
	# 投票结果
	url(r'^api/get_vote_result', get_vote_result),
	# 获取文章详情
	url(r'^api/article/(?P<id>\d+)',get_article),


]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)