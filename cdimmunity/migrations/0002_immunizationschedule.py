# Generated by Django 5.0.2 on 2024-02-25 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cdimmunity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImmunizationSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccine_name', models.CharField(max_length=100)),
                ('recommended_age', models.PositiveIntegerField(help_text='Recommended age in months for this dose')),
                ('number_of_doses', models.PositiveIntegerField(default=1)),
                ('additional_info', models.TextField(blank=True, null=True)),
                ('child_name', models.CharField(max_length=100)),
                ('child_image', models.ImageField(blank=True, null=True, upload_to='child_images/')),
            ],
        ),
    ]
