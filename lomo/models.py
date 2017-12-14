from django.db import models
from django.conf import settings
from django.db.models.fields.files import ImageFieldFile

import uuid
import os
from PIL import Image

from django.utils.translation import ugettext_lazy as _

# Create your models here.

def image_file_path(self, filename):
	ext = filename.split('.')[-1]
	return 'choice_image/{}.{}'.format(uuid.uuid4(),ext)

# wxuser
class WxUser(models.Model):
	openid = models.CharField('openid', max_length=200, blank=True, null=True)
	created_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.openid

	class Meta:
		ordering = ['-created_date']

# vote
class Vote(models.Model):
	channel_name = models.CharField('频道名', max_length=100, blank=True, null=True)
	header = models.CharField('标题', max_length=200, blank=True, null=True)
	subheader = models.CharField('副标题', max_length=200, blank=True, null=True)
	editor_say = models.CharField('小编说',max_length=200, blank=True)
	header_image = models.ImageField('头图', upload_to=image_file_path, blank=True, null=True)
	sub_image = models.ImageField('副图', upload_to=image_file_path, blank=True, null=True)
	thumb_img = models.ImageField('缩略图', upload_to='thumb_img', blank=True, null=True)
	created_date = models.DateTimeField('创建时间',auto_now_add=True)

	CHOICES = (
			(1, '是'),
			(0, '否')
		)
	single_choice = models.IntegerField('可否多选',choices=CHOICES,blank=True,default=0)


	def __str__(self):
		return self.header

	# admin image preview
	def image_tag(self):
		return '<img src="%s" style="width:120px;height:80px"/>'%(self.header_image.url)
	image_tag.short_description = '预览图'
	image_tag.allow_tags = True

	# 生成缩略图
	def save(self, *args, **kargs):
		super(Vote, self).save(*args, **kargs)
		# 首先要判断是不是已经有缩略图了
		if self.thumb_img == None:

			# 处理图片
			image = Image.open(self.header_image)
			image.thumbnail((100,100), Image.ANTIALIAS)
			# 生成保存路径
			MEDIA_ROOT = settings.MEDIA_ROOT
			ext = self.header_image.name.split('.')[-1]
			name = uuid.uuid4()
			related_name = 'thumb_img/{}.{}'.format(name,ext)
			image_path = os.path.join(MEDIA_ROOT,'thumb_img/{}.{}'.format(name, ext))
			# 保存图片
			image.save(image_path)
			# 保存图片后，关联对应的字段
			self.thumb_img = ImageFieldFile(self, self.thumb_img, related_name)
			super(Vote, self).save(*args, **kargs)

	class Meta:
		ordering = ['-created_date']


#def image_file_path(self, filename):
#	ext = filename.split('.')[-1]
#	return 'choice_image/{}.{}'.format(uuid.uuid4(),ext)

# choice
class Choice(models.Model):
	header_image = models.ImageField('图片', upload_to=image_file_path, blank=True, null=True)
	title = models.CharField('标题', max_length=200, blank=True, null=True)
	created_date = models.DateTimeField('创建时间', auto_now_add=True)
	belong_to_vote = models.ForeignKey(Vote, related_name='choices', verbose_name='属于')

	def thumb_image(self):
		return '<img src="%s" style="width:50px;height:50px"/>'%(self.header_image.url)
	thumb_image.short_description = '预览图'
	thumb_image.allow_tags = True

	class Meta:
		ordering = ['-created_date']

	def __str__(self):
		return self.title


# ticket
class Ticket(models.Model):
	belong_to_choice = models.ForeignKey(Choice, related_name='tickets',verbose_name='选项')
	belong_to_user = models.ForeignKey(WxUser, related_name='tickets', verbose_name='用户')
	created_date = models.DateTimeField('创建时间', auto_now_add=True)

	class Meta:
		ordering = ['-created_date']

	def __str__(self):
		return '%s投给了%s'%(self.belong_to_user, self.belong_to_choice)


# post
def article_image_path(self, filename):
	ext = filename.split('.')[-1]
	return 'article_img/{}.{}'.format(uuid.uuid4(),ext)

class Article(models.Model):
	title = models.CharField('文章标题',max_length=200,blank=True)
	content = models.TextField('文章内容',blank=True)
	header_image = models.ImageField('全屏图', upload_to=article_image_path, blank=True)
	sub_image = models.ImageField('简介图',upload_to=article_image_path,blank=True)
	created_date = models.DateTimeField('创建时间', auto_now_add=True)

	belong_to_vote = models.OneToOneField(Vote, related_name='article', verbose_name='属于')

	def image_tag(self):
		return '<img src="%s"/ style="width:120px;height:80px">'%(self.sub_image.url)
	image_tag.short_description = '预览图'
	image_tag.allow_tags = True

	class Meta:
		ordering = ['-created_date']

	def __str__(self):
		return self.title


