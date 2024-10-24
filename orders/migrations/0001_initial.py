# Generated by Django 5.1 on 2024-08-29 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgreementColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_sheets', models.IntegerField(verbose_name='枚数')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='単価')),
            ],
            options={
                'verbose_name': '同意説明書カラー',
                'verbose_name_plural': '同意説明書カラー',
            },
        ),
    ]
