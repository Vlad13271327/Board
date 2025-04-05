# Generated by Django 5.1.6 on 2025-02-28 16:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('tanks', 'Танки'), ('hralers', 'Хилы'), ('damage_dealers', 'ДД'), ('traders', 'торговецы'), ('gildmasters', 'гилдмастеры'), ('questgivers', 'квестгиверы'), ('blacksmiths', 'кузнецы'), ('tanners', 'кожевники'), ('potions_master', 'зельевар'), ('spellmaster', 'мастер заклинаний')], max_length=25, verbose_name='Категория')),
                ('date_in', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=250, verbose_name='Название')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текс')),
                ('status', models.BooleanField(default=True)),
                ('date_in', models.DateField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MMO_board.post')),
            ],
        ),
    ]
