from email.policy import default
import datetime
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

class UserManager(BaseUserManager):
  def create_user(self, email, password, birth, phonenumber, nickname, name):
    if not email:
      raise ValueError('must have user email')
    if not nickname:
      raise ValueError('must have user nickname')
    if not name:
      raise ValueError('must have user name')
    user = self.model(
      email = self.normalize_email(email),
      name = name,
      nickname= nickname,
      phonenumber = phonenumber,
      birth = birth,
    )

    user.set_password(password)
    user.save()
    return user

  def create_superuser(self, email, password):
    user = self.create_user(email, password, "2000-01-01", "01000000000", nickname="admin", name="admin")
    user.is_admin = True
    user.save(using=self.db)
    return user

class User(AbstractBaseUser):
  usernumber = models.AutoField(primary_key=True)
  email = models.EmailField(max_length=255, unique=True, verbose_name="이메일")
  name = models.CharField(max_length=5, verbose_name="실명")
  nickname = models.CharField(max_length=15, verbose_name="닉네임", unique=True)
  birth = models.DateField(verbose_name="생년월일")
  phonenumber = models.CharField(max_length=11, unique=True, verbose_name="휴대폰 번호")
  rate = models.FloatField("평점", default=0)
  joindate = models.DateField(auto_now_add=True, editable=False)
  lastLogin = models.DateTimeField(default=datetime.datetime.now,)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  location = models.TextField(default="", verbose_name="위치")
  postcode = models.CharField(verbose_name="우편번호", default="", max_length=5)
  sigungu = models.CharField(max_length=15, verbose_name="시군구", default="")
  like = models.TextField("찜한 아이템 번호", default="")
  numItemSharing = models.IntegerField("판매중인 아이템 수", default=0)
  numWrittenReview = models.IntegerField("작성 리뷰 수", default=0)

  objects = UserManager()

  USERNAME_FIELD = "email"
  REQUIRED_FIELD = ["email", "nickname", "name"]

  def __str__(self):
    return self.email
  
  def has_perm(self, perm, obj=None):
    return True
  
  def has_module_perms(self, app_label):
    return True
  
  @property
  def is_staff(self):
    return self.is_admin

