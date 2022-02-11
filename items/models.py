from django.db import models

class ItemManager(models.Manager):
  def create_item(self, title, category, content, cntImg, images, location, postcode, price, pricePerHour):
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
      pricePerHour = pricePerHour
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
  price = models.IntegerField(verbose_name="가격", default=0)
  pricePerHour = models.BooleanField(verbose_name="시간당 가격", default=True)

  objects = ItemManager()

  REQUIRED_FIELD = ["title", "category", 'location']

  def __str__(self):
    return self.title
  
  def has_perm(self, perm, obj=None):
    return True
  
  def has_module_perms(self, app_label):
    return True
  