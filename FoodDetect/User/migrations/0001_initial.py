# Generated by Django 4.1 on 2023-11-11 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('favorites_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='收藏夹id')),
                ('note', models.CharField(blank=True, max_length=255, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='用户id')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='姓名')),
                ('openid', models.CharField(max_length=128, verbose_name='openid')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('image_url', models.CharField(max_length=255, unique=True, verbose_name='图片url')),
                ('history_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='收藏夹id')),
                ('date', models.DateField(auto_now_add=True, verbose_name='历史记录的时间')),
                ('favorites', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.favorites', verbose_name='收藏夹id')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.user', verbose_name='用户id')),
            ],
        ),
        migrations.AddField(
            model_name='favorites',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.user', verbose_name='用户id'),
        ),
    ]