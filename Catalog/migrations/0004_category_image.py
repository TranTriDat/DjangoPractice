# Generated by Django 3.2.12 on 2022-04-05 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Catalog', '0003_alter_category_category_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category_images/'),
        ),
    ]
