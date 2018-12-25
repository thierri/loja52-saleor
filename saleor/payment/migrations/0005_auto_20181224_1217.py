# Generated by Django 2.1.4 on 2018-12-24 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_auto_20181206_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='charge_status',
            field=models.CharField(choices=[('charged', 'CHARGED'), ('waiting', 'Waiting Confirmation'), ('paid', 'Paid'), ('unpaid', 'Unpaid'), ('not-charged', 'Not charged'), ('fully-refunded', 'Fully refunded')], default='not-charged', max_length=15),
        ),
    ]