# Generated by Django 4.1.4 on 2022-12-12 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmaker',
            fields=[
                ('key', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('key', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=50, unique=True)),
                ('last_update_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('commence_time', models.DateTimeField()),
                ('home_team', models.CharField(max_length=50)),
                ('away_team', models.CharField(max_length=50)),
                ('sport', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='odds.sport')),
            ],
        ),
        migrations.CreateModel(
            name='BetOdds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_update_time', models.DateTimeField()),
                ('market', models.CharField(max_length=50)),
                ('name_1', models.CharField(max_length=50)),
                ('price_1', models.SmallIntegerField()),
                ('point_1', models.FloatField(blank=True, null=True)),
                ('name_2', models.CharField(max_length=50)),
                ('price_2', models.SmallIntegerField()),
                ('point_2', models.FloatField(blank=True, null=True)),
                ('bookmaker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='odds.bookmaker')),
                ('game', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='odds.game')),
            ],
        ),
    ]