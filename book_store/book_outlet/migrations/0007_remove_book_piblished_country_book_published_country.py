# Generated by Django 5.0.1 on 2024-02-01 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_outlet', '0006_country_book_piblished_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='piblished_country',
        ),
        migrations.AddField(
            model_name='book',
            name='published_country',
            field=models.ManyToManyField(null=True, related_name='books', to='book_outlet.country'),
        ),
    ]
