from django.db import models
import datetime

class ItemManager(models.Manager):
  def create_item(self, title, category, content, cntImg, images, location, sigungu, postcode, price, pricePerHour, writer, writerName, startDate, endDate):
    if not title:
      raise ValueError('must have title')
    if not category:
      raise ValueError('must have category')
    if not location:
      raise ValueError('must have location')
    item = self.model(
      title = title,
      category = category,
      content = content,
      location = location,
      sigungu = sigungu,
      postcode = postcode,
      cntImg = cntImg,
      image1 = images[0],
      image2 = images[1],
      image3 = images[2],
      image4 = images[3],
      image5 = images[4],
      image6 = images[5],
      image7 = images[6],
      image8 = images[7],
      price = price,
      pricePerHour = pricePerHour,
      writer = writer,
      writerName = writerName,
      startDate = startDate,
      endDate = endDate
    )

    item.save()
    return item

class Item(models.Model):
  itemnumber = models.AutoField(primary_key=True)
  title = models.CharField(max_length=25, verbose_name="제목")
  category = models.IntegerField(verbose_name="카테고리")
  content = models.TextField(verbose_name="상품설명")
  cntImg = models.IntegerField(verbose_name="이미지 수")
  image1 = models.TextField(verbose_name="이미지1")
  image2 = models.TextField(verbose_name="이미지2")
  image3 = models.TextField(verbose_name="이미지3")
  image4 = models.TextField(verbose_name="이미지4")
  image5 = models.TextField(verbose_name="이미지5")
  image6 = models.TextField(verbose_name="이미지6")
  image7 = models.TextField(verbose_name="이미지7")
  image8 = models.TextField(verbose_name="이미지8")
  location = models.CharField(max_length=255, verbose_name="위치", default="")
  postcode = models.CharField(max_length=5, verbose_name="우편번호", default="")
  sigungu = models.CharField(max_length=15, verbose_name="시군구")
  price = models.IntegerField(verbose_name="가격", default=0)
  pricePerHour = models.BooleanField(verbose_name="시간당 가격", default=True)
  writer = models.IntegerField("작성자", default=0)
  reviews = models.IntegerField("평가 수", default=0)
  rate = models.FloatField("평점", default=0)
  like = models.IntegerField("찜한 사람 수", default=0)
  uploaded = models.DateTimeField("올린 시간", default=datetime.datetime.now)
  likedUser = models.TextField("찜한 유저들", default="")
  writerName = models.CharField("작성자 닉네임", default='', max_length=15)
  startDate = models.DateField("시간시간", default=datetime.datetime.now)
  endDate = models.DateField("종료시간", default=datetime.datetime.now)

  objects = ItemManager()

  REQUIRED_FIELD = ["title", "category", 'location']

  def __str__(self):
    return self.title
  
  def has_perm(self, perm, obj=None):
    return True
  
  def has_module_perms(self, app_label):
    return True
  