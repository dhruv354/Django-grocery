# Generated by Django 3.1.2 on 2021-09-17 11:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Grocery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('price', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('Pending', 'P'), ('Bought', 'B'), ('Not available', 'NA')], default='Pending', max_length=20)),
            ],
            options={
                'verbose_name': 'Groceries',
            },
        ),
        migrations.CreateModel(
            name='GroceryList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(blank=True)),
                ('groceries', models.ManyToManyField(to='grocery_app.Grocery')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Saved',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groceryList', models.ManyToManyField(to='grocery_app.GroceryList')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
