from rest_framework import serializers
from .models import Vote, Choice, Ticket, Article

import re
from bs4 import BeautifulSoup


def build_absolute_uri(instance, obj):
	request = instance.context.get('request')
	image_url = obj.header_image.url
	return request.build_absolute_uri(image_url)

class VoteSerializer(serializers.ModelSerializer):
	header_image = serializers.SerializerMethodField()

	class Meta:
		model = Vote
		fields = '__all__'

	def get_header_image(self, obj):
		return build_absolute_uri(self, obj)


class ChoiceSerializer(serializers.ModelSerializer):
	# serializers.SerializerMethodField()用来声明某个字段的值是通过调用一个特定方法来生成的
	# 这个方法的命名规范为[get_fieldname]
	header_image = serializers.SerializerMethodField()

	def get_header_image(self, obj):
		return build_absolute_uri(self, obj)

	class Meta:
		model = Choice
		fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ticket
		fields = '__all__'


# article serializer

class ArticleSerializer(serializers.ModelSerializer):

	content = serializers.SerializerMethodField()
	sub_image = serializers.SerializerMethodField()
	def get_content(self, obj):
		request = self.context['request']
		HTTP_HOST = request.scheme + '://'+ request.META['HTTP_HOST']

		soup = BeautifulSoup(obj.content.encode('utf-8'), 'lxml')
		tag_list = soup.find_all('p')
		nodes = []
		for tag in tag_list:
			node = {}
			if tag.string:
				node = {
					'type': 'view',
					'text': tag.string
				}
				nodes.append(node)
				continue
			elif tag.find('img'):
				node = {
					'type': 'image',
					'src':HTTP_HOST + tag.find('img')['src']
				}
				nodes.append(node)
				continue

		return nodes

	def get_sub_image(self, obj):
		request = self.context['request']
		return request.build_absolute_uri(obj.sub_image.url)

	class Meta:
		model = Article
		fields = '__all__'






