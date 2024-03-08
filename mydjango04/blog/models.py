from django.db import models
from django.db.models import UniqueConstraint
from django.conf import settings
from django.utils.text import slugify
from uuid import uuid4

# class PublishedPostManager(models.Manager):
#     def get_queryset(self) -> models.QuerySet:
#         qs = super().get_queryset()
#         qs = qs.filter(status=Post.Status.PUBLISHED)
#         return qs

#     def create(self, **kwargs):
#         kwargs.setdefault("status", Post.Status.PUBLISHED)
#         return super().create(**kwargs)


class PostQuerySet(models.QuerySet):

    def published(self):
        return self.filter(status=Post.Status.PUBLISHED)

    def draft(self):
        return self.filter(status=Post.Status.DRAFT)

    def search(self, query: str):
        return self.filter(title__contains=query)

    def by_author(self, author):
        return self.filter(author=author)

    def create(self, **kwargs):
        kwargs.setdefault("status", Post.Status.PUBLISHED)
        return super().create(**kwargs)


class Category(models.Model):
    name = models.CharField(max_length=50)


# Create your models here.
class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = "D", "초안"
        PUBLISHED = "P", "발행"

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    content = models.TextField()

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(
        max_length=120, allow_unicode=True, help_text="title로부터 자동 생성"
    )
    # published = PublishedPostManager()
    # objects = models.Manager()
    objects = PostQuerySet.as_manager()

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def slugify(self, force=False):
        if force or not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
            self.slug = self.slug[:112]
            self.slug += "-" + uuid4().hex[:8]

    def save(self, *args, **kwargs):
        self.slugify()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [UniqueConstraint(fields=["slug"], name="unique_slug")]
