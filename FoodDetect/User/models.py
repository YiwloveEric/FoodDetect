from django.db import models
from datetime import date


# Create your models here.
class Users(models.Model):
    user_id = models.IntegerField(primary_key=True, verbose_name="用户id")
    name = models.CharField(max_length=255, unique=True, verbose_name="姓名")
    openid = models.CharField(max_length=128, verbose_name="openid")

    class Meta:
        db_table = "User"
        verbose_name = "用户表"


class Favorites(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="用户id")
    favorites_id = models.IntegerField(primary_key=True, verbose_name="收藏夹id")
    note = models.CharField(max_length=255, blank=True, verbose_name="备注")
    history_id = models.ForeignKey('History', default=None, on_delete=models.CASCADE, verbose_name="历史记录")

    class Meta:
        db_table = "Favorites"
        verbose_name = "收藏夹"


class History(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="用户id")
    image = models.ImageField(default=None, verbose_name="图片url")
    # favorites = models.ForeignKey(Favorites, on_delete=models.CASCADE, verbose_name="收藏夹id", blank=True)
    history_id = models.AutoField(primary_key=True, verbose_name="收藏夹id")
    date = models.DateField(auto_now_add=True, verbose_name="历史记录的时间")

    class Meta:
        db_table = "History"
        verbose_name = "历史记录"
