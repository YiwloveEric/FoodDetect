# Generated by Django 4.1 on 2023-11-11 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorites',
            options={'verbose_name': '收藏夹'},
        ),
        migrations.AlterModelOptions(
            name='history',
            options={'verbose_name': '历史记录'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户表'},
        ),
        migrations.RemoveField(
            model_name='history',
            name='image_url',
        ),
        migrations.AddField(
            model_name='history',
            name='image',
            field=models.ImageField(default='', upload_to='', verbose_name='图片url'),
        ),
        migrations.AlterModelTable(
            name='favorites',
            table='Favorites',
        ),
        migrations.AlterModelTable(
            name='history',
            table='History',
        ),
        migrations.AlterModelTable(
            name='user',
            table='User',
        ),
    ]
