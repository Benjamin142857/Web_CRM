# Generated by Django 2.2.5 on 2019-12-03 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0002_auto_20191202_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuroot',
            name='icon',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='根菜单图标'),
        ),
        migrations.AddField(
            model_name='menuroot',
            name='weight',
            field=models.IntegerField(default=142857, verbose_name='根菜单排序权重'),
        ),
    ]