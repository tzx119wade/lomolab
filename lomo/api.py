from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from .models import WxUser, Vote, Choice, Ticket, Article
from .serializers import VoteSerializer, ChoiceSerializer, ArticleSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

import requests
import uuid

from .common import generate_choice
import random

@api_view(['GET'])
def wxlogin(request,code,old_session=None):

	url = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'.format(settings.WXAPPID, settings.WXAPPSECRET, code)

	if old_session :
		# 登录态过期的情况下删除旧的session_key
		cache.delete_pattern(old_session)

	res = requests.get(url)
	data = res.json()
	openid = data['openid']
	session_key = data['session_key']
	value = session_key + '&' + openid
	
	# 判断数据库里是否有当前的openid
	try:
		user = WxUser.objects.get(openid=openid)
	except ObjectDoesNotExist:
		wxuser = WxUser(openid=openid)
		wxuser.save()

	# 写入缓存
	key = uuid.uuid1()
	cache.set(key, value, timeout=None)

	# 将第三方的session_key返回
	body = {
		'session_key':key
	} 
	return Response(body, status=status.HTTP_200_OK)


@api_view(['GET'])
def vote_top3(request):
	query = Vote.objects.all()[0:3]
	serializers = VoteSerializer(query, context={'request':request}, many=True)

	return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def vote(request, page_num):
	queryset = Vote.objects.all()
	page_robot = Paginator(queryset, 4)

	try:
		page_data = page_robot.page(page_num)
	except EmptyPage:
		body = {
			'msg':'EmptyPage,page_num is fail'
		}
		return Response(body, status=status.HTTP_400_BAD_REQUEST)
	except PageNotAnInteger:
		page_data = page_robot.page(1)

	# 判断是否有下一页 并返回给前台
	has_next = 1
	if page_data.has_next():
		has_next = 1
	else:
		has_next = 0

	serializers = VoteSerializer(page_data,context={'request':request}, many=True)

	body = {
		'has_next': has_next,
		'data': serializers.data
	}

	return Response(body, status=status.HTTP_200_OK)

@api_view(['POST'])
def get_vote_detail(request):
	# 验证session_key是否有效
	session_key = request.data['session_key']
	if not cache.has_key(session_key):
		return Response({'msg':'session key is fail'}, status=status.HTTP_400_BAD_REQUEST)

	value = cache.get(session_key)
	openid = value.split('&')[1]
	user = WxUser.objects.get(openid=openid)

	vote_id = request.data['id']
	query_vote = Vote.objects.get(id=vote_id)
	query_choices = Choice.objects.filter(belong_to_vote=query_vote)
	is_vote = None

	for item in query_choices:
		query_tickets = Ticket.objects.filter(belong_to_choice=item, belong_to_user=user)
		if query_tickets.count() > 0:
			is_vote = 1
			break
		else:
			continue

	vote_serializer = VoteSerializer(query_vote, context={'request':request}, many=False)
	choice_serializer = ChoiceSerializer(query_choices, context={'request':request}, many=True)

	body = {
		'vote':vote_serializer.data,
		'choices':choice_serializer.data,
		'is_vote':is_vote
	}
	return Response(body, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_ticket(request):
	# 传递的参数：
	# session_key,single_choice,choice_id

	value = cache.has_key(request.data['session_key'])
	if value == False:
		body = {
			'error':'session_key is wrong'
		}
		return Response(body, status=status.HTTP_400_BAD_REQUEST)

	# 查询user
	value = cache.get(request.data['session_key'])
	openid = value.split('&')[1]
	user = WxUser.objects.get(openid=openid)

	single_choice = int(request.data['single_choice'])
	# 多选
	if single_choice == 1:
		id_list = request.data['choice_id'].split('&')
		for item_id in id_list:
			item_id = int(item_id)
			choice = Choice.objects.get(id=item_id)
			ticket = Ticket(belong_to_choice=choice, belong_to_user=user)
			ticket.save()
	else:
		item_id = request.data['choice_id']
		choice = Choice.objects.get(id=item_id)
		ticket = Ticket(belong_to_choice=choice, belong_to_user=user)
		ticket.save()

	return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_article(request,id):
	query_data = Article.objects.get(id=id)
	# 阅读数redis
	key = 'read_count' + '&' + str(query_data.id)
	if cache.has_key(key):
		value = cache.get(key)
		value += 1
		cache.set(key,value,timeout=None)
	else:
		cache.set(key,1,timeout=None)
		value = 1
	
	serializers = ArticleSerializer(query_data, context={'request':request}, many=False)

	data = {
		'article': serializers.data,
		'read_count': value
	}
	return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_vote_result(request):
	vote_id = request.data['vote_id']
	session_key = request.data['session_key']

	value = cache.get(session_key)
	openid = value.split('&')[1]
	user = WxUser.objects.get(openid=openid)

	query_vote = Vote.objects.get(id=vote_id)
	editor_say = query_vote.editor_say

	choices = []
	selected_list = []
	choice_count = query_vote.choices.count()
	num_list = generate_choice(choice_count)

	for choice in query_vote.choices.all():
		count = Ticket.objects.filter(belong_to_choice=choice, belong_to_user=user).count()
		data = {}
		if count > 0:
			data = {
				'id': choice.id,
				'title': choice.title,
				'selected': 1
			}
		else:
			data = {
				'id': choice.id,
				'title': choice.title,
				'selected': 0
			}

		number = random.choice(num_list)
		while number in selected_list:
			number = random.choice(num_list)

		data['num'] = number
		selected_list.append(number)
		choices.append(data)

	query_article = Article.objects.get(belong_to_vote=query_vote)

	data = {
		'editor_say':editor_say,
		'choices':choices,
		'article':{
			'id': query_article.id,
			'sub_image': request.build_absolute_uri(query_article.sub_image.url),
			'title': query_article.title
		}
	}

	return Response(data, status=status.HTTP_200_OK)



