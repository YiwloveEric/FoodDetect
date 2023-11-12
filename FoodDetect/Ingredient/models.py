from django.db import models


# Create your models here.
class Ingredient(models.Model):
    ingredient_id = models.IntegerField(primary_key=True, verbose_name="配料id")
    chinese_name = models.CharField(max_length=255, unique=True, verbose_name="中文名")
    english_name = models.CharField(max_length=255, unique=True, verbose_name="英文名")
    introduction = models.TextField(verbose_name="简介")
    effects = models.TextField(verbose_name="功效")
    rating = models.FloatField(verbose_name="评分")
    potential_risk_people = models.CharField(max_length=255, null=True, verbose_name="潜在风险人群")
    daily_intake_recommendation = models.TextField(verbose_name="每日建议摄入量")

    class Meta:
        db_table = "Ingredient"
        verbose_name = "配料表"
