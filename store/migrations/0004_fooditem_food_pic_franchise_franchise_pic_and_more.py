# Generated by Django 4.0 on 2022-03-02 23:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_fooditem_type_alter_franchise_fish_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooditem',
            name='food_pic',
            field=models.ImageField(default=django.utils.timezone.now, upload_to=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='franchise',
            name='franchise_pic',
            field=models.ImageField(default=django.utils.timezone.now, upload_to=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='item_pic',
            field=models.ImageField(default=django.utils.timezone.now, upload_to=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mongers',
            name='monger_pic',
            field=models.ImageField(default=django.utils.timezone.now, upload_to=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='restaurant_pic',
            field=models.ImageField(default=django.utils.timezone.now, upload_to=None),
            preserve_default=False,
        ),
    ]