# Generated by Django 2.0.1 on 2018-03-17 10:37

from django.db import migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20180315_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='month',
            name='SpentList',
            field=picklefield.fields.PickledObjectField(default=1, editable=False),
            preserve_default=False,
        ),
    ]
