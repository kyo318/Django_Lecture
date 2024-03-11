from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    # Generic Relation에서는 1측에 관계를 정의하므로, 모델 클래스에 직접적으로 필드를 정의
    # 이 필드명으로 Comment에 대한 related_name, related_query_name 역할을 같이 수행
    comment_set = GenericRelation(to="Comment", related_query_name="post")


class Article(models.Model):
    title = models.CharField(max_length=100)
    comment_set = GenericRelation(to="Comment", related_query_name="article")


class Comment(models.Model):
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    # on_delete 옵션을 지원하지 않습니다. CASCADE 정책으로만 동작합니다.
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_id")
    message = models.TextField()
