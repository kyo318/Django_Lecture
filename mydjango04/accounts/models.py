from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.validators import RegexValidator


class User(AbstractUser):
    # 친구 관계 (대칭 관계)
    friend_set = models.ManyToManyField(
        to="self",
        blank=True,
        # to="self"에서 디폴트 True
        symmetrical=True,
        # related_name="friend_set",
        related_query_name="friend_user",
    )

    # 팔로잉 관계 (비대칭 관계)
    follower_set = models.ManyToManyField(
        to="self",
        blank=True,
        # to="self"에서 디폴트 True
        symmetrical=False,
        # symmetrical=False 에서는 related_name을 지원
        related_name="following_set",
        related_query_name="following",
    )


class SuperUserManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_superuser=True)


class SuperUser(User):
    objects = SuperUserManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.is_superuser = True
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="profile",
        related_query_name="profile",
    )
    address = models.CharField(max_length=100, blank=True)
    point = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(
        max_length=13,
        blank=True,
        validators=[RegexValidator(r"^01\d[ -]?\d{4}[ -]?\d{4}$")],
    )
    photo = models.ImageField(upload_to="profile/photo", blank=True)
    birth_date = models.DateField(blank=True, null=True)
    location_point = models.CharField(max_length=50, blank=True)


@receiver(post_delete, sender=Profile)
def post_delete_on_profile(instance: Profile, **kwargs):
    print("post_delete_on_profile 메서드 호출 :", instance)
    instance.photo.delete(save=False)
