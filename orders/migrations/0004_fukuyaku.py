# Generated by Django 5.1 on 2024-10-24 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_casecard_chiken_alter_agreementcolor_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fukuyaku',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_sheets', models.IntegerField(verbose_name='枚数')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='単価')),
            ],
            options={
                'verbose_name': '服薬日誌',
                'verbose_name_plural': '服薬日誌',
            },
        ),
    ]