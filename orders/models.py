from django.db import models
import datetime

class OrderManager(models.Manager):
  def create_order(self, seller, buyer, itemnumber, startTime, endTime, price, buyerName, buyerPhone, buyerEmail, buyerDemand):
    order = self.model(
      seller = seller,
      buyer = buyer,
      itemnumber = itemnumber,
      startTime = startTime,
      endTime = endTime,
      price = price,
      buyerName = buyerName,
      buyerPhone = buyerPhone,
      buyerEmail = buyerEmail,
      buyerDemand = buyerDemand
    )

    order.save()
    return order

class Order(models.Model):
  ordernumber = models.AutoField(primary_key=True)
  seller = models.IntegerField("판매자번호")
  buyer = models.IntegerField("구매자번호")
  itemnumber = models.IntegerField("아이템번호")
  startTime = models.TextField("시작시간")
  endTime = models.TextField("종료시간")
  price = models.IntegerField("가격")
  buyerName = models.CharField("구매자 이름", max_length=30)
  buyerPhone = models.TextField("구매자 휴대폰번호")
  buyerEmail = models.TextField("구매자 이메일")
  buyerDemand = models.TextField("구매자 요청사항")
  confirmTime = models.DateTimeField("확정시간", default=datetime.datetime.now)

  objects = OrderManager()

  REQUIRED_FIELD = ["seller", "buyer", 'itemnumber']

  def __str__(self):
    return self.title
  
  def has_perm(self, perm, obj=None):
    return True
  
  def has_module_perms(self, app_label):
    return True
  