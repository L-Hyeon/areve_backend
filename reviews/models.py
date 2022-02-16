from django.db import models

class ReviewManager(models.Manager):
  def create_review(self, score, content, cntImg, images, numItem, numWriter):
    if not score:
      raise ValueError('must have score')
    if not numItem:
      raise ValueError('must have itemnumber')
    if not numWriter:
      raise ValueError('must have writer')
    review = self.model(
      score = score,
      content = content,
      cntImg = cntImg,
      image1 = images[0],
      image2 = images[1],
      image3 = images[2],
      image4 = images[3],
      image5 = images[4],
      numItem = numItem,
      numWriter = numWriter
    )

    review.save()
    return review

class Review(models.Model):
  reviewnumber = models.AutoField(primary_key=True)
  score = models.IntegerField(verbose_name="평점")
  content = models.TextField(verbose_name="리뷰내용")
  cntImg = models.IntegerField(verbose_name="이미지 수")
  image1 = models.TextField(verbose_name="이미지1")
  image2 = models.TextField(verbose_name="이미지2")
  image3 = models.TextField(verbose_name="이미지3")
  image4 = models.TextField(verbose_name="이미지4")
  image5 = models.TextField(verbose_name="이미지5")
  numItem = models.IntegerField(verbose_name="아이템번호")
  numWriter = models.IntegerField(verbose_name="작성자번호")

  objects = ReviewManager()

  REQUIRED_FIELD = ["score", "numItem", 'numWriter']

  def __str__(self):
    return self.score
  
  def has_perm(self, perm, obj=None):
    return True
  
  def has_module_perms(self, app_label):
    return True
  