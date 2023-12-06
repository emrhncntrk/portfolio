# Generated by Django 4.2 on 2023-05-20 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_comments_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='get_category', to='auctions.categories'),
        ),
    ]
