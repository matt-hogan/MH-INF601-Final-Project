# Generated by Django 4.1.4 on 2022-12-12 19:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tracker.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackedBet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sportsbook', models.CharField(max_length=50)),
                ('sport', models.CharField(max_length=50)),
                ('market', models.CharField(choices=[('h2h', 'Moneyline'), ('spreads', 'Spread'), ('totals', 'Total'), ('other', 'Other')], max_length=20)),
                ('description', models.CharField(max_length=240)),
                ('points', models.FloatField(blank=True, null=True)),
                ('bet_amount', models.FloatField(validators=[tracker.validators.validate_bet_amount])),
                ('odds', models.IntegerField(validators=[tracker.validators.validate_odds])),
                ('winnings', models.FloatField(blank=True, null=True)),
                ('result', models.CharField(choices=[('pending', 'Pending'), ('win', 'Win'), ('loss', 'Loss'), ('void', 'Void')], default='pending', max_length=20)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
