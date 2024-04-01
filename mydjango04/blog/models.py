from django.db import models
from django.db.models import UniqueConstraint
from django.conf import settings
from django.utils.text import slugify
from uuid import uuid4
from core.model_fields import IPv4AddressIntegerField, BooleanYNField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q
from django.db.models.functions import Lower
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse

# class PublishedPostManager(models.Manager):
#     def get_queryset(self) -> models.QuerySet:
#         qs = super().get_queryset()
#         qs = qs.filter(status=Post.Status.PUBLISHED)
#         return qs

#     def create(self, **kwargs):
#         kwargs.setdefault("status", Post.Status.PUBLISHED)
#         return super().create(**kwargs)


class TimestampedModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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
class Post(TimestampedModel):

    class Status(models.TextChoices):
        DRAFT = "D", "초안"
        PUBLISHED = "P", "발행"

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_post_set",
        related_query_name="blog_post",
    )
    title = models.CharField(max_length=100)
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    content = models.TextField()
    slug = models.SlugField(
        max_length=120, allow_unicode=True, help_text="title로부터 자동 생성"
    )
    # published = PublishedPostManager()
    # objects = models.Manager()
    tag_set = models.ManyToManyField(
        "Tag",
        related_name="blog_post_set",
        related_query_name="blog_post",
        blank=True,
        through="PostTagRelation",
        through_fields=("post", "tag"),
    )

    objects = PostQuerySet.as_manager()

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def slugify(self, force=False):
        if force or not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
            self.slug = self.slug[:112]
            self.slug += "-" + uuid4().hex[:8]

    # def save(self, *args, **kwargs):
    #     self.slugify()
    #     super().save(*args, **kwargs)

    class Meta:
        constraints = [UniqueConstraint(fields=["slug"], name="unique_slug")]
        verbose_name = "포스팅"
        verbose_name_plural = "포스팅 목록"
        permissions = [
            ("view_premium_post", "프리미엄 포스팅을 볼 수 있음"),
        ]


class AccessLog(TimestampedModel):
    ip_generic = models.GenericIPAddressField(protocol="IPv4")
    ip_int = IPv4AddressIntegerField()


@receiver(pre_save, sender=Post)
def pre_save_on_save(sender, instance: Post, **kwargs):
    print("pre_save_on_save 메서드가 호출 되었습니다.")
    instance.slugify()


class Article(TimestampedModel):
    title = models.CharField(max_length=100)
    is_public_ch = models.CharField(
        max_length=1,
        choices=[("Y", "Yes"), ("N", "No")],
        default="N",
    )

    is_public_yn = BooleanYNField(default=False)


class Tag(TimestampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("name"), name="blog_tag_name_uniq"),
        ]
        indexes = [
            models.Index(
                fields=["name"],
                name="blog_tag_name_like",
                opclasses=["varchar_pattern_ops"],
            )
        ]
        ordering = ["-pk"]


class PostTagRelation(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # 관계 모델을 통해, 관계에 대한 추가 정보를 담을 수 있습니다.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["post", "tag"],
                name="blog_post_tag_relation_unique",
            )
        ]


class Comment(TimestampedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()


class Student(models.Model):
    name = models.CharField(max_length=100)


class Course(models.Model):
    title = models.CharField(max_length=100)


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=10)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                "student",
                "course",
                Lower("semester"),  # 다수의 expression 지정
                # fields=["student", "course", "semester"],  # 단순 필드명 나열
                name="blog_enrollment_uniq",
            ),
        ]


class Review(TimestampedModel):
    message = models.TextField()
    rating = models.SmallIntegerField(
        # validators=[
        #     MinValueValidator(1),
        #     MaxValueValidator(5),
        # ],
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(rating__gte=1, rating__lte=5),
                name="blog_review_rating_gte_1_lte_5",
            ),
        ]
        db_table_comment = "사용자 리뷰와 평점을 저장하는 테이블"

    def get_absolute_url(self):
        return reverse("blog:review_detail", args=[self.pk])


class MemoGroup(models.Model):
    name = models.CharField(max_length=100)


class Memo(models.Model):
    class Status(models.TextChoices):
        PRIVATE = "V", "비공개"
        PUBLIC = "P", "공개"

    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(MemoGroup, on_delete=models.CASCADE)
    message = models.CharField(max_length=140)
    status = models.CharField(
        max_length=1, default=Status.PUBLIC, choices=Status.choices
    )
    created_at = models.DateTimeField(auto_now_add=True)
